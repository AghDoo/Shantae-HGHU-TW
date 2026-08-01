#!/usr/bin/env python3
"""驗證公開 zh-Hant-TW 譯文目錄與 PR 不可變欄位。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable


CATALOG_PATH = Path("translations/zh-Hant-TW/strings.csv")
MANIFEST_PATH = Path("translations/zh-Hant-TW/catalog.json")
MIGRATIONS_PATH = Path("translations/zh-Hant-TW/contract-migrations.json")
FIELDS = ["id", "area", "translated_tw", "required_tokens", "translator_note"]
ID_PATTERN = re.compile(r"^HGHU-TW-(\d{6})$")
ALLOWED_AREAS = {"角色與劇情", "系統與介面", "製作名單", "DLC"}
TOKEN_KEYS = {
    "markup_tag",
    "var_tag",
    "brace_token",
    "escaped_control",
    "printf_token",
    "literal_newline",
}
PROTECTED_PATTERNS = {
    "markup_tag": re.compile(r"<[^<>]+>"),
    "var_tag": re.compile(r"\[VAR:[^\]]+\]"),
    "brace_token": re.compile(r"\{[^{}]+\}"),
    "escaped_control": re.compile(r"\\[nrt]"),
    "printf_token": re.compile(r"(?<!\d)%(?:\d+\$)?[-+#0]*\d*(?:\.\d+)?[diuoxXfFeEgGaAcspn]"),
    "literal_newline": re.compile(r"\n"),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def token_json(text: str) -> str:
    tokens = {
        name: sorted(match.group(0) for match in pattern.finditer(text))
        for name, pattern in PROTECTED_PATTERNS.items()
    }
    return json.dumps(tokens, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_tokens(value: object, label: str) -> str:
    if not isinstance(value, dict) or set(value) != TOKEN_KEYS:
        raise ValueError(f"{label} token schema 不符")
    if any(
        not isinstance(items, list)
        or any(not isinstance(item, str) for item in items)
        for items in value.values()
    ):
        raise ValueError(f"{label} token value 格式不符")
    return json.dumps(
        {key: sorted(items) for key, items in value.items()},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def parse_migrations(data: bytes, label: str) -> dict[tuple[str, str, str, str], str]:
    document = json.loads(data.decode("utf-8", "strict"))
    if not isinstance(document, dict) or set(document) != {"schema_version", "migrations"}:
        raise ValueError(f"{label} schema 不符")
    if document["schema_version"] != 1 or not isinstance(document["migrations"], list):
        raise ValueError(f"{label} schema version 或 migrations 格式不符")
    result: dict[tuple[str, str, str, str], str] = {}
    required_fields = {"id", "field", "from_value", "to_value", "reason"}
    for index, migration in enumerate(document["migrations"]):
        item_label = f"{label} migrations[{index}]"
        if not isinstance(migration, dict) or set(migration) != required_fields:
            raise ValueError(f"{item_label} 欄位不符")
        public_id = migration["id"]
        if not isinstance(public_id, str) or not ID_PATTERN.fullmatch(public_id):
            raise ValueError(f"{item_label} id 格式錯誤")
        if migration["field"] != "required_tokens":
            raise ValueError(f"{item_label} 只允許 required_tokens")
        before = canonical_tokens(migration["from_value"], f"{item_label}.from_value")
        after = canonical_tokens(migration["to_value"], f"{item_label}.to_value")
        reason = migration["reason"]
        if before == after:
            raise ValueError(f"{item_label} 不得記錄無變更遷移")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{item_label} reason 不得空白")
        key = (public_id, "required_tokens", before, after)
        if key in result:
            raise ValueError(f"{item_label} 重複")
        result[key] = reason
    return result


def validate_migration_history(
    current: dict[tuple[str, str, str, str], str],
    base: dict[tuple[str, str, str, str], str],
) -> set[tuple[str, str, str, str]]:
    for key, reason in base.items():
        if current.get(key) != reason:
            raise ValueError("既有格式契約遷移不得刪除或修改")
    return set(current) - set(base)


def parse_catalog(data: bytes, label: str) -> list[dict[str, str]]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{label} 不得含 UTF-8 BOM")
    text = data.decode("utf-8", "strict")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != FIELDS:
        raise ValueError(f"{label} schema/order 不符：{reader.fieldnames}")
    return list(reader)


def validate_rows(rows: list[dict[str, str]], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} 不得為空")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{label} 含重複 id")
    numbers: list[int] = []
    for row in rows:
        public_id = row["id"]
        match = ID_PATTERN.fullmatch(public_id)
        if not match:
            raise ValueError(f"id 格式錯誤：{public_id}")
        numbers.append(int(match.group(1)))
        if row["area"] not in ALLOWED_AREAS:
            raise ValueError(f"area 不在允許清單：{public_id}")
        translated = row["translated_tw"]
        if not translated.strip():
            raise ValueError(f"translated_tw 空白：{public_id}")
        if "\ufffd" in translated or "\x00" in translated:
            raise ValueError(f"translated_tw 含損壞字元：{public_id}")
        try:
            required = json.loads(row["required_tokens"])
        except json.JSONDecodeError as exc:
            raise ValueError(f"required_tokens JSON 錯誤：{public_id}") from exc
        if not isinstance(required, dict) or set(required) != TOKEN_KEYS:
            raise ValueError(f"required_tokens schema 不符：{public_id}")
        if any(not isinstance(value, list) or any(not isinstance(item, str) for item in value) for value in required.values()):
            raise ValueError(f"required_tokens value 格式不符：{public_id}")
        if row["required_tokens"] != json.dumps(
            {key: sorted(value) for key, value in required.items()},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ):
            raise ValueError(f"required_tokens 必須 canonical：{public_id}")
        if token_json(translated) != row["required_tokens"]:
            raise ValueError(f"protected token mismatch：{public_id}")
    if numbers != sorted(numbers):
        raise ValueError("id 必須依數字遞增")


def git_blob(repo: Path, ref: str, path: Path, *, allow_missing: bool = False) -> bytes | None:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={repo.as_posix()}", "show", f"{ref}:{path.as_posix()}"],
        cwd=repo,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        if allow_missing and (
            b"does not exist" in result.stderr
            or b"exists on disk, but not in" in result.stderr
        ):
            return None
        raise ValueError(f"無法讀取 base catalog：{result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def validate_base(
    current: list[dict[str, str]],
    base: list[dict[str, str]],
    new_migrations: set[tuple[str, str, str, str]],
) -> None:
    if len(current) != len(base):
        raise ValueError(f"PR 不得新增或刪除字串：{len(current)} != {len(base)}")
    for current_row, base_row in zip(current, base, strict=True):
        for field in ("id", "area"):
            if current_row[field] != base_row[field]:
                raise ValueError(f"PR 不得修改 {field}：{base_row['id']}")
        if current_row["required_tokens"] != base_row["required_tokens"]:
            migration = (
                base_row["id"],
                "required_tokens",
                base_row["required_tokens"],
                current_row["required_tokens"],
            )
            if migration not in new_migrations:
                raise ValueError(
                    f"PR 不得修改 required_tokens，除非附上精確契約遷移：{base_row['id']}"
                )
            new_migrations.remove(migration)
    if new_migrations:
        raise ValueError("新增的格式契約遷移沒有對應本次 catalog 變更")


def validate_manifest(repo: Path, catalog_bytes: bytes, rows: list[dict[str, str]]) -> None:
    manifest = json.loads((repo / MANIFEST_PATH).read_text(encoding="utf-8"))
    expected = {
        "schema_version": 1,
        "locale": "zh-Hant-TW",
        "catalog": "strings.csv",
        "row_count": len(rows),
        "catalog_sha256": sha256_bytes(catalog_bytes),
        "id_range": [rows[0]["id"], rows[-1]["id"]],
        "contains_official_source_text": False,
    }
    if manifest != expected:
        raise ValueError("catalog.json 與 strings.csv 不一致；請執行 --write-manifest")


def write_manifest(repo: Path, catalog_bytes: bytes, rows: list[dict[str, str]]) -> None:
    manifest = {
        "schema_version": 1,
        "locale": "zh-Hant-TW",
        "catalog": "strings.csv",
        "row_count": len(rows),
        "catalog_sha256": sha256_bytes(catalog_bytes),
        "id_range": [rows[0]["id"], rows[-1]["id"]],
        "contains_official_source_text": False,
    }
    (repo / MANIFEST_PATH).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="驗證公開譯文 CSV。")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--base-ref")
    parser.add_argument("--allow-initial-catalog", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    catalog_bytes = (repo / CATALOG_PATH).read_bytes()
    rows = parse_catalog(catalog_bytes, str(CATALOG_PATH))
    validate_rows(rows, str(CATALOG_PATH))
    migrations = parse_migrations(
        (repo / MIGRATIONS_PATH).read_bytes(), str(MIGRATIONS_PATH)
    )
    if args.base_ref:
        base_bytes = git_blob(
            repo,
            args.base_ref,
            CATALOG_PATH,
            allow_missing=args.allow_initial_catalog,
        )
        if base_bytes is not None:
            base_rows = parse_catalog(base_bytes, f"{args.base_ref}:{CATALOG_PATH}")
            validate_rows(base_rows, "base catalog")
            base_migration_bytes = git_blob(
                repo, args.base_ref, MIGRATIONS_PATH, allow_missing=True
            )
            base_migrations = (
                parse_migrations(base_migration_bytes, f"{args.base_ref}:{MIGRATIONS_PATH}")
                if base_migration_bytes is not None
                else {}
            )
            new_migrations = validate_migration_history(migrations, base_migrations)
            validate_base(rows, base_rows, new_migrations)
    if args.write_manifest:
        write_manifest(repo, catalog_bytes, rows)
    validate_manifest(repo, catalog_bytes, rows)
    print(f"[ok] zh-Hant-TW catalog：{len(rows):,} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
