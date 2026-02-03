-- Ad CTR and Conversion Analysis SQL Queries
-- Designed for SQLite (Compatible with PostgreSQL/BigQuery with minimal changes)

-- 1. Basic Aggregation: Daily CTR, CVR, Avg CPC
-- Overview of daily performance
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

-- 2. Segmentation Analysis: Device, Browser
-- Performance breakdown by device and browser
SELECT 
    device_type,
    browser,
    COUNT(*) as impressions,
    SUM(is_click) as clicks,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent
FROM ad_impressions
GROUP BY 1, 2
ORDER BY 1, 5 DESC;

-- 3. Time Trends: Hourly Analysis
-- Identify peak performance hours
SELECT 
    strftime('%H', timestamp) as hour_of_day,
    COUNT(*) as impressions,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent
FROM ad_impressions
GROUP BY 1
ORDER BY 1;

-- 4. High Value Users: CTR > 5% and has conversion
-- Filter for high-potential user IDs. Aggregated by user_id.
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

-- 5. A/B Testing Analysis
-- Comparison of control vs experimental groups
SELECT 
    experiment_group,
    COUNT(*) as impressions,
    SUM(is_click) as clicks,
    ROUND(AVG(is_click) * 100, 2) as ctr_percent,
    ROUND(SUM(is_conversion) * 1.0 / NULLIF(SUM(is_click), 0) * 100, 2) as cvr_percent
FROM ad_impressions
GROUP BY 1;

-- 6. Funnel Analysis
-- Calculate conversion rates across Impressions -> Click -> Registration -> Conversion
WITH FunnelStats AS (
    SELECT 
        COUNT(*) as total_impressions,
        SUM(is_click) as total_clicks,
        SUM(is_registration) as total_registrations,
        SUM(is_conversion) as total_conversions
    FROM ad_impressions
)
SELECT 
    '1. Impressions' as step, total_impressions as count, 100.0 as conversion_rate
FROM FunnelStats
UNION ALL
SELECT 
    '2. Clicks' as step, total_clicks, ROUND(total_clicks * 100.0 / total_impressions, 2)
FROM FunnelStats
UNION ALL
SELECT 
    '3. Registrations' as step, total_registrations, ROUND(total_registrations * 100.0 / total_clicks, 2)
FROM FunnelStats
UNION ALL
SELECT 
    '4. Conversions' as step, total_conversions, ROUND(total_conversions * 100.0 / total_registrations, 2)
FROM FunnelStats;
