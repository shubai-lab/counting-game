-- 60-200级、偏将军以下官阶用户：玩牌局数 × 核心模式
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）
-- 官阶口径：骁卒+校尉（偏将军以下）
-- 等级：60-200级

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
      AND user_level BETWEEN 60 AND 200
),
ret AS (
    SELECT DISTINCT ru.user_id, ru.data_day
    FROM ru
    JOIN mg_metabase.sgsnew_login_his_aso lr
      ON ru.user_id = lr.user_id
     AND DATE_ADD(ru.data_day, 1) = lr.data_day
    WHERE lr.is_aso = '0'
),
game_cnt AS (
    SELECT user_id, data_day, COUNT(DISTINCT gameid) AS game_count
    FROM mg_metabase.sgsnew_game_his
    WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
    GROUP BY user_id, data_day
),
rank AS (
    SELECT user_id, data_day,
           ROW_NUMBER() OVER (PARTITION BY user_id, data_day ORDER BY start_time DESC) AS rn
    FROM mg_metabase.sgsnew_logout_his
    WHERE data_day BETWEEN '2026-03-05' AND '2026-04-15'
)
SELECT
    ru.period,
    CASE WHEN COALESCE(gc.game_count, 0) = 0 THEN '0局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 1 AND 3 THEN '1-3局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 4 AND 10 THEN '4-10局'
         ELSE '10局以上' END AS game_group,
    CASE WHEN lo.shuaidian <= 30000 THEN '骁卒'
         WHEN lo.shuaidian <= 150000 THEN '校尉'
         WHEN lo.shuaidian <= 500000 THEN '郎将'
         ELSE '偏将军以上' END AS rank_group,
    lo.gameid AS core_mode_id,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT ret.user_id) AS retained_users,
    ROUND(COUNT(DISTINCT ret.user_id) * 100.0 / NULLIF(COUNT(DISTINCT ru.user_id), 0), 2) AS retention_rate
FROM ru
LEFT JOIN rank lo ON ru.user_id = lo.user_id AND ru.data_day = lo.data_day AND lo.rn = 1
LEFT JOIN game_cnt gc ON ru.user_id = gc.user_id AND ru.data_day = gc.data_day
LEFT JOIN ret ON ru.user_id = ret.user_id AND ru.data_day = ret.data_day
WHERE ru.period IS NOT NULL
  AND lo.shuaidian <= 150000  -- 偏将军以下：骁卒+校尉
GROUP BY ru.period,
    CASE WHEN COALESCE(gc.game_count, 0) = 0 THEN '0局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 1 AND 3 THEN '1-3局'
         WHEN COALESCE(gc.game_count, 0) BETWEEN 4 AND 10 THEN '4-10局'
         ELSE '10局以上' END,
    CASE WHEN lo.shuaidian <= 30000 THEN '骁卒'
         WHEN lo.shuaidian <= 150000 THEN '校尉'
         WHEN lo.shuaidian <= 500000 THEN '郎将'
         ELSE '偏将军以上' END,
    lo.gameid
ORDER BY ru.period, game_group, rank_group, return_users DESC