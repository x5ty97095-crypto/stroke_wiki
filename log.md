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

## [2026-11-22] ingest | 台灣腦中風學會 2025 急性缺血性腦中風靜脈血栓溶解治療指引更新（全文）
- **來源／對象**：`raw/guidelines/2025台灣腦中風學會急性缺血性腦中風靜脈血栓溶解治療指引更新.pdf` → `wiki/guidelines/tsgs-ivt-2025.md`、`index.md`
- **動作摘要**：完整精讀正文 38 頁（Ch 1–12，含總表一至四、表 2.1、表 9.1–9.2、表 10.1–10.4 與醫療法律章節）並建立 `tsgs-ivt-2025.md`（`status: active`），完整盤點與 `aha-asa-ais-2026.md` 間之 10 項核心臨床與健保/仿單分歧。
- **備註／待確認**：因偵測到多項美台指引實質分歧（輕型非失能中風、0.6 mg/kg 低劑量、DOAC <24h Xa 抑制劑、手術/TBI/動脈瘤時間與大小門檻、ARIA、Epinephrine IM vs SC、sICH Fibrinogen 目標、IVT 後早期抗血小板），已依半自動把關提交整合更新計畫待使用者確認；其餘 2 份台灣指引（2023 EVT、2020 院前/急診）待後續單篇依序 Ingest。

## [2026-11-23] integrate | 完成 2025 台灣腦中風學會 IVT 指引跨頁整合與美台比較頁建置
- **來源／對象**：`wiki/guidelines/tsgs-ivt-2025.md` → `wiki/comparisons/aha-2026-vs-tsgs-2025-ivt.md`、`wiki/topics/ais-ivt-thrombolysis.md`、`wiki/interventions/alteplase.md`、`wiki/interventions/tenecteplase.md`、`wiki/topics/ais-antithrombotic-dapt.md`、`wiki/guidelines/aha-asa-ais-2026.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建美台 IVT 指引分歧比較頁 `aha-2026-vs-tsgs-2025-ivt.md`，將台灣 2025 IVT 指引、健保給付、0.6 mg/kg 選項、DOAC 分時段規則與禁忌分歧同步整合至既有 IVT／藥物／DAPT 主題頁與 AHA 2026 指引對照欄，補齊全庫雙向連結。
- **備註／待確認**：`raw/guidelines/` 尚餘 2 份台灣指引（2023 EVT、2020 院前/急診）待單篇依序 Ingest。

## [2026-11-23] ingest | 台灣腦中風學會 2023 急性缺血中風動脈內血栓移除治療指引更新（全文）
- **來源／對象**：`raw/guidelines/2023急性缺血性中風動脈內機械取栓治療指引.pdf` → `wiki/guidelines/tsgs-evt-2023.md`、`index.md`
- **動作摘要**：完整精讀正文 15 頁（p.151–165，一至五章，含表一至表六與圖一至圖三）並建立 `tsgs-evt-2023.md`（`status: active`），完整萃取台灣健保 24h EVT 給付背景、術前影像（CTA/CTP/CTA-CS/PC-ASPECTS/PMI）、Bridging 6 RCT、前循環 6–24h 與大核心、後循環 BAO/PCA 與術中麻醉/血壓穩定建議，並盤點與 `aha-asa-ais-2026.md` 間之 6 項核心分歧。
- **備註／待確認**：偵測到**單獨 PCA 阻塞存在實質方向衝突**（TSGS 2023 `COR IIb, B-NR` vs AHA 2026 `COR 3: No Benefit, A`）及前循環大核心、BAO 12–24h、CTA 不等 Creatinine、術中麻醉等推薦強度差異；已依半自動把關暫停，提交跨頁整合更新計畫待使用者確認。尚餘 1 份台灣指引（2020 院前/急診）待後續單篇 Ingest。

## [2026-11-23] integrate | 完成 2023 台灣腦中風學會 EVT 指引跨頁整合與美台 EVT 比較頁建置
- **來源／對象**：`wiki/guidelines/tsgs-evt-2023.md` → `wiki/comparisons/aha-2026-vs-tsgs-2023-evt.md`、`wiki/topics/ais-evt-thrombectomy.md`、`wiki/topics/ais-bp-glucose-supportive.md`、`wiki/guidelines/aha-asa-ais-2026.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建美台 EVT 指引分歧比較頁 `aha-2026-vs-tsgs-2023-evt.md`，將台灣 2023 EVT 指引、健保 24h 給付背景、單獨 PCA 阻塞方向衝突警示（TSGS 2023 `COR IIb` vs AHA 2026 `COR 3: No Benefit`）、大核心／BAO 12–24h／CTA-CS 差異與術中血壓穩定數據（MABP <70 >10 min 或 >90 >45 min）完整整合至既有主題頁、AHA 2026 指引對照欄與總覽索引。
- **備註／待確認**：`raw/guidelines/` 僅餘最後 1 份台灣指引（`2020台灣腦中風學會與台灣急診醫學會急性缺血中風病人的院前緊急處置與急診診斷治療指引.pdf`）待單篇 Ingest。

## [2026-11-23] ingest | 台灣腦中風學會與台灣急診醫學會 2020 急性缺血中風院前與急診診斷治療指引（全文）
- **來源／對象**：`raw/guidelines/2020台灣腦中風學會與台灣急診醫學會急性缺血中風病人的院前緊急處置與急診診斷治療指引.pdf` → `wiki/guidelines/tsgs-tsem-prehospital-ed-2020.md`、`index.md`
- **動作摘要**：完整精讀正文 11 頁（p.257–267，第 1–13 章）並建立 `tsgs-tsem-prehospital-ed-2020.md`（`status: active`），完整收錄台灣 119 EMS 評估與院前通報、衛福部緊急醫療能力分級評定/區域聯防、醫策會認證/TCPI、DTN <60 min、遠距醫療法規報備、IVT 前血糖與不因 CXR 延遲 IVT，並盤點與 `aha-asa-ais-2026.md` 及台灣後續 2023 EVT / 2025 IVT 指引之演變分歧。
- **備註／待確認**：偵測到 EMS 繞道策略（RACECAT）、PSC 建立 CTA/MRA（`COR IIb` vs AHA `COR 1`）、Telestroke 決定 IVT（`COR IIa` vs AHA `COR 1`）、以及台灣內部醒後中風 DWI-FLAIR 推薦演變（2020 `COR IIa` → 2025 `COR IIb`）；已依半自動把關暫停，提交跨頁整合更新計畫待使用者確認。此份完成整合後，`raw/guidelines/` 內現有 5 份指引將達成 **100% 收錄**。

## [2026-11-23] integrate | 完成 2020 台灣院前／急診指引跨頁整合（`raw/guidelines/` 現有 5 份指引 100% 完成）
- **來源／對象**：`wiki/guidelines/tsgs-tsem-prehospital-ed-2020.md` → `wiki/topics/ais-prehospital-ed-systems.md`、`wiki/guidelines/aha-asa-ais-2026.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，將台灣 119 院前通報、衛福部醫院分級評定與區域聯防、醫策會／TCPI、遠距醫療法規報備、DTN <60 min、不因 CXR 延遲 IVT，以及與 AHA 2026（RACECAT/MSU/院前禁忌/PSC CTA/Telestroke）與台灣後續 2023 EVT / 2025 IVT 之版本演變完整整合至 `ais-prehospital-ed-systems.md`、`aha-asa-ais-2026.md` 與 `overview.md`。
- **備註／待確認**：`raw/guidelines/` 現有全部 5 份 PDF（2026 AHA/ASA 主文＋勘誤、2025 台灣 IVT、2023 台灣 EVT、2020 台灣院前／急診）皆已完成全文編譯與跨頁整合。

## [2026-11-23] ingest | AHA/ASA 2022 自發性腦出血臨床指引（區塊 A：Top 10、Sec 1–4、Sec 5.1 急性降壓、Sec 5.2 抗凝反轉與止血）
- **來源／對象**：`raw/guidelines/greenberg-et-al-2022-2022-guideline-for-the-management-of-patients-with-spontaneous-intracerebral-hemorrhage-a.pdf` → `wiki/guidelines/aha-asa-ich-2022.md`、`index.md`
- **動作摘要**：建立 `wiki/guidelines/aha-asa-ich-2022.md`（`status: partial`），完成區塊 A（e282–e306）完整萃取：Top 10 Take-Home、SVD/CAA（7.39% vs 1.11%/y）、院前體系與 MSU、入院評估與 HE 影像標記（Spot sign / NCCT 徵象）、DIAGRAM 大血管病因檢核、急性降壓（2h 內啟動、1h 達標、目標 140 維持 130–150、禁 <130 `COR 3: Harm`）、抗凝反轉（4-F PCC＋Vit K、Andexanet alfa、Idarucizumab、活性碳、RRT、Protamine）、PATCH 禁用血小板輸注（`COR 3: Harm`）及 TXA/rFVIIa。
- **備註／待確認**：跨頁整合更新計畫（新建 `ich-acute-bp-hemostasis.md`、`ich-anticoagulation-reversal.md` 與更新 `overview.md`）已依半自動把關提交待使用者確認；尚餘區塊 B（Sec 5.3–5.5, Sec 6）與區塊 C（Sec 7–9）待後續分次收錄。

## [2026-11-23] integrate | 完成 AHA/ASA 2022 ICH 指引區塊 A 跨頁整合（急性降壓／止血、抗凝反轉、4-Factor PCC）
- **來源／對象**：`wiki/guidelines/aha-asa-ich-2022.md` → `wiki/topics/ich-acute-bp-hemostasis.md`、`wiki/topics/ich-anticoagulation-reversal.md`、`wiki/interventions/four-factor-pcc.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，正式展開 `ich` 領域知識網，新建 2 篇 ICH 臨床主題頁（含 DIAGRAM 病因檢核與抗凝反轉 Mermaid 流程圖）與 1 篇 `4-Factor PCC` 藥物快查頁，並補齊全庫雙向連結與總覽索引。
- **備註／待確認**：`aha-asa-ich-2022.md` 尚餘區塊 B（Sec 5.3–5.5 神經重症／ICP／癲癇 ＋ Sec 6 外科與微創手術）與區塊 C（Sec 7–9 預後／撤除維生／復健／次級預防與抗栓重啟）待後續分次 Ingest。

## [2026-11-23] ingest | AHA/ASA 2022 自發性腦出血臨床指引（區塊 B：Sec 5.3–5.5 神經重症／ICP／癲癇 ＋ Sec 6 外科手術與微創引流）
- **來源／對象**：`raw/guidelines/greenberg-et-al-2022-2022-guideline-for-the-management-of-patients-with-spontaneous-intracerebral-hemorrhage-a.pdf` → `wiki/guidelines/aha-asa-ich-2022.md`、`index.md`
- **動作摘要**：於 `aha-asa-ich-2022.md` 補入區塊 B（e306–e325）全部建議與數據：照護場域與轉診、QASC／吞嚥／心電監測、DVT（IPC 當日、24–48h 藥物預防、禁彈性襪、近端 DVT 濾網與延遲 1–2 週抗凝）、血糖（<40–60 矯正、>180–200 治療、NICE-SUGAR）、體溫、癲癇（cEEG ≥24h、禁預防性 ASM）、EVD／ICP／滲透壓／禁類固醇，以及 Sec 6 全套外科建議（MIS MISTIE III、IVH 溶栓 CLEAR III、天幕上開顱 STICH、小腦出血 `≥15 mL` 立即手術、減壓去骨瓣）。
- **備註／待確認**：區塊 B 跨頁整合計畫（新建 `ich-surgical-mis-icp.md`、`ich-inpatient-supportive-care.md` 與更新 `overview.md`）已提交待使用者確認；僅餘區塊 C（Sec 7–9）即可達成全文 100% 收錄。

## [2026-11-23] integrate | 完成 AHA/ASA 2022 ICH 指引區塊 B 跨頁整合（外科／微創／ICP 與住院重症／VTE／癲癇）
- **來源／對象**：`wiki/guidelines/aha-asa-ich-2022.md` → `wiki/topics/ich-surgical-mis-icp.md`、`wiki/topics/ich-inpatient-supportive-care.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建 2 篇 ICH 臨床主題頁（含解剖部位導向之外科／微創 Mermaid 流程圖、降死亡 vs 功能預後對照表、ICP/EVD、DVT/VTE 預防治療與癲癇處置），並補齊雙向連結與總覽索引。
- **備註／待確認**：`aha-asa-ich-2022.md` 僅餘最後區塊 C（Sec 7 預後與撤除維生、Sec 8 復健與情緒認知、Sec 9 次級預防與抗栓重啟／初級預防）即可完成全文 100% 收錄。

## [2026-11-23] ingest | AHA/ASA 2022 自發性腦出血臨床指引（區塊 C：Sec 7 預後／撤除維生 ＋ Sec 8 復健／情緒認知 ＋ Sec 9 次級與初級預防 — 全文 100% 完成）
- **來源／對象**：`raw/guidelines/greenberg-et-al-2022-2022-guideline-for-the-management-of-patients-with-spontaneous-intracerebral-hemorrhage-a.pdf` → `wiki/guidelines/aha-asa-ich-2022.md`、`index.md`
- **動作摘要**：於 `aha-asa-ich-2022.md` 補入最後區塊 C（e325–e337）全數建議與數據（ICH/Max-ICH 分數、禁單憑分數撤除維生、延後 DNAR 至至少第 2 天、DNAR 限縮他項治療有害、跨專業復健/ESD、AVERT 24h 密集下床有害、無憂鬱禁 Fluoxetine、PSD/失智篩檢與 SSRI 權衡、7 大再出血因子與 CAA 7.4%/y、長期 BP <130/80 PROGRESS NNT=18、機械瓣膜/LVAD 早期重啟、RESTART 抗血小板、AF ~7–8 週重啟與 LAAO、Statin SPARCL、禁長期 NSAIDs、照護者訓練與高風險 MRI 初級預防），並將指引頁升格為 `status: active`（全文 100% 收錄）。
- **備註／待確認**：區塊 C 跨頁整合計畫（新建 `ich-secondary-prevention-recovery.md` 並更新 `overview.md` 狀態）已依半自動把關提交待使用者確認。

## [2026-11-23] integrate | 完成 AHA/ASA 2022 ICH 指引區塊 C 跨頁整合與全指引收尾（`raw/guidelines/` 現有 6 份 PDF 100% 完成）
- **來源／對象**：`wiki/guidelines/aha-asa-ich-2022.md` → `wiki/topics/ich-secondary-prevention-recovery.md`、`wiki/topics/sp-af-anticoagulation-timing.md`、`wiki/topics/ich-anticoagulation-reversal.md`、`wiki/overview.md`、`index.md`
- **動作摘要**：獲使用者確認後，新建 `ich-secondary-prevention-recovery.md`，完成 ICH 次級預防（7 大再出血因子、長期 BP <130/80、抗血栓重啟/LAAO、禁長期 NSAIDs）、預後/DNAR 倫理、復健/AVERT 紅線與高風險 MRI 初級預防整合，並雙向串聯 `sp-af-anticoagulation-timing.md`、`ich-anticoagulation-reversal.md` 與 `overview.md`（正式升格 `active`）。
- **備註／待確認**：`raw/guidelines/` 現有全部 6 份指引 PDF（2026 AHA/ASA AIS 主文＋勘誤、2022 AHA/ASA ICH、2025 台灣 IVT、2023 台灣 EVT、2020 台灣院前／急診）皆已完成 100% 全文編譯與跨頁整合。
