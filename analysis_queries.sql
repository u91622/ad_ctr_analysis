-- 數位廣告 CTR 與轉換分析 SQL 查詢
-- 設計用於 SQLite（只需少量調整即可適用於 PostgreSQL/BigQuery）

-- 1. 基礎聚合：每日 CTR (點擊率), CVR (轉換率), Avg CPC (平均點擊成本)
-- 每日成效概覽
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as impressions,
    SUM(is_click) as clicks,
    SUM(is_conversion) as conversions,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent,
    ROUND(SUM(is_conversion) * 1.0 / NULLIF(SUM(is_click), 0) * 100, 2) as cvr_percent,
    ROUND(AVG(cpc_bid), 2) as avg_cpc
FROM ad_impressions
GROUP BY 1
ORDER BY 1;

-- 2. 分群分析：裝置、瀏覽器
-- 依裝置與瀏覽器細分表現
SELECT 
    device_type,
    browser,
    COUNT(*) as impressions,
    SUM(is_click) as clicks,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent
FROM ad_impressions
GROUP BY 1, 2
ORDER BY 1, 5 DESC;

-- 3. 時間趨勢：每小時分析
-- 找出一天中的黃金時段
SELECT 
    strftime('%H', timestamp) as hour_of_day,
    COUNT(*) as impressions,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent
FROM ad_impressions
GROUP BY 1
ORDER BY 1;

-- 4. 高價值用戶：CTR > 5% (模擬值) 且有轉換
-- 篩選高潛力用戶 ID。由於資料是單次曝光層級，需先對 user_id 進行聚合 (Group By)。
SELECT 
    user_id,
    COUNT(*) as user_impressions,
    SUM(is_click) as user_clicks,
    SUM(is_conversion) as user_conversions,
    ROUND(AVG(is_click) * 100, 2) as user_ctr
FROM ad_impressions
GROUP BY user_id
HAVING user_ctr > 5.0 AND user_conversions > 0
ORDER BY user_conversions DESC
LIMIT 50;

-- 5. A/B 測試模擬
-- 比較實驗組與對照組的成效
SELECT 
    experiment_group,
    COUNT(*) as impressions,
    SUM(is_click) as clicks,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent,
    ROUND(SUM(is_conversion) * 1.0 / NULLIF(SUM(is_click), 0) * 100, 2) as cvr_percent
FROM ad_impressions
GROUP BY 1;
