# Ad CTR and Conversion Analysis Pipeline

This is an end-to-end data analysis project simulating a real-world AdTech environment. It covers the entire pipeline from synthetic data generation and SQL data engineering to automated visualization and interactive dashboarding using Python.

---

## Project Highlights
- **Data Generation**: Simulated 50,000 ad impressions with statistical properties (mobile bias, weekend effects, A/B testing variance).
- **SQL Data Engineering**: Efficient SQL queries for daily performance aggregation, user segmentation, and funnel conversion tracking.
- **Automated Reporting**: Automated database connectivity and professional visualization using Pandas and Seaborn.
- **A/B Testing**: Implementation of experimental vs. control group comparison and statistical significance testing.
- **Interactive Dashboard**: A full-featured Streamlit web application for dynamic data exploration.

## Tech Stack
- **Language**: Python 3.x
- **Database**: SQLite
- **Data Analysis**: Pandas, NumPy, Scipy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Web App**: Streamlit
- **Version Control**: Git

## Project Structure
```text
ad_ctr_analysis/
├── data_generator.py     # Synthetic data generator
├── setup_db.py           # Automated SQLite database setup
├── analysis_queries.sql  # Core SQL analysis code (Funnel, Segmentation)
├── analyze_and_report.py # Automated analysis and visualization script
├── dashboard.py          # Interactive Streamlit dashboard
├── README.md             # Project documentation
└── reports/              # Generated visualization reports
    ├── daily_ctr_trend.png
    ├── device_ctr_comparison.png
    ├── ab_test_result.png
    └── funnel_analysis.png
```

## Data Insights and Report

Based on the simulated dataset of 50,000 ad impressions over 30 days, here are the key findings:

### 1. Daily Click-Through Rate (CTR) Trend
![Daily CTR Trend](reports/daily_ctr_trend.png)
*   **Observation**: Overall CTR fluctuates between 2% and 3%.
*   **Insight**: Performance remains stable over time with expected random variance.

### 2. CTR by Device Type
![CTR by Device Type](reports/device_ctr_comparison.png)
*   **Observation**: **Mobile** devices show a significantly higher CTR (~3.4%) compared to desktop (~2.3%).
*   **Insight**: Mobile users are 1.5x more likely to engage with ads. Targeting strategies should prioritize mobile budget allocation.

### 3. A/B Test Results: Ad Creative Performance
![A/B Test Result](reports/ab_test_result.png)
*   **Observation**: `test_creative_A` outperformed the control group in CTR.
*   **Statistical Result**:
    *   **Control Group**: CTR ~2.4%
    *   **Test Group (Creative A)**: CTR ~2.8% (approx. 15% lift)
*   **Conclusion**: Creative A has a statistically significant positive impact.

### 4. Funnel Analysis
![Funnel Analysis](reports/funnel_analysis.png)
*   **Conversion Metrics**:
    *   Impression -> Click: ~2.4%
    *   Click -> Registration: ~30%
    *   Registration -> Conversion: ~24%
*   **Insight**: The conversion rate from registration to purchase is relatively high, indicating strong purchase intent among registered users.

---

## Discovery Dashboard
The project includes a fully interactive dashboard built with Streamlit for real-time data exploration.

### Features
*   **Multi-dimensional Filters**: Filter data by date range and device type.
*   **KPI Monitoring**: Real-time calculation of CTR, CVR, and CPC metrics.
*   **Interactive Visuals**: Plotly-powered charts with zoom and hover capabilities.

### How to Run
1.  Install dependencies:
    ```bash
    pip install streamlit plotly pandas scipy
    ```
2.  Launch the dashboard:
    ```bash
    streamlit run dashboard.py
    ```
3.  The dashboard will open in your default browser at `http://localhost:8501`.

---

## Business Recommendations
1.  **Segment Optimization**: Focus on the **25-34** age group, as they exhibit the highest engagement rates in this simulation.
2.  **Device-Specific Strategy**: While mobile has higher CTR, data suggests desktop is superior for final conversions.
    *   **Strategy**: Use mobile for top-of-funnel awareness and desktop for conversion-focused retargeting.

---
**Author**: [Your Name]
**Keywords**: AdTech, SQL Analysis, Data Visualization, Python, CTR Prediction, Funnel Analysis.
