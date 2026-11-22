# 腦中風臨床處置 LLM Wiki

這是一個依 Andrej Karpathy **LLM Wiki** 構想建立的個人臨床文獻知識庫，專注於**腦中風臨床處置（AIS、ICH、SAH、TIA 與次級預防、住院併發症）**，搭配 **Obsidian** 閱讀檢索、由 AI Agent 協助編譯與維護。

> [!CAUTION] 臨床使用聲明
> 本知識庫僅供專業醫學文獻整理、查房參考與學術追蹤，**不得替代床邊臨床判斷、病患個體化評估或院內標準作業規範（SOP）**。請勿於本資料夾存入任何病患可識別個資（PHI）。

---

## 快速開始

### 1. 用 Obsidian 開啟
1. 打開 Obsidian → **Open folder as vault** → 選擇本資料夾（`/Users/wuyingzhang/Downloads/wiki`）。
2. 從 `wiki/overview.md` 或 `index.md` 開始瀏覽；可使用 Graph View、Tags 與 Properties 篩選各臨床領域與試驗。

### 2. 放入原始文獻（`raw/`）
- 期刊論文 PDF（RCT、Meta-analysis、Review）→ 放入 `raw/papers/`
- 臨床指引 PDF（AHA/ASA、ESO、台灣腦中風學會指引）→ 放入 `raw/guidelines/`
- 建議檔名保持好辨識（例如 `SELECT2_NEJM_2023.pdf`、`AHA_ASA_AIS_2026.pdf`）。`raw/` 內檔案為**唯讀**，Agent 不會修改或刪除原檔。

---

## 常用 AI 指令範例

### 1. 吸收單篇論文（預設主力，最高精準度）
> 「請依照 AGENTS.md 執行單篇 Ingest：`raw/papers/SELECT2_NEJM_2023.pdf`。」

### 2. 吸收大型臨床指引（強制一次一篇，可分章節）
> 「請依照 AGENTS.md 單篇 Ingest `raw/guidelines/AHA_ASA_AIS_2026.pdf`，先處理『靜脈溶栓 IVT』與『機械取栓 EVT』兩個章節。」

### 3. 兩階段小批次匯入（建議每批 3–5 篇同主題論文）
> 「請依照 AGENTS.md 的兩階段小批次模式，批次 Ingest `raw/papers/` 裡這 4 篇大梗塞核心取栓 RCT，先完成階段一逐篇建頁，再提出整合更新計畫給我確認。」

### 4. 查房／臨床快速查詢（預設唯讀不改檔）
> 「查詢：發病 4.5–9 小時的 AIS 病患，目前庫內指引與試驗對 IVT（Alteplase / Tenecteplase）的影像篩選條件與劑量建議是什麼？AHA/ASA、ESO 跟台灣指引有差異嗎？」

### 5. 定期知識庫健檢（Lint）
> 「請依照 AGENTS.md 執行一次完整的 Lint 健檢，列出過時指引、證據衝突、缺漏欄位、死連結，以及 `raw/` 裡還沒收錄的檔案。」

---

## 資料夾一覽

| 路徑 | 用途 | 編輯權限 |
| :--- | :--- | :--- |
| `AGENTS.md` | AI Agent 完整運作規則、臨床護欄與 Ingest/Query/Lint 規範 | 人類／共同維護 |
| `index.md` | 全庫頁面目錄索引（單行摘要） | Agent 維護 |
| `log.md` | 唯追加操作紀錄 | Agent 維護 |
| `raw/papers/` | 原始英文論文 PDF | 人類放入（Agent 唯讀） |
| `raw/guidelines/` | 原始臨床指引 PDF | 人類放入（Agent 唯讀） |
| `raw/assets/` | 擷取圖表與靜態資源 | 唯讀／經同意存入 |
| `wiki/overview.md` | 四大領域主入口導覽頁（MOC） | 確認後由 Agent 更新 |
| `wiki/topics/` | 臨床處置主題頁（頂部速查結論＋完整證據） | 確認後由 Agent 更新 |
| `wiki/trials/` | 關鍵試驗與論文結構化摘要 | Agent 可直接生成 |
| `wiki/guidelines/` | 臨床指引彙整與版本對照 | Agent 可直接生成 |
| `wiki/interventions/` | 藥物與介入處置快查頁 | 確認後由 Agent 更新 |
| `wiki/comparisons/` | 臨床爭議與跨文獻比較頁 | 確認後由 Agent 更新 |
| `templates/` | 五種標準 Markdown 頁面模板 | 人類／共同維護 |
