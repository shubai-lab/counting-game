-- SQL5 修正版: 回流用户玩牌局数分段（含0局）
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）
-- 维度：period × 牌局数分段
-- 口径：回流当日玩了X局（含所有模式）
-- 修复：LEFT JOIN 匹配不上时 game_count 为 NULL，用 COALESCE 兜底确保0局用户被统计

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
game_cnt AS (
    SELECT user_id, data_day, COUNT(DISTINCT gameid) AS game_count
    FROM mg_metabase.sgsnew_game_his
    WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
    GROUP BY user_id, data_day
),
ret AS (
    SELECT DISTINCT ru.user_id, ru.data_day
    FROM ru
    JOIN mg_metabase.sgsnew_login_his_aso lr
      ON ru.user_id = lr.user_id
     AND DATE_ADD(ru.data_day, 1) = lr.data_day
    WHERE lr.is_aso = '0'
)
SELECT
    ru.period,
    CASE WHEN COALESCE(gc.game_count, 0) = 0 THEN '0局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 1 AND 3 THEN '1-3局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 4 AND 10 THEN '4-10局'
         ELSE '10局以上' END AS game_group,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT ret.user_id) AS retained_users,
    ROUND(COUNT(DISTINCT ret.user_id) * 100.0 / NULLIF(COUNT(DISTINCT ru.user_id), 0), 2) AS retention_rate
FROM ru
LEFT JOIN game_cnt gc ON ru.user_id = gc.user_id AND ru.data_day = gc.data_day
LEFT JOIN ret ON ru.user_id = ret.user_id AND ru.data_day = ret.data_day
WHERE ru.period IS NOT NULL
GROUP BY ru.period,
    CASE WHEN COALESCE(gc.game_count, 0) = 0 THEN '0局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 1 AND 3 THEN '1-3局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 4 AND 10 THEN '4-10局'
         ELSE '10局以上' END
ORDER BY ru.period, game_group