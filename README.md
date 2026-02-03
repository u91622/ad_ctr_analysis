# 數位廣告點擊率 (CTR) 與轉換分析專案
### Digital Advertising CTR & Conversion Analysis Pipeline

這是一個模擬真實廣告技術 (AdTech) 情情境的端到端數據分析專案。從資料生成、SQL 數據工程到 Python 視覺化自動報告，完整展示了對廣告指標（如 CTR、CVR、CPC）的深度理解與技術實作。

---

## 🚀 專案亮點 (Highlights)
- **數據生成**：模擬 50,000 筆具有統計特性的廣告曝光資料（包含行動裝置偏好、週末效應、A/B 測試差異）。
- **SQL 數據工程**：撰寫高效 SQL 查詢，進行每日成效聚合、用戶分群分析與漏斗轉化計算。
- **自動化報告**：使用 Python (Pandas, Seaborn) 自動串聯資料庫並產出專業級的視覺化分析圖表。
- **A/B 測試實務**：實作實驗組與對照組的成效比對邏輯。

## 🛠️ 技術棧 (Tech Stack)
- **語言**：Python 3.x
- **資料庫**：SQLite (內建標準庫，輕量高效)
- **數據分析**：Pandas, NumPy
- **視覺化**：Matplotlib, Seaborn
- **版本控制**：Git

## 📂 檔案結構 (Project Structure)
```text
ad_ctr_analysis/
├── data_generator.py     # 合成資料生成器 (模擬 Ad Logs)
├── setup_db.py           # 自動化 SQLite 資料庫建置與資料匯入
├── analysis_queries.sql  # 核心 SQL 分析代碼 (分群、趨勢、高價值用戶)
├── analyze_and_report.py # Python 自動化分析與視覺化報告腳本
├── README.md             # 專案說明文件
└── reports/              # [自動生成] 存放分析圖表路徑
    ├── daily_ctr_trend.png
    ├── device_ctr_comparison.png
    └── ab_test_result.png
```

## 📊 分析結果與洞察報告 (Data Insights)

本分析基於 30 天內的 50,000 筆模擬廣告數據，以下是關鍵發現：

### 1. 每日點擊率趨勢 (Daily CTR Trend)
![每日點擊率趨勢](reports/daily_ctr_trend.png)
*   **觀察**：整體 CTR 穩定在 2% ~ 3% 之間波動。
*   **洞察**：每日波動主要受模擬雜訊影響，但在週末觀察到轉換率 (CVR) 有明顯提升趨勢。

### 2. 裝置成效對比 (CTR by Device)
![各裝置點擊率比較](reports/device_ctr_comparison.png)
*   **觀察**：**行動裝置 (Mobile)** 的 CTR (約 3.4%) 顯著高於桌機 (約 2.3%) 與平板。
*   **洞察**：行動端用戶對廣告的點擊意願強出 1.5 倍，應考慮將 **60% 以上的預算優先投放在行動裝置** 以優化 ROI。

### 3. A/B 測試：廣告創意成效 (A/B Test Results)
![A/B 測試結果](reports/ab_test_result.png)
*   **觀察**：`test_creative_A` 組別在點擊率 (CTR) 上優於 `control` 組。
*   **數據報告**：
    *   **Control 組**：CTR ~2.4%
    *   **Test 組 (Creative A)**：CTR ~2.8% (提升約 15%)
*   **結論**：新的廣告創意（實驗組）具備顯著的正向影響，建議全面導入該版創意。

### 4. 漏斗分析 (Funnel Analysis)
![漏斗分析](reports/funnel_analysis.png)
*   **各階段轉化**：
    *   Impression -> Click: ~2.4%
    *   Click -> Registration: ~30%
    *   Registration -> Conversion: ~24%
*   **洞察**：註冊到購買的流失率較低，顯示註冊用戶具備高購買意圖。

---

## 📈 互動式儀表板 (Discovery Dashboard)
本專案包含一個基於 **Streamlit** 的全功能數據儀表板，讓您可以透過瀏覽器跟數據互動。

### 功能特色 (Features)
*   **多維度篩選**：可依照「日期區間」與「裝置類型」即時過濾數據。
*   **關鍵指標監控 (KPIs)**：即時計算 CTR, CVR, CPC 等核心指標。
*   **動態視覺化**：整合 Plotly 的互動式圖表（可縮放、懸停查看數值）。

### 如何啟動 (How to Run)
1.  安裝必要的 Python 套件：
    ```bash
    pip install streamlit plotly
    ```
2.  啟動 Dashboard：
    ```bash
    streamlit run dashboard.py
    ```
3.  瀏覽器會自動開啟，即可開始探索數據（預設網址：`http://localhost:8501`）。

---

## 💡 深度商業洞察 (Business Recommendations)
1.  **分群優化**：針對 **25-34 歲** 的核心受眾（模擬中加權最高），點擊率最為穩定，建議開發專為該年齡層量身打造的內容。
2.  **轉換漏斗**：雖然行動裝置點擊率高，但數據顯示桌機在「轉換率 (CVR)」上更具優勢。這可能暗示用戶傾向在手機上「看」，而在桌機上完成「結帳」。
    *   **策略建議**：手機廣告應側重於品牌曝光與清單收藏，而桌機廣告應側重於最後的購買點擊。

---

## ⚙️ 如何執行 (How to Setup)

1. **複製專案**：
   ```bash
   git clone <your-repo-url>
   cd ad_ctr_analysis
   ```

2. **安裝依賴套件**：
   ```bash
   pip install pandas matplotlib seaborn
   ```

3. **依序執行腳本**：
   ```bash
   # 生成模擬數據與資料庫
   python data_generator.py
   python setup_db.py

   # 產出分析報告
   python analyze_and_report.py
   ```

---

## 💡 專案背景與洞察
在 Appier 等廣告科技公司，數據的顆粒度極大且具備時序性。本專案模擬了這類數據的關鍵特徵：
- **行動裝置優先**：模擬數據中行動手機具備更強的點擊誘因。
- **週末高峰**：考慮到用戶在休假時具備較高的購物意願，調整了週末的轉換機率。
- **數據清洗邏輯**：嚴格實作「最後點擊歸因」(Last Click Attribution)，確保只有點擊過的曝光才能進入轉換統計。

---
**Author**: [Your Name/GitHub ID]
**Keywords**: AdTech, SQL Analysis, Data Visualization, Python, CTR Prediction Context.
