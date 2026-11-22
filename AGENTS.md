# AGENTS.md — 腦中風臨床處置 LLM Wiki 運作規則

本知識庫採用 Andrej Karpathy 的 **LLM Wiki** 架構模式：由人類負責提供原始文獻與把關臨床處置變更，由 AI Agent 負責將原始文獻持續「編譯」成結構化、可交叉比對的 Obsidian Markdown 知識網，而非每次查詢都重新檢索零散段落。

> [!CAUTION] 臨床免責聲明
> 本知識庫僅供醫療專業人員進行**醫學文獻整理、證據追蹤與查房快速參考**，**不得替代床邊臨床判斷、病患個體化評估或所屬醫院之標準作業規範（SOP）**。任何處方劑量與處置決策，請務必對照最新官方指引與院內規範核實。

---

## 1. 核心定位與涵蓋範疇

- **主要使用場景**：臨床實務與查房快速參考（優先提供指引建議、時間窗、劑量、收案/排除條件與關鍵試驗數據）。
- **涵蓋臨床領域（`domain` 代碼）**：
  - `ais`：急性缺血性中風（IVT 溶栓、EVT 取栓、影像篩選、急性血壓與抗血栓處置）
  - `ich`：自發性腦出血（血壓控制、抗凝劑反轉、止血、手術與微創引流適應症）
  - `sah`：蜘蛛膜下腔出血（動脈瘤處置、血管痙攣/遲發性缺血預防、水腦與重症處置）
  - `secondary-prevention`：TIA 與次級預防（DAPT、心房顫動抗凝啟用時機、頸動脈狹窄、PFO、血脂與血壓控制）
  - `inpatient-care`：中風病房照護與併發症（惡性腦水腫、出血轉化、吞嚥評估、感染與 DVT 預防、早期復健）
  - `general`：跨領域通用主題（如中風量表、影像判讀、共同指引原則）
- **主要原始來源**：英文期刊論文 PDF（大型 RCT、Meta-analysis、Systematic Review）與臨床指引 PDF（AHA/ASA、ESO、台灣腦中風學會指引）。

---

## 2. 臨床安全護欄（不可違反的硬性原則）

1. **零幻覺原則（Zero Hallucination）**：
   - 嚴禁憑記憶補充、推測或杜撰任何劑量、時間窗、影像閾值、收案/排除條件、統計數字（mRS、sICH、死亡率、OR/RR/HR、95% CI、p 值、NNT/NNH）或證據等級（COR/LOE）。
   - 若原始文獻未提供某項必備欄位，一律明標 **`[原文未報告]`**；若需查核附錄或待確認頁碼，標註 **`[待查證]`**。
2. **逐條出處與年份**：
   - 每一條臨床建議與關鍵數據皆必須附上來源連結與發表年份，例：`[[extend-2019|EXTEND (2019)]]`、`[[aha-asa-ais-2026|AHA/ASA AIS (2026)]]`；關鍵數據建議同時加註章節或表格來源（如 `Table 2`、`Sec 4.2`）。
3. **矛盾與版本演變顯性化**：
   - **禁止靜默覆蓋**不同指引之間的分歧（例如 AHA/ASA vs ESO vs 台灣腦中風學會指引），或新試驗挑戰舊指引之處。
   - 遇到任何分歧或證據衝突，必須以 Obsidian Callout（`> [!warning] 指引／證據分歧` 或 `> [!danger] 證據衝突／待確認`）明確並列各方說法、年份與依據。
   - 舊版指引被新版取代時，**不得刪除舊頁**；須將舊頁 frontmatter 改為 `status: superseded` 並填入 `superseded_by: "[[新指引檔名]]"`。
4. **零病患個資原則（No PHI）**：
   - 嚴禁於任何 `wiki/`、`index.md`、`log.md` 或檔案中寫入任何可識別病患身份的資訊（姓名、病歷號、身分證字號、生日、確切就診/住院日期等）。
   - 若在 `raw/` 中偵測到疑似 PHI，必須立即停止處理並提醒使用者先行去識別化或移除檔案。
5. **`raw/` 嚴格唯讀**：
   - `raw/` 為不可變原始文獻層。Agent **絕對不可修改、重新命名、移動或刪除** `raw/` 內的任何檔案（僅允許讀取；若需擷取圖表檔案，須經使用者同意後存於 `raw/assets/`）。

---

## 3. 專案資料夾架構

```text
.
├── AGENTS.md                 # 本規則檔（Schema & Governance Layer）
├── README.md                 # 人類操作說明與常用指令範例
├── index.md                  # 全庫頁面目錄索引（單行摘要與分類）
├── log.md                    # 唯追加（append-only）操作日誌
├── raw/                      # 【唯讀】原始文獻層
│   ├── papers/               # 英文期刊論文 PDF（RCT、Meta-analysis、Review）
│   ├── guidelines/           # 臨床指引 PDF（AHA/ASA、ESO、台灣腦中風學會等）
│   └── assets/               # 靜態附件與擷取圖表
├── wiki/                     # 【編譯層】Agent 維護的雙向連結知識網
│   ├── overview.md           # 四大領域主入口導覽頁（MOC）
│   ├── topics/               # 臨床處置主題頁（頂部速查結論＋完整證據）
│   ├── trials/               # 關鍵試驗／論文結構化摘要頁
│   ├── guidelines/           # 臨床指引彙整與版本對照頁
│   ├── interventions/        # 藥物與介入處置快查頁（劑量、禁忌症、監測）
│   └── comparisons/          # 臨床爭議與跨試驗／跨指引比較頁
└── templates/                # 五種標準頁面模板（撰寫新頁時必須參照）
    ├── topic.md
    ├── trial.md
    ├── guideline.md
    ├── intervention.md
    └── comparison.md
```

---

## 4. 語言、檔名與 Obsidian 格式規範

### 4.1 語言風格
- 內文以**繁體中文**為主，保留英文醫學專有名詞與國際標準縮寫（如 `AIS`、`ICH`、`SAH`、`TIA`、`IVT`、`EVT`、`LVO`、`NIHSS`、`ASPECTS`、`mRS`、`sICH`、`DAPT`、`DOAC`、`COR`、`LOE`、`NNT`、`NNH`）。
- 查房友善原則：`topics/` 與 `interventions/` 頁面頂部必放精簡的「**臨床速查結論（Bottom Line）**」，下方再展開完整證據表格、納入排除條件與出處引用。

### 4.2 檔案命名（一律英文 `kebab-case`）
- 全部小寫英文字母、數字與連字號 `-`，不使用空格或中文檔名：
  - `wiki/topics/`：`<domain>-<topic>.md`（例：`ais-ivt-thrombolysis.md`、`ich-anticoagulation-reversal.md`、`sp-af-anticoagulation-timing.md`）
  - `wiki/trials/`：`<acronym-or-firstauthor>-<year>.md`（例：`extend-2019.md`、`select2-2023.md`、`interact3-2023.md`）
  - `wiki/guidelines/`：`<org>-<topic>-<year>.md`（例：`aha-asa-ais-2026.md`、`eso-ivt-2021.md`、`tsgs-ais-2024.md`）
  - `wiki/interventions/`：`<drug-or-procedure>.md`（例：`tenecteplase.md`、`alteplase.md`、`four-factor-pcc.md`、`mechanical-thrombectomy.md`）
  - `wiki/comparisons/`：`<option-a>-vs-<option-b>.md`（例：`tnk-vs-alteplase-ais.md`、`early-vs-late-doac-af-stroke.md`）

### 4.3 Obsidian 語法與 Frontmatter
- **內部連結**：統一使用 Obsidian wikilink 並帶中文或可讀別名：`[[檔名不含副檔名|顯示名稱]]`（例：`[[select2-2023|SELECT2 (2023)]]`）。
- **禁止死連結**：除非該頁面已存在或將於本次確認後一併建立，否則不得建立指向不存在檔案的 `[[wikilink]]`；若僅暫時提及未來主題，以純文字加註`（待建頁）`。
- **YAML Frontmatter**：所有 `wiki/` 頁面皆須包含對應 `templates/*.md` 所定義的 YAML frontmatter（至少包含 `title`、`type`、`domain`、`status`、`last_updated`、`aliases`、`tags`）。
- **Obsidian Callout 語義**：
  - `> [!tip] 臨床速查結論（Bottom Line）`：查房 10 秒可讀完的核心處置重點
  - `> [!info]`：時間窗、劑量速查、檢核條件
  - `> [!warning]`：指引間差異（AHA/ASA vs ESO vs 台灣指引）、研究限制、臨床注意事項
  - `> [!danger]`：絕對禁忌症、重大出血風險、或新舊證據重大衝突

---

## 5. 臨床證據必備萃取標準

撰寫各類頁面時，必須嚴格套用 `templates/` 內對應模板，並確保以下臨床核心項目完整記錄（原文缺漏者標記 `[原文未報告]`）：

- **`trials/`（RCT / Meta-analysis / Review）**：
  - 研究設計、期刊與發表年份、註冊號（如 NCT）
  - 完整 **PICO**（Population、Intervention、Comparator、Outcomes）
  - **收案與排除條件**（特別記錄發病時間窗、NIHSS、ASPECTS、梗塞核心體積、血壓門檻、抗凝狀態等）
  - 樣本數（總數與各組人數）與追蹤時間
  - **主要療效指標**（如 90-day mRS 0–2、mRS ordinal shift，附絕對百分比、Effect size、95% CI、p 值、NNT）
  - **關鍵安全性指標**（sICH 採用的定義如 ECASS III / SITS-MOST / Heidelberg 與發生率、90-day 死亡率、NNH）
  - 重要亞組分析、研究限制與臨床實務意義
- **`guidelines/`（臨床指引）**：
  - 發布機構（AHA/ASA、ESO、台灣腦中風學會等）、年份、涵蓋範圍、取代之舊版指引
  - 核心建議清單表（臨床情境 / 建議內容 / COR / LOE / 關鍵支撐試驗 / 備註）
  - 與其他主要指引之差異比較（含台灣指引或健保給付條件差異，**僅記錄原文有載明者**）
- **`topics/`（臨床處置主題頁）**：
  - 頂部「臨床速查結論（Bottom Line）」
  - 時間窗與評估／處置決策表（必要時附 Mermaid 流程圖）
  - **多方指引對照表**（AHA/ASA vs ESO vs 台灣腦中風學會）
  - 關鍵支撐試驗彙整表與臨床爭議／未解問題
- **`interventions/`（藥物與介入處置快查頁）**：
  - 頂部速查（核准適應症、標準劑量與給藥方式、最大劑量、時間窗）
  - 絕對與相對禁忌症
  - 給藥前後監測（如血壓上限、神經學評估頻率）與併發症處置（如 sICH、血管性水腫）
  - 支撐試驗與相關指引連結
- **`comparisons/`（臨床爭議與比較分析頁）**：
  - 明確臨床問題、各方選項/試驗/指引之正面對照表、證據強度評估、現階段臨床實務建議與適用情境區分

---

## 6. 三大核心操作流程（Ingest / Query / Lint）

### 6.1 `Ingest`（吸收新文獻）—— 半自動把關＋雙模式支援

#### 通用原則
- **預設為「模式 A：一次一篇」**，確保高嚴謹度數據萃取品質。
- **大型臨床指引 PDF**（如 AHA/ASA、ESO、台灣腦中風學會全文指引）**強制採用模式 A（一次一篇）**；若篇幅超過 40 頁，主動建議使用者依臨床章節分次 Ingest。
- **模式 B（兩階段小批次）**僅用於期刊論文（RCT、Meta-analysis、Review），**建議每批 3–5 篇**；若使用者一次要求超過 5 篇，先提醒切分為每批 3–5 篇分批執行，避免上下文過長導致數字遺漏或混雜。
- **半自動把關規則（兩模式皆適用）**：
  - 單篇文獻編譯頁（`wiki/trials/*.md`、`wiki/guidelines/*.md`）與對應之 `index.md` / `log.md` 紀錄可**直接建立**。
  - 凡涉及修改或新增臨床處置頁（`wiki/topics/*.md`、`wiki/interventions/*.md`、`wiki/comparisons/*.md`、`wiki/overview.md`），或將舊指引標為 `superseded`，或處理指引／試驗間衝突時，**必須先輸出「整合更新計畫」待使用者明確確認後再寫入**。

#### 模式 A：一次一篇（Single-Paper Ingest）
1. **前置檢查**：確認 `raw/` 指定檔案路徑存在、無疑似 PHI；讀取 `index.md` 了解現有頁面與命名，避免重複建頁。
2. **精讀與編譯文獻頁**：
   - 完整閱讀原始檔，嚴格依 `templates/trial.md` 或 `templates/guideline.md` 建立 `wiki/trials/<slug>.md` 或 `wiki/guidelines/<slug>.md`。
   - 核對每一項數據（人數、時間窗、劑量、mRS、sICH、死亡率、COR/LOE），原文未載者填 `[原文未報告]`。
3. **初步登錄索引與日誌**：
   - 將新建的文獻頁加入 `index.md`。
   - 在 `log.md` 追加一筆 `ingest` 紀錄（註明文獻頁已建立，跨頁整合待確認）。
4. **【半自動把關暫停點】提交「整合更新計畫」**：
   - 向使用者簡要回報：
     - 已建立的文獻頁路徑與核心摘要（Bottom Line + 關鍵數字）
     - 建議新增或修改的 `wiki/topics/`、`wiki/interventions/`、`wiki/comparisons/`、`wiki/overview.md` 清單與預計修改重點
     - 是否偵測到**指引分歧、版本取代或試驗矛盾**（若有，明確列出新舊數據對照）
   - 詢問使用者是否確認執行上述跨頁整合（或微調）。
5. **確認後整合**：獲使用者確認後，執行相關頁面更新、補齊雙向 `[[wikilinks]]`、更新 `index.md` 與 `log.md`。

#### 模式 B：兩階段小批次（Batch Ingest，每批 3–5 篇論文）
1. **盤點與分批檢查**：列出本次待處理的 3–5 篇論文檔名並確認皆無 PHI；讀取 `index.md`。
2. **階段一（逐篇獨立萃取）**：
   - 嚴格「逐篇」讀取與撰寫，每篇獨立生成對應的 `wiki/trials/<slug>.md`，完成一篇核對一篇，**嚴禁跨篇混雜數據**。
   - 將本批所有新建的 `wiki/trials/` 頁面登入 `index.md`，並於 `log.md` 追加一筆 `ingest-batch` 階段一紀錄。
3. **【半自動把關暫停點】階段二（單一整合更新計畫）**：
   - 彙整整批論文的共通結論與差異，提出**一份整合更新計畫**：
     - 預計建立或更新的 `wiki/topics/` 與 `wiki/interventions/` 頁面與具體變更
     - 建議新建或更新的 `wiki/comparisons/` 比較頁（例如同主題多篇 RCT 的橫向比較表）
     - 偵測到的跨試驗或與既有指引的衝突點
   - 待使用者**一次確認**後，統一執行所有跨頁更新並於 `log.md` 記錄階段二完成。

---

### 6.2 `Query`（臨床查詢與知識檢索）

1. **先讀索引再讀內文**：先查閱 `index.md`（及必要時 `wiki/overview.md`），找出最相關的 `topics/`、`interventions/`、`guidelines/`、`comparisons/` 與 `trials/` 頁面閱讀。
2. **預設唯讀不改檔**：回答查詢時，**不自動建立或修改任何檔案**。
3. **查房友善回答格式**：
   - 第一段先給**臨床重點結論（Bottom Line）**（直接回答時間窗、劑量、條件或處置建議）。
   - 接著提供結構化細節與證據出處（附 `[[wikilinks]]`、年份、COR/LOE 或關鍵試驗數據）。
   - 若存在不同指引差異（AHA/ASA vs ESO vs 台灣指引）或試驗矛盾，明確標出提醒。
   - 若知識庫目前尚未收錄相關文獻，誠實說明「**目前知識庫尚未收錄此主題文獻**」，切勿以訓練記憶偽裝成庫內資料；若需要補充一般背景知識，必須明確區隔標註「以下非出自本庫收錄文獻」。
4. **選擇性寫回（File Back）**：
   - 若本次查詢產出了高價值的跨文獻綜合比較、臨床決策對照或教學整理，在回覆末尾主動詢問：
     > 「這份比較整理具有重複查閱價值，是否要寫回 `wiki/comparisons/<建議檔名>.md`，並同步更新 `index.md` 與 `log.md`？」
   - 僅在使用者同意後才寫入檔案。

---

### 6.3 `Lint`（定期維護與品質健檢）

當使用者下令執行 `Lint`（或健康檢查）時，全面掃描 `raw/`、`wiki/`、`index.md` 與 `log.md`，產出**健檢報告**（先報告再依使用者指示修復，或針對明確的技術錯誤如 `index.md` 漏登詢問是否一併自動修正）：

1. **臨床內容面檢查**：
   - **指引版本過時**：是否已收錄新版指引，但舊版仍標為 `status: active`？是否有 `topics/` 或 `interventions/` 仍將已取代建議列為現行標準？
   - **未解決之矛盾與衝突**：跨指引或跨試驗間是否有明顯數據或建議衝突卻未在 `topics/` 或 `comparisons/` 標示？
   - **必備臨床欄位缺漏**：檢查 `trials/` 是否遺漏 PICO、時間窗、樣本數、mRS、sICH、死亡率；`interventions/` 是否遺漏劑量或禁忌症（區分合理之 `[原文未報告]` 與漏填空白）。
2. **技術與圖譜結構檢查**：
   - **死連結（Broken Links）**：檢查所有 `[[wikilinks]]` 是否指向實際存在的檔案。
   - **孤立頁面（Orphan Pages）**：檢查是否有 `wiki/` 頁面未從任何其他頁面（含 `overview.md` 與 `topics/`）連入。
   - **`index.md` 同步性**：所有 `wiki/` 檔案是否皆已收錄於 `index.md`？是否有已刪除的殘留條目？
   - **`raw/` 未收錄清單**：列出 `raw/papers/` 與 `raw/guidelines/` 中尚未建立對應 `wiki/` 頁面的原始檔案。
   - **格式合規性**：檔名是否符合 `kebab-case`？YAML frontmatter 必填欄位是否齊全？
3. **日誌紀錄**：每次執行 `Lint` 後，於 `log.md` 追加一筆 `lint` 紀錄。

---

## 7. `index.md` 與 `log.md` 維護規範

- **`index.md`**：每次新增、刪除或更名 `wiki/` 頁面時必須同步更新。每筆條目包含 `[[wikilink|顯示名稱]]`、領域標籤、狀態與一句話精準摘要，確保 Agent 讀取 `index.md` 即可掌握全庫版圖。
- **`log.md`**：採**唯追加（append-only）**原則，永遠在檔案最末端新增紀錄，不改寫歷史紀錄。標題行嚴格遵循以下格式（方便指令列以 `grep "^## \[" log.md` 檢索）：

```markdown
## [YYYY-MM-DD] <operation> | <簡短標題>
- **來源／對象**：<相關 raw/ 或 wiki/ 檔案>
- **動作摘要**：<建立、更新或檢查之具體項目>
- **備註／待確認**：<衝突提醒、半自動把關狀態或後續行動>
```

其中 `<operation>` 統一使用：`init`、`ingest`、`ingest-batch`、`integrate`、`query-fileback`、`lint`。
