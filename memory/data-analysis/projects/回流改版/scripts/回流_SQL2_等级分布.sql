-- SQL2: 回流用户等级分布
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）
-- 维度：period × 等级分层

WITH ru AS (
    SELECT
        user_id,
        user_level,
        os_type,
        data_day,
        CASE WHEN data_day BETWEEN '2026-03-05' AND '2026-03-25' THEN 'before'
             WHEN data_day BETWEEN '2026-03-26' AND '2026-04-15' THEN 'after'
             ELSE NULL END AS period
    FROM mg_metabase.sgsnew_return_his
    WHERE is_aso = 0
      AND data_day BETWEEN '2026-03-05' AND '2026-04-15'
),
lr AS (
    SELECT DISTINCT user_id, data_day
    FROM mg_metabase.sgsnew_login_his_aso
    WHERE is_aso = '0'
),
ret AS (
    SELECT DISTINCT ru.user_id, ru.data_day
    FROM ru
    JOIN lr ON ru.user_id = lr.user_id AND DATE_ADD(ru.data_day, 1) = lr.data_day
)
SELECT
    ru.period,
    CASE WHEN ru.user_level < 5 THEN '5级以下'
         WHEN ru.user_level BETWEEN 5 AND 60 THEN '5-60级'
         WHEN ru.user_level BETWEEN 61 AND 200 THEN '60-200级'
         ELSE '200级以上' END AS level_group,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT ret.user_id) AS retained_users,
    ROUND(COUNT(DISTINCT ret.user_id) * 100.0 / COUNT(DISTINCT ru.user_id), 2) AS retention_rate
FROM ru
LEFT JOIN ret ON ru.user_id = ret.user_id AND ru.data_day = ret.data_day
WHERE ru.period IS NOT NULL
GROUP BY ru.period, CASE WHEN ru.user_level < 5 THEN '5级以下'
                         WHEN ru.user_level BETWEEN 5 AND 60 THEN '5-60级'
                         WHEN ru.user_level BETWEEN 61 AND 200 THEN '60-200级'
                         ELSE '200级以上' END
ORDER BY ru.period, level_group