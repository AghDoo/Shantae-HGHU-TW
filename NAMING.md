# 命名規範

本文件是 `Shantae-HGHU-TW` 對外名稱、版本顯示與 Credit 的唯一命名
契約。不同位置不必使用完全相同的字串，但必須由下表的角色分工派生。

| 用途 | 固定格式 |
|---|---|
| Repository slug | `Shantae-HGHU-TW` |
| 正式中文專案名 | 《桑塔：半精靈英雄 終極版》台灣正體中文化專案 |
| 英文正式名 | Shantae: Half-Genie Hero Ultimate Edition — Traditional Chinese (Taiwan) Localization Project |
| Locale | `zh-Hant-TW` |
| 安裝器產品名 | Shantae HGHU 台灣正體中文化管理程式 |
| 安裝器視窗標題 | `Shantae HGHU 台灣正體中文化管理程式 {SemVer}` |
| Release Title | `Shantae HGHU 台灣正體中文補丁 v{SemVer}` |
| Git tag | `v{SemVer}` |
| Release asset | `Shantae-HGHU-TW-{SemVer}.zip` |
| Credit | 台灣正體中文化 by AghDoo |
| GitHub About | 《桑塔：半精靈英雄 終極版》台灣正體中文化專案｜繁體中文補丁 |

## 用詞分工

- 「台灣正體中文化」是正式品牌與 Credit，用於專案名、安裝器產品名及
  作者署名。
- 「繁體中文化」可用於玩家操作動作，例如「安裝繁體中文化」與
  「解除安裝繁體中文化」。
- 「繁體中文補丁／繁中補丁」是玩家通俗稱呼與搜尋詞，可出現在介紹與
  SEO 文案，但不是正式專案名。
- 「漢化」只作歷史或搜尋別名，不用於新的正式標題、權利聲明或流程
  名稱。
- 英文固定使用 `Traditional Chinese (Taiwan)`；不要使用
  `Taiwan Standard Chinese` 或 `Orthodox Chinese`。

## 版本字串

- Manifest 與機器欄位使用純 SemVer，例如 `0.9.0-beta.1`。
- Git tag 與 Release Title 使用 `v` 前綴，例如 `v0.9.0-beta.1`。
- 安裝器視窗標題顯示純 SemVer，不加 `v`，以對齊安裝器內部版本欄位。
- 已公開的 Release 名稱與資產不可為了套用新命名而回頭修改；本規範只
  約束後續版本。
