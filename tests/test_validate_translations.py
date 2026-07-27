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
            VALIDATOR.validate_base([changed], [base])

    def test_allows_translation_and_note_change(self) -> None:
        base = row()
        changed = {**base, "translated_tw": "就在這裡！", "translator_note": "調整語氣"}
        changed["required_tokens"] = base["required_tokens"]
        VALIDATOR.validate_base([changed], [base])

    def test_requires_canonical_token_json(self) -> None:
        candidate = row()
        tokens = json.loads(candidate["required_tokens"])
        candidate["required_tokens"] = json.dumps(tokens, ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "canonical"):
            VALIDATOR.validate_rows([candidate], "test")


if __name__ == "__main__":
    unittest.main()
