# 安裝與解除安裝

本文件適用於 `Shantae-HGHU-TW` 公開 Release 提供的 Windows 中文化管理程式。

## 支援環境

- Windows 10 或 Windows 11
- Steam 版 `Shantae: Half-Genie Hero Ultimate Edition`
- Steam App ID：`764300`
- 符合該 Release 公告之已知原廠檔案基線

其他商店版本、未知遊戲更新、已被其他 MOD 修改的 PAK，均不在目前支援範圍內。

## 安裝前準備

1. 確認遊戲已完全關閉。
2. 建議先透過 Steam 驗證遊戲檔案完整性。
3. 從 GitHub Releases 下載最新安裝程式。
4. 核對 Release 頁面提供的 SHA-256。
5. 若已安裝其他會修改相同 PAK 的 MOD，請先還原原廠檔案。

## 安裝

1. 執行 `Shantae-HGHU-TW-{版本}-setup.exe`。
2. 閱讀並接受使用前聲明。
3. 讓程式偵測 Steam 遊戲目錄，或依畫面提示選擇正確目錄。
4. 程式會先驗證完整 PAK 集合；只有符合支援的原廠基線時才會繼續。
5. 驗證通過後，程式會建立備份並套用差分補丁。
6. 顯示安裝完成後再啟動遊戲。

備份、安裝狀態與本機備援解除安裝程式會保存在遊戲根目錄的 `.hghu-tw` 資料夾。

## 解除安裝

可使用以下任一方式：

- 再次執行安裝時使用的同一份 EXE。
- 執行遊戲根目錄 `.hghu-tw/installer/` 內的本機備援解除安裝程式。

程式確認備份與安裝狀態完整後，會還原原廠檔案。完整還原成功後，`.hghu-tw` 資料夾會一併移除。

## 重要注意事項

- 安裝或還原期間請勿啟動遊戲。
- 請勿強制關閉管理程式。
- 請勿手動修改、移動或刪除 `.hghu-tw` 內的備份與狀態檔。
- 偵測到未知修改、不完整狀態或損毀備份時，程式會停止操作，不會推測或強制覆寫檔案。
- 遊戲更新後，原廠檔案基線可能改變；請先查看最新 Release 說明。

## Windows SmartScreen

安裝程式尚未使用 Authenticode 憑證簽署時，Windows SmartScreen 可能顯示警告。請只從本專案 GitHub Releases 下載，並在執行前核對 SHA-256。

PowerShell 可使用：

```powershell
Get-FileHash .\Shantae-HGHU-TW-0.9.0-beta.1-setup.exe -Algorithm SHA256
```

輸出必須與對應 Release 頁面列出的值完全一致。

## 發生問題時

先閱讀 [疑難排解](TROUBLESHOOTING.md)。仍無法解決時，請使用 GitHub 的「安裝器／解除安裝問題」Issue Form 回報。