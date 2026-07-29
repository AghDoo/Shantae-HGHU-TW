# 貢獻指南

感謝協助改善《桑塔：半精靈英雄 終極版》的台灣正體中文翻譯。

## 可接受的變更

- 修正錯字、標點與語病。
- 改善語句自然度或角色語氣。
- 統一人名、地名、道具名及介面用語。
- 修正文字超框、換行或格式標記。
- 補充必要的翻譯情境與備註。

## Pull Request 原則

- 一個 PR 應聚焦於單一角色、場景、介面區域或明確問題。
- 不要順手修改無關內容。
- 不得修改或移除字串識別碼。
- 不得修改 `area` 或 `required_tokens`；這兩欄由建置端維護。
- 必須保留 `{0}`、`%s`、`<color>` 等變數與格式標記。
- 如涉及情境、文字框或顯示問題，請附修改前後截圖。
- 未經確認，不得提交官方完整原文、遊戲資源、執行檔或反編譯內容。

## CSV 編輯規則

- 編碼固定為 UTF-8。
- 換行格式固定為 LF。
- 使用符合 RFC 4180 慣例的 CSV quoting。
- 欄位包含逗號、半形雙引號或換行時，必須以半形雙引號包住。
- 欄位內的半形雙引號必須寫成兩個雙引號。
- 不得使用簡單的 `Split(',')` 解析 CSV。
- 使用試算表軟體後，請確認字串 ID、前導零與編碼未被自動轉換。
- 儲存後執行 `python tools/validate_translations.py --write-manifest`，
  將 `catalog.json` 一併提交。

目前 CSV 欄位固定為：

```text
id,area,translated_tw,required_tokens,translator_note
```

可修改欄位只有 `translated_tw` 與 `translator_note`。公開 ID 只供 PR
定位；真正的遊戲結構座標與官方原文不會放在此 Repository。

## 建議分支名稱

```text
fix/dialogue-typo
fix/menu-terminology
fix/character-tone
```

## Commit 格式

本專案使用 Conventional Commits，例如：

```text
fix(dialogue): 修正角色對話語氣
fix(ui): 統一存檔與讀取用語
```

## Review 流程

Public `main` 代表譯文已通過公開可執行的格式、內容與語境 Review，
不代表該譯文已完成候選 PAK 建置或遊戲實機驗證。合併 PR 與核准
Release 是兩個不同階段。

1. Fork Repository 並建立分支。
2. 修改 `translations/zh-Hant-TW/` 下的翻譯檔案。
3. 建立 Pull Request 並說明修改理由。
4. 通過 CSV、不可變欄位、格式 token、文字與語境 Review。
5. 合併後由維護者鎖定完整 public commit，匯入非公開建置環境。
6. 由非公開流水線完成來源 hash、token、重建與反向抽取驗證，產生
   候選測試包。
7. 候選包通過遊戲實機測試後才安排 Release。
8. 若實測失敗，開啟新的修正 PR，並重新執行上述流程；不得發布未通過
   實機驗證的 public commit。
