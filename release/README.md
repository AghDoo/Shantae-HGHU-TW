# Release 發布規範

正式漢化包應附加於本 Repository 的 GitHub Release，不要將每一版 ZIP 或大型二進位檔直接 Commit 進 Git。

## 建議附件

```text
Shantae-HGHU-TW-v0.1.0-patch.zip
manifest.json
SHA256SUMS.txt
```

## 發布前流程

1. 翻譯 PR 已合併至 `main`。
2. 私有／本機 Workspace 將 Submodule 更新至待發布 Commit。
3. 使用正版遊戲檔與本機建置工具產生漢化包。
4. 完成遊戲內實機測試。
5. Tag 指向實際通過測試的翻譯 Commit。
6. 建立 GitHub Release 並上傳附件、相容版本與已知問題。

## Manifest 建議欄位

```json
{
  "name": "Shantae-HGHU-TW",
  "version": "0.1.0",
  "locale": "zh-Hant-TW",
  "gameVersion": "待確認",
  "translationCommit": "待填入完整 Commit SHA",
  "packageType": "delta-patch",
  "builderVersion": "待確認"
}
```

優先發布差異補丁、安裝器或完全由本專案製作的新增檔案，避免發布包含大量原始遊戲內容的完整修改資源檔。
