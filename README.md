# Shantae-HGHU-TW

**《桑塔：半精靈英雄 終極版》台灣正體中文化專案**

> Shantae: Half-Genie Hero Ultimate Edition — Traditional Chinese (Taiwan) Localization Project

提供台灣用語的正體中文翻譯與繁體中文補丁；本專案為非官方社群作品。

[![最新版本](https://img.shields.io/github/v/release/AghDoo/Shantae-HGHU-TW?include_prereleases&sort=semver)](https://github.com/AghDoo/Shantae-HGHU-TW/releases)
[![翻譯驗證](https://github.com/AghDoo/Shantae-HGHU-TW/actions/workflows/translation-pr.yml/badge.svg)](https://github.com/AghDoo/Shantae-HGHU-TW/actions/workflows/translation-pr.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![語系：zh-Hant-TW](https://img.shields.io/badge/locale-zh--Hant--TW-bf3f7f)](translations/zh-Hant-TW/)
[![平台：Windows](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white)](https://github.com/AghDoo/Shantae-HGHU-TW/releases)

[![GitHub stars](https://img.shields.io/github/stars/AghDoo/Shantae-HGHU-TW?style=social)](https://github.com/AghDoo/Shantae-HGHU-TW/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/AghDoo/Shantae-HGHU-TW)](https://github.com/AghDoo/Shantae-HGHU-TW/issues)
[![Star History](https://img.shields.io/badge/Star%20History-查看趨勢-FFD700?logo=github)](https://www.star-history.com/#AghDoo/Shantae-HGHU-TW&Date)

## 下載

前往 [GitHub Releases](https://github.com/AghDoo/Shantae-HGHU-TW/releases) 下載最新版本的 Windows 安裝程式。

目前公開版本仍屬 Beta 測試階段。安裝前請確認：

- 作業系統為 Windows 10 或 Windows 11。
- 已合法持有並安裝 Steam 版 Ultimate Edition（App ID `764300`）。
- 遊戲檔案符合該版本列出的已知原廠基線。
- 安裝與解除安裝期間均已關閉遊戲。

Windows SmartScreen 可能因安裝程式尚未使用 Authenticode 憑證簽署而顯示警告。執行前請核對 Release 頁面列出的 SHA-256。

完整操作方式請參閱 [安裝與解除安裝](docs/INSTALLATION.md)；遇到問題請先閱讀 [疑難排解](docs/TROUBLESHOOTING.md)。

## 安裝方式

1. 關閉遊戲。
2. 從最新 Release 下載 `Shantae-HGHU-TW-{版本}-setup.exe`。
3. 執行安裝程式，確認偵測到受支援的原廠遊戲檔案後完成安裝。

再次執行同一份 EXE，即可解除安裝繁體中文化並還原原廠檔案。安裝完成後，遊戲目錄 `.hghu-tw/installer/` 也會保存本機備援解除安裝程式。

安裝器採 fail-closed 設計：偵測到未知修改、不完整的安裝狀態或損毀的備份時會停止操作，不會推測或強制覆寫檔案。

## 專案狀態

- Locale：`zh-Hant-TW`
- 公開譯文目錄：5,497 筆
- 發布形式：單檔 Windows 安裝程式與必要驗證資料
- 目前階段：公開 Beta／Pre-release

公開 `main` 是已通過翻譯 Review 的來源，不等於已通過實機驗證的 Release。每個候選版本仍須由非公開建置環境鎖定完整 commit、重新建置、回套驗證並完成遊戲內測試後才會發布。

## 問題回報

- 安裝、解除安裝或還原問題：建立「安裝器／解除安裝問題」Issue。
- 翻譯錯誤、文字截斷或顯示問題：建立「翻譯／顯示問題」Issue。

請勿上傳完整遊戲 PAK、官方完整原始文本、私人路徑、個人資料或其他未經授權的遊戲內容。

## 翻譯貢獻

本 Repository 也是公開翻譯協作入口，接受錯字、語氣、專有名詞、UI 長度與換行等修正。角色名、地名與術語請先查閱[專有名詞對照表](docs/GLOSSARY.md)。

提交前請閱讀：

- [貢獻指南](CONTRIBUTING.md)
- [翻譯規範](TRANSLATION_GUIDE.md)
- [專有名詞對照表](docs/GLOSSARY.md)
- [翻譯 PR Template](.github/PULL_REQUEST_TEMPLATE/translation.md)

Pull Request 會自動檢查：

- 5,497 個 ID 是否完整、唯一、排序且未被修改。
- `area` 與 `required_tokens` 等不可變欄位是否漂移。
- 格式 token、換行與契約遷移是否一致。
- `catalog.json` 的列數與 SHA-256 是否對應目前 CSV。

本機可使用：

```powershell
python tools/validate_translations.py --write-manifest
python -m unittest discover -s tests -v
```

## 專案與發布文件

- [專有名詞對照表](docs/GLOSSARY.md)
- [命名規範](NAMING.md)
- [版本規則](VERSIONING.md)
- [Release 發布規範](release/README.md)
- [權利與內容聲明](NOTICE.md)

## 譯名參考與致謝

本專案在系列譯名整理與翻譯過程中，參考了：

- 《Shantae and the Seven Sirens》官方繁體中文版
- 《香緹：半精靈英雄》正體中文模組（CodeBay.IN 出品）

感謝上述官方在地化作品與社群中文化團隊留下的翻譯成果，為本專案的系列譯名研究與一致性整理提供參考。更完整的說明請參閱[專有名詞對照表](docs/GLOSSARY.md#譯名參考與致謝)。

## 支持專案

如果這份中文化對你有幫助，歡迎透過 [Ko-fi](https://ko-fi.com/aghdoo) 支持後續的翻譯校對、字型維護與測試工作。

## 授權與權利聲明

本專案為非官方社群中文化專案，與 WayForward Technologies 或其他相關權利人沒有隸屬、授權、贊助或背書關係。

程式碼與文件授權請參閱 [LICENSE](LICENSE)；第三方商標、遊戲內容及翻譯相關聲明請參閱 [NOTICE.md](NOTICE.md)。