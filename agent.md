# agent.md — 專案規則

本專案是一個由 AI agent 協助維護的知識庫（wiki）。任何 agent 在這個專案中工作時，都必須遵守以下規則。

## 1. 目錄結構

```
/
├── agent.md          # 本規則檔（agent 每次工作前先讀）
├── index.html        # 首頁：列出 wiki/ 下所有子頁面
├── raw/              # 原始資料（唯讀）
├── wiki/             # 整理後的知識頁面（agent 撰寫與維護）
└── scripts/
    └── build_index.py  # 重新產生 index.html 的頁面清單
```

## 2. raw/ — 原始資料

- 存放未經整理的來源：文章、筆記、逐字稿、PDF、網頁擷取、資料檔等。
- **唯讀**：agent 不得修改或刪除 raw/ 內的檔案，只能讀取。
- 新增來源時，檔名使用 `YYYY-MM-DD-簡短描述.副檔名`（例：`2026-11-17-會議記錄.md`）。

## 3. wiki/ — 知識頁面

- 每個主題一個頁面，格式為 HTML（`主題-slug.html`）或 Markdown（`主題-slug.md`）。
- 檔名使用小寫英文、數字與連字號（kebab-case），例：`project-overview.html`。
- 每頁開頭須包含：
  - 標題（HTML 用 `<title>` 與 `<h1>`；Markdown 用第一行 `# 標題`）
  - 一句話摘要
  - 「來源」區塊：列出引用的 raw/ 檔案路徑
- 頁面之間用相對連結互相引用（例：`<a href="other-topic.html">`）。
- 優先更新既有頁面，避免建立重複主題的新頁面。
- 內容須忠於 raw/ 來源；推論或未經證實的內容須明確標示。

## 4. index.html — 首頁

- index.html 必須列出 wiki/ 下的**所有**子頁面，不可遺漏。
- 每次新增、改名或刪除 wiki/ 頁面後，執行：

  ```bash
  python3 scripts/build_index.py
  ```

  此腳本會改寫 index.html 中 `<!-- PAGES:START -->` 與 `<!-- PAGES:END -->` 之間的清單。不要手動編輯這兩個標記之間的內容。

## 5. 工作流程

1. 閱讀本檔（agent.md）。
2. 讀取 raw/ 中新增或相關的資料。
3. 在 wiki/ 建立或更新對應頁面，並補上來源與交叉連結。
4. 執行 `python3 scripts/build_index.py` 更新首頁。
5. 簡短回報本次新增／修改了哪些頁面。

## 6. 禁止事項

- 不修改或刪除 raw/ 內容。
- 不在 wiki/ 以外的位置建立內容頁面。
- 不刪除 wiki/ 頁面，除非使用者明確要求。
- 不修改本規則檔，除非使用者明確要求。
