from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate_translations.py"
SPEC = importlib.util.spec_from_file_location("validate_translations", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def row(public_id: str = "HGHU-TW-000001", text: str = "已到站啦！") -> dict[str, str]:
    return {
        "id": public_id,
        "area": "角色與劇情",
        "translated_tw": text,
        "required_tokens": VALIDATOR.token_json(text),
        "translator_note": "",
    }


class ValidateTranslationsTests(unittest.TestCase):
    def test_accepts_valid_rows(self) -> None:
        VALIDATOR.validate_rows([row()], "test")

    def test_rejects_token_loss(self) -> None:
        source = row(text="<hgh_f c=0>提示</hgh_f>")
        source["translated_tw"] = "提示"
        with self.assertRaisesRegex(ValueError, "protected token mismatch"):
            VALIDATOR.validate_rows([source], "test")

    def test_rejects_immutable_pr_change(self) -> None:
        base = row()
        changed = {**base, "area": "系統與介面"}
        with self.assertRaisesRegex(ValueError, "不得修改 area"):
            VALIDATOR.validate_base([changed], [base], set())

    def test_allows_exact_required_token_contract_migration(self) -> None:
        base = row()
        changed = {**base, "translated_tw": "第一行\n第二行"}
        changed["required_tokens"] = VALIDATOR.token_json(changed["translated_tw"])
        migration = {
            (
                base["id"],
                "required_tokens",
                base["required_tokens"],
                changed["required_tokens"],
            )
        }
        VALIDATOR.validate_base([changed], [base], migration)

    def test_rejects_unused_contract_migration(self) -> None:
        base = row()
        migration = {
            (base["id"], "required_tokens", base["required_tokens"], "unused")
        }
        with self.assertRaisesRegex(ValueError, "沒有對應"):
            VALIDATOR.validate_base([base], [base], migration)

    def test_rejects_contract_migration_history_rewrite(self) -> None:
        key = ("HGHU-TW-000001", "required_tokens", "before", "after")
        with self.assertRaisesRegex(ValueError, "不得刪除或修改"):
            VALIDATOR.validate_migration_history({key: "新理由"}, {key: "原理由"})

    def test_allows_translation_and_note_change(self) -> None:
        base = row()
        changed = {**base, "translated_tw": "就在這裡！", "translator_note": "調整語氣"}
        changed["required_tokens"] = base["required_tokens"]
        VALIDATOR.validate_base([changed], [base], set())

    def test_requires_canonical_token_json(self) -> None:
        candidate = row()
        tokens = json.loads(candidate["required_tokens"])
        candidate["required_tokens"] = json.dumps(tokens, ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "canonical"):
            VALIDATOR.validate_rows([candidate], "test")


if __name__ == "__main__":
    unittest.main()
