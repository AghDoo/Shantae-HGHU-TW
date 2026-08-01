# Release 發布規範

正式中文化發布檔應附加於本 Repository 的 GitHub Release，不要將每一版 ZIP 或大型二進位檔直接 Commit 進 Git。

## 建議附件

```text
Shantae-HGHU-TW-0.8.0-beta.1.zip
0.8.0-beta.1-release-index.json
```

## 發布前流程

1. 翻譯 PR 已合併至 `main`。
2. 非公開建置環境以完整 Git SHA 鎖定該 Commit。
3. 匯入時驗證完整 ID 集合、來源 hash 與格式 token。
4. 使用正版原廠遊戲檔重新建置並反向驗證。
5. 完成遊戲內實機測試。
6. 由原廠檔與受測成品建立逐 PAK `xdelta3` 差分並回套驗證。
7. Tag 指向實際受測的翻譯 Commit。
8. 建立 GitHub Release 並上傳差分包、manifest 與 SHA256SUMS。

差分 ZIP 內含 `release-manifest.json` 與 `SHA256SUMS`；外部
`release-index.json` 固定 archive 大小、SHA-256、譯文 commit 與
Step 10 候選 provenance，兩者都應上傳。

## Manifest 核心欄位

```json
{
  "name": "Shantae-HGHU-TW",
  "version": "0.8.0-beta.1",
  "locale": "zh-Hant-TW",
  "gameVersion": "待確認",
  "translationCommit": "待填入完整 Commit SHA",
  "packageType": "delta-patch",
  "builderVersion": "待確認",
  "patchTool": "xdelta3 3.2.0",
  "prerelease": true
}
```

優先發布差異補丁、安裝器或完全由本專案製作的新增檔案，避免發布包含大量原始遊戲內容的完整修改資源檔。

Beta 只能建立 GitHub prerelease，manifest 必須明記尚未完成的 smoke
項目；正式版則必須由完整 runtime gate 通過的候選產生。差分安裝器會
先核對原廠 SHA-256，未知或已被其他模組修改的 PAK 會直接停止。
