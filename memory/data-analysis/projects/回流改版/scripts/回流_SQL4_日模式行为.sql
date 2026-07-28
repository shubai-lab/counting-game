-- SQL4: 回流用户日模式行为分析
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）
-- 维度：period × 日模式参与（有/无）
-- 日模式定义：playground IN (8, 36, 401)

WITH ru AS (
    SELECT
        user_id,
        user_level,
        data_day,
        CASE WHEN data_day BETWEEN '2026-03-05' AND '2026-03-25' THEN 'before'
             WHEN data_day BETWEEN '2026-03-26' AND '2026-04-15' THEN 'after'
             ELSE NULL END AS period
    FROM mg_metabase.sgsnew_return_his
    WHERE is_aso = 0
      AND data_day BETWEEN '2026-03-05' AND '2026-04-15'
),
logout_info AS (
    SELECT user_id, data_day, shuaidian,
           ROW_NUMBER() OVER (PARTITION BY user_id, data_day ORDER BY start_time DESC) AS rn
    FROM mg_metabase.sgsnew_logout_his
    WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
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
),
game AS (
    SELECT DISTINCT user_id, data_day
    FROM mg_metabase.sgsnew_game_his
    WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
      AND playground IN ('8', '36', '401')
)
SELECT
    ru.period,
    CASE WHEN g.user_id IS NOT NULL THEN '有日模式' ELSE '无日模式' END AS day_mode,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT ret.user_id) AS retained_users,
    ROUND(COUNT(DISTINCT ret.user_id) * 100.0 / COUNT(DISTINCT ru.user_id), 2) AS retention_rate
FROM ru
LEFT JOIN logout_info lo ON ru.user_id = lo.user_id AND ru.data_day = lo.data_day AND lo.rn = 1
LEFT JOIN game g ON ru.user_id = g.user_id AND ru.data_day = g.data_day
LEFT JOIN ret ON ru.user_id = ret.user_id AND ru.data_day = ret.data_day
WHERE ru.period IS NOT NULL
GROUP BY ru.period, CASE WHEN g.user_id IS NOT NULL THEN '有日模式' ELSE '无日模式' END
ORDER BY ru.period, day_mode