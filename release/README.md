# Release 發布規範

正式中文化發布檔應附加於本 Repository 的 GitHub Release，不要將每一版大型二進位檔直接 Commit 進 Git。

## 發布資產型態

每個版本只能依實際交付方式選擇一種主要發布資產：

```text
單檔安裝器：Shantae-HGHU-TW-0.9.0-beta.1-setup.exe
差分壓縮包：Shantae-HGHU-TW-0.9.0-beta.1.zip
```

單檔安裝器版本不需要再提供內容重複的 ZIP；差分壓縮包版本則不應同時提供功能重複的安裝器。

每個公開版本另提供必要驗證資料：

```text
0.9.0-beta.1-release-index.json
0.9.0-beta.1-security-audit.json
```

建置流水線的中間產物不應預設公開。只有在 release index 或 security audit 明確引用、且外部驗證確實需要時，才附加其他 JSON。

## 發布前流程

1. 翻譯 PR 已合併至 `main`。
2. 非公開建置環境以完整 Git SHA 鎖定該 Commit。
3. 匯入時驗證完整 ID 集合、來源 hash 與格式 token。
4. 使用正版原廠遊戲檔重新建置並反向驗證。
5. 完成遊戲內實機測試。
6. 由原廠檔與受測成品建立逐 PAK `xdelta3` 差分並回套驗證。
7. Tag 指向實際受測的翻譯 Commit。
8. 建立 GitHub Release，設定正確的 prerelease／stable 狀態並上傳主要發布資產與必要驗證資料。
9. 核對 Release notes 中的版本、commit、工具版本與 SHA-256。

## Release index

外部 `release-index.json` 應固定：

- 中文化版本與 prerelease／stable 狀態
- 主要發布資產名稱、大小與 SHA-256
- 公開譯文 commit
- 支援的遊戲版本與原廠基線
- 建置與候選 provenance
- 對應 security audit

差分壓縮包可在 ZIP 內附 `release-manifest.json` 與 `SHA256SUMS`。單檔安裝器則應將執行所需的 manifest、授權文件與差分 payload 納入經 audit 的安裝器內容，不需要另外上傳內容重複的 ZIP。

## Manifest 核心欄位

```json
{
  "name": "Shantae-HGHU-TW",
  "version": "0.9.0-beta.1",
  "locale": "zh-Hant-TW",
  "gameVersion": "待確認",
  "translationCommit": "待填入完整 Commit SHA",
  "packageType": "installer",
  "builderVersion": "待確認",
  "patchTool": "xdelta3 3.2.0",
  "prerelease": true
}
```

`packageType` 依主要發布資產使用 `installer` 或 `delta-patch`。

## Release notes

Release notes 應聚焦於該版本本身：

- 玩家可見變更
- 已知問題與限制
- 該版本特有的升級或移除注意事項
- 公開譯文 commit
- 建置與資安工具版本
- 主要發布資產、release index 與 security audit 的 SHA-256

固定的安裝、解除安裝、疑難排解與問題回報方式應維護於 README、`docs/` 與 Issue Forms，不需要在每一版 Release notes 重複。

## 安全與相容性

優先發布差異補丁、安裝器或完全由本專案製作的新增檔案，避免發布包含大量原始遊戲內容的完整修改資源檔。

Beta 只能建立 GitHub prerelease，manifest 必須明記尚未完成的 smoke 項目；正式版則必須由完整 runtime gate 通過的候選產生。差分安裝器會先核對原廠 SHA-256，未知或已被其他模組修改的 PAK 會直接停止。