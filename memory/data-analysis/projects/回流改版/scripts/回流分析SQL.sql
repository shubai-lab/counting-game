-- 回流用户次留率对比（更新前 vs 更新后）
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）

SELECT
    CASE
        WHEN data_day BETWEEN '2026-03-05' AND '2026-03-25' THEN '更新前'
        WHEN data_day BETWEEN '2026-03-26' AND '2026-04-15' THEN '更新后'
    END AS period,
    COUNT(DISTINCT user_id) AS return_users,
    COUNT(DISTINCT CASE WHEN next_day_login = 1 THEN user_id END) AS retained_users,
    ROUND(COUNT(DISTINCT CASE WHEN next_day_login = 1 THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM mg_metabase.sgsnew_return_his
WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
    AND is_aso = '0'
    AND isyjcm = 'true'
GROUP BY
    CASE
        WHEN data_day BETWEEN '2026-03-05' AND '2026-03-25' THEN '更新前'
        WHEN data_day BETWEEN '2026-03-26' AND '2026-04-15' THEN '更新后'
    END
ORDER BY period