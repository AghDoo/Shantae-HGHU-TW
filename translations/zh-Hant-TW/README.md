# zh-Hant-TW 翻譯資料

此目錄存放可透過 Pull Request 修改的台灣正體中文 CSV 譯文。

本目錄不得加入官方完整原文、遊戲資源或其他不適合公開散布的內容。

## 目前內容

```text
strings.csv    5,497 筆可透過 PR 修正的台灣正體中文譯文
catalog.json   目錄列數、ID 範圍與 strings.csv SHA-256
```

`strings.csv` 欄位為：

```text
id,area,translated_tw,required_tokens,translator_note
```

- 可修改：`translated_tw`、`translator_note`
- 不可修改：`id`、`area`、`required_tokens`

公開 ID 不包含 PAK、offset 或官方原文資訊。建置端另有不公開的 ID
對照，只有完整 ID 集合、來源 hash 與 token 全部吻合才會接受 PR 譯文。

## 編輯前請閱讀

- [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
- [`TRANSLATION_GUIDE.md`](../../TRANSLATION_GUIDE.md)
