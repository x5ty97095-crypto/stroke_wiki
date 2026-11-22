---
title: "<試驗縮寫或第一作者 (YYYY)> — <簡短中文標題>"
type: trial
domain:
  - "<ais | ich | sah | secondary-prevention | inpatient-care | general>"
study_design: "<RCT | Cluster-RCT | Meta-analysis | Cohort | Systematic Review>"
year: YYYY
journal: "<期刊縮寫，如 NEJM / Lancet / JAMA / Stroke>"
nct: "<NCTxxxxxxxx 或 [原文未報告]>"
sample_size: 0
status: active
source_file: "raw/papers/<原始檔名.pdf>"
last_updated: YYYY-MM-DD
aliases:
  - "<試驗縮寫>"
  - "<試驗縮寫 YYYY>"
tags:
  - stroke/trial
  - stroke/<domain>
---

# <試驗縮寫或第一作者 (YYYY)>：<簡短中文標題>

> [!tip] 一句話臨床結論（Take-home Message）
> <針對什麼族群、比較什麼處置、主要療效與安全結果為何，對臨床決策有何影響？>

---

## 1. 基本資料與研究設計
- **完整文獻標題**：<原文標題>
- **期刊與年份**：<Journal, YYYY; Vol(Issue): Pages；DOI>
- **研究設計**：<多中心／雙盲或開放標籤 PROBE／優效性或非劣性試驗／停招原因等>
- **收案期間與地區**：<年份、國家／中心數>
- **樣本數（N）**：總計 `N = `（介入組 `n = ` vs 對照組 `n = `）
- **追蹤時間**：<如 90 天>
- **原始檔案**：`raw/papers/<原始檔名.pdf>`

---

## 2. PICO 結構化摘要
- **P（Population，對象）**：<疾病類型、時間窗、NIHSS、ASPECTS／核心體積／灌流影像條件>
- **I（Intervention，介入）**：<藥物名稱、精確劑量與給藥途徑／介入方式>
- **C（Comparator，對照）**：<安慰劑／標準治療／對照藥物與劑量>
- **O（Outcomes，指標）**：
  - **主要療效指標**：<明確定義與評估時間點>
  - **主要安全指標**：<明確定義，特別標註 sICH 採用的定義標準如 ECASS III / SITS-MOST / Heidelberg>

---

## 3. 關鍵收案與排除條件（Eligibility Criteria）
### 收案條件（Inclusion）
- **時間窗**：<如 Last known well 至治療 4.5–9 小時>
- **臨床嚴重度**：<如 NIHSS 範圍、發病前 mRS 門檻>
- **影像條件**：<如 ASPECTS 範圍、CT/MR Perfusion core/penumbra 閾值、血管阻塞位置>
- **其他條件**：<年齡或其他關鍵條件>

### 關鍵排除條件（Exclusion）
- <逐條列出對臨床選案最重要的排除條件；若原文省略詳列請註明 `[原文未報告]` 或引用附錄>

---

## 4. 核心研究結果

### 4.1 療效指標（Efficacy Outcomes）
| 指標項目 | 介入組（n= ） | 對照組（n= ） | 效應值（OR / RR / HR / RD） | 95% CI | p 值 | NNT | 來源表／頁 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **主要指標**：<指標名> | xx.x% (x/n) | xx.x% (x/n) | <數值> | <區間> | <p 值> | <數值或 `[原文未報告]`> | Table X |
| **次要指標**：<如 mRS 0–1 / 0–2 / shift> | xx.x% (x/n) | xx.x% (x/n) | <數值> | <區間> | <p 值> | <數值或 `[原文未報告]`> | Table X |

### 4.2 安全性指標（Safety Outcomes）
| 安全指標（註明定義） | 介入組（n= ） | 對照組（n= ） | 效應值（OR / RR / RD） | 95% CI | p 值 | NNH | 來源表／頁 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **sICH**（定義：<如 ECASS III>） | xx.x% (x/n) | xx.x% (x/n) | <數值> | <區間> | <p 值> | <數值或 `[原文未報告]`> | Table X |
| **90-day 死亡率** | xx.x% (x/n) | xx.x% (x/n) | <數值> | <區間> | <p 值> | <數值或 `[原文未報告]`> | Table X |
| **其他重大不良事件** | xx.x% (x/n) | xx.x% (x/n) | <數值> | <區間> | <p 值> | <數值或 `[原文未報告]`> | Table X |

### 4.3 關鍵亞組分析（Subgroup Highlights）
- <列出具有臨床意義的亞組結果與交互作用 p 值（$p_{\text{interaction}}$）；無特殊異質性亦簡要說明>

---

## 5. 研究限制與臨床判讀（Critical Appraisal）
> [!warning] 限制與外推性提醒
> - **方法學限制**：<如提前終止、開放標籤、高交叉率、樣本數不足、高比率合併使用其他治療等>
> - **臨床外推限制**：<族群代表性、亞洲族群比例、影像設備需求等>

---

## 6. 與現行指引及其他試驗的關聯
- **相關臨床主題**：<`[[topic-slug|主題名]]`>
- **相關藥物／介入**：<`[[intervention-slug|藥物或處置名]]`>
- **相關指引與比較**：<`[[guideline-slug|指引名]]`、`[[comparison-slug|比較頁]]`>
- **是否挑戰既有建議**：<說明是否與現有庫內指引或試驗存在分歧>
