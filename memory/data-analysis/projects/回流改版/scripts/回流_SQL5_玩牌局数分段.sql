-- SQL5: 回流用户玩牌局数分段
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）
-- 维度：period × 牌局数分段
-- 口径：回流当日玩了X局（含所有模式）

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
game_cnt AS (
    SELECT user_id, data_day, COUNT(DISTINCT gameid) AS game_count
    FROM mg_metabase.sgsnew_game_his
    WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
    GROUP BY user_id, data_day
)
SELECT
    ru.period,
    CASE WHEN gc.game_count = 0 THEN '0局'
         WHEN gc.game_count BETWEEN 1 AND 3 THEN '1-3局'
         WHEN gc.game_count BETWEEN 4 AND 10 THEN '4-10局'
         ELSE '10局以上' END AS game_group,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT ret.user_id) AS retained_users,
    ROUND(COUNT(DISTINCT ret.user_id) * 100.0 / COUNT(DISTINCT ru.user_id), 2) AS retention_rate
FROM ru
LEFT JOIN logout_info lo ON ru.user_id = lo.user_id AND ru.data_day = lo.data_day AND lo.rn = 1
LEFT JOIN game_cnt gc ON ru.user_id = gc.user_id AND ru.data_day = gc.data_day
LEFT JOIN ret ON ru.user_id = ret.user_id AND ru.data_day = ret.data_day
WHERE ru.period IS NOT NULL
GROUP BY ru.period, CASE WHEN gc.game_count = 0 THEN '0局'
                         WHEN gc.game_count BETWEEN 1 AND 3 THEN '1-3局'
                         WHEN gc.game_count BETWEEN 4 AND 10 THEN '4-10局'
                         ELSE '10局以上' END
ORDER BY ru.period, game_group