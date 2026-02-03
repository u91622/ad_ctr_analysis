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

## 📊 分析結果預覽 (Results Preview)
以下為自動生成的報告範例：

### 1. 每日點擊率趨勢 (Daily CTR Trend)
觀察廣告在 30 天內的成效波動，有助於發現週期性趨勢。

### 2. 裝置成效對比 (CTR by Device)
數據顯示 **行動裝置 (Mobile)** 的 CTR 明顯高於桌機，建議廣告主以此分配預算。

### 3. A/B 測試分析 (A/B Test Results)
對比不同廣告創意對點擊率與轉換率的提升影響。

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
