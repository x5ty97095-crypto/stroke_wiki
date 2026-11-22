# 操作日誌（Log）

> 本檔案為**唯追加（append-only）**紀錄，按時間順序記錄每次 `init`、`ingest`、`ingest-batch`、`integrate`、`query-fileback` 與 `lint` 操作。禁止修改或刪除既有歷史紀錄。

---

## [2026-11-22] init | 建立腦中風臨床處置 LLM Wiki 初始架構
- **來源／對象**：`AGENTS.md`、`README.md`、`index.md`、`log.md`、`wiki/overview.md`、`templates/*.md`、`raw/` 與 `wiki/` 目錄結構
- **動作摘要**：依需求訪談結果完成初始資料夾、高嚴謹臨床規則、Obsidian 最佳化模板（Topic / Trial / Guideline / Intervention / Comparison）與空白導覽骨架建置。
- **備註／待確認**：已設定半自動把關與雙模式 Ingest（預設一次一篇；支援 3–5 篇兩階段小批次；大型指引強制一次一篇）。等待放入首批 `raw/` 文獻。

## [2026-11-22] ingest | AHA/ASA 2026 AIS 臨床指引（區塊 A：總覽、影像 3.2、IVT 4.6、EVT 4.7）
- **來源／對象**：`raw/guidelines/prabhakaran-et-al-2026-2026-guideline-...pdf`、`raw/guidelines/prabhakaran-et-al-2026-correction-...pdf` → `wiki/guidelines/aha-asa-ais-2026.md`、`index.md`
- **動作摘要**：建立 `wiki/guidelines/aha-asa-ais-2026.md`（`status: partial`），完整收錄 Top 10 Take-Home、What Is New、Table 2 分級、Sec 3.2（含 Table 3）、Sec 4.6（含 Tables 4–8）與 Sec 4.7（含大核心、BAO、MeVO、輔助技術與兒童 EVT），並核對 2026/08 勘誤（確認 August 2026 主檔已整合該勘誤）。
- **備註／待確認**：跨頁整合計畫（`topics/`、`interventions/`、`overview.md`）已提交待使用者確認；其餘章節（區塊 B/C/D）待後續分批收錄。

## [2026-11-22] integrate | 完成 AHA/ASA 2026 AIS 區塊 A 跨頁臨床整合（IVT / EVT / TNK / Alteplase）
- **來源／對象**：`wiki/guidelines/aha-asa-ais-2026.md` → `wiki/topics/ais-ivt-thrombolysis.md`、`wiki/topics/ais-evt-thrombectomy.md`、`wiki/interventions/tenecteplase.md`、`wiki/interventions/alteplase.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建 IVT 與 EVT 兩篇臨床處置主題頁及 Tenecteplase 與 Alteplase 兩篇藥物快查頁，補齊雙向 Obsidian `[[wikilinks]]` 並更新 `overview.md` 與 `index.md`。
- **備註／待確認**：`aha-asa-ais-2026.md` 尚餘區塊 B/C/D 待分次 Ingest；ESO 與台灣腦中風學會指引待後續收錄後補入跨指引對照表。

## [2026-11-22] ingest | AHA/ASA 2026 AIS 臨床指引（區塊 B：Sec 4.1–4.5 支持/血壓/血糖 ＋ Sec 4.8–4.12 抗血小板/抗凝/緊急頸動脈）
- **來源／對象**：`raw/guidelines/prabhakaran-et-al-2026-2026-guideline-...pdf`、`raw/guidelines/prabhakaran-et-al-2026-correction-...pdf` → `wiki/guidelines/aha-asa-ais-2026.md`、`index.md`
- **動作摘要**：於 `aha-asa-ais-2026.md` 補入區塊 B 全部建議與數據（Sec 4.1 氧氣/NBO、4.2 擺位、4.3 血壓 [IVT/EVT 後禁止積極降壓 <140]、4.4 體溫、4.5 血糖 [禁止 80–130]、4.8 抗血小板與 Figure 4/Table 9 五大 DAPT 試驗、4.9 抗凝/早期 DOAC、4.10–4.12 血流動力/神經保護/緊急 CEA 調降 COR 3），並核對勘誤 #9（TRUTH study）與 #21（Figure 4 ABCD2 ≥4）。
- **備註／待確認**：區塊 B 跨頁整合更新計畫已提交待使用者確認；尚餘區塊 C（Sec 5–6）與區塊 D（Sec 2, 3.1, 3.3）待收錄。

## [2026-11-22] integrate | 完成 AHA/ASA 2026 AIS 區塊 B 跨頁臨床整合（血壓/血糖/支持、抗血小板/DAPT、AF 抗凝時機）
- **來源／對象**：`wiki/guidelines/aha-asa-ais-2026.md` → `wiki/topics/ais-bp-glucose-supportive.md`、`wiki/topics/ais-antithrombotic-dapt.md`、`wiki/topics/sp-af-anticoagulation-timing.md`、`wiki/topics/ais-ivt-thrombolysis.md`、`wiki/topics/ais-evt-thrombectomy.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建 3 篇臨床主題頁（含 Figure 4 DAPT Mermaid 流程圖與 Table 9 劑量/NNT 總表），更新 IVT/EVT 主題頁血壓與併用抗血栓細則，補齊所有雙向 `[[wikilinks]]` 與索引。
- **備註／待確認**：`aha-asa-ais-2026.md` 尚餘區塊 C（Sec 5–6）與區塊 D（Sec 2, 3.1, 3.3）待收錄。

## [2026-11-22] ingest | AHA/ASA 2026 AIS 臨床指引（區塊 C：Sec 5 住院支持照護 ＋ Sec 6 惡性腦水腫／開顱手術／癲癇）
- **來源／對象**：`raw/guidelines/prabhakaran-et-al-2026-2026-guideline-...pdf`、`raw/guidelines/prabhakaran-et-al-2026-correction-...pdf` → `wiki/guidelines/aha-asa-ais-2026.md`、`index.md`
- **動作摘要**：於 `aha-asa-ais-2026.md` 補入區塊 C 全數建議與數據（Sec 5.1–5.7 Stroke Unit、吞嚥/FEES/VFSS/PES、營養 FOOD 1–3、DVT CLOTS/PREVAIL、PSD、抗生素/導尿管禁忌、AVERT/SSRI；Sec 6.1–6.5 惡性腦水腫內外科處置、CHARM Glibenclamide 陰性、≤60 vs >60 歲減壓開顱、小腦梗塞 EVD/≥35 mL 枕下減壓、癲癇），並核對勘誤 #22–#26（確認非氣切 PES 已下修為 COR 2b，並標註前頁 e320 摘要表殘留舊字樣之差異）。
- **備註／待確認**：區塊 C 跨頁整合計畫已提交待使用者確認；僅剩區塊 D（Sec 2, 3.1, 3.3）即可完成本指引全文 100% 收錄。

## [2026-11-22] integrate | 完成 AHA/ASA 2026 AIS 區塊 C 跨頁臨床整合（中風病房照護、惡性腦水腫與癲癇）
- **來源／對象**：`wiki/guidelines/aha-asa-ais-2026.md` → `wiki/topics/inpatient-stroke-unit-care.md`、`wiki/topics/inpatient-malignant-edema-seizures.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建 2 篇住院照護與急性併發症主題頁，補齊雙向 Obsidian `[[wikilinks]]` 與總覽索引。
- **備註／待確認**：`aha-asa-ais-2026.md` 僅餘區塊 D（Sec 2, 3.1, 3.3）即可達成全文 100% 收錄並將狀態升為 `active`。

## [2026-11-22] ingest | AHA/ASA 2026 AIS 臨床指引（區塊 D：Sec 2 院前與中風體系 ＋ Sec 3.1/3.3 量表與檢驗 — 全文 100% 完成）
- **來源／對象**：`raw/guidelines/prabhakaran-et-al-2026-2026-guideline-...pdf`、`raw/guidelines/prabhakaran-et-al-2026-correction-...pdf` → `wiki/guidelines/aha-asa-ais-2026.md`、`index.md`
- **動作摘要**：於 `aha-asa-ais-2026.md` 補入最後區塊 D（Sec 2.1–2.10 民眾衛教、EMS 品管、院前量表/提前通知、禁院前 GTN/RIC/現場降壓 130–140、EMS 轉送目的地/RACECAT、DIDO ≤120 min、MSU、醫院認證、急診團隊、遠距醫療、EVT 品管與認證、NIHSS/ECG/Troponin），核對勘誤 #3–#4，並將指引頁正式升格為 `status: active`（100% 全文收錄）。
- **備註／待確認**：區塊 D 跨頁整合計畫（新建院前/急診體系主題頁與更新 `overview.md` 狀態）已提交待使用者確認。

## [2026-11-22] integrate | 完成 AHA/ASA 2026 AIS 區塊 D 跨頁整合與全指引收尾（院前/急診體系）
- **來源／對象**：`wiki/guidelines/aha-asa-ais-2026.md` → `wiki/topics/ais-prehospital-ed-systems.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建 `wiki/topics/ais-prehospital-ed-systems.md`，更新 `overview.md` 與 `index.md` 將 `aha-asa-ais-2026` 標記為 `active`（100% 全文收錄），並補齊全庫雙向連結。
- **備註／待確認**：`raw/guidelines/` 內現有兩份 2026 AHA/ASA AIS 檔案已全數編譯與整合完成。
