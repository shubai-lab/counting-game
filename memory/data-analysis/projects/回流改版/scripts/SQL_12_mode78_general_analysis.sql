-- SQL 12: 模式78武将使用分布分析
WITH return_users AS (
    SELECT
        r.user_id,
        r.data_day AS return_date
    FROM mg_metabase.sgsnew_return_his r
    WHERE r.data_day BETWEEN '2026-03-26' AND '2026-04-15'
        AND r.user_level BETWEEN 60 AND 200
        AND r.is_aso = 0
),

-- 模式78的牌局记录
mode78_games AS (
    SELECT
        g.user_id,
        g.data_day,
        g.gameid,
        g.role1,
        g.issuccess,
        ROW_NUMBER() OVER (PARTITION BY g.user_id, g.data_day ORDER BY g.start_time) AS game_seq
    FROM mg_metabase.sgsnew_game_his g
    INNER JOIN return_users ru ON g.user_id = ru.user_id AND g.data_day = ru.return_date
    WHERE g.playground = '78'
),

-- 每个用户的流失阶段
user_dropout_stage AS (
    SELECT
        user_id,
        data_day,
        COUNT(DISTINCT gameid) AS total_games,
        CASE
            WHEN COUNT(DISTINCT gameid) = 1 THEN '第1局流失'
            WHEN COUNT(DISTINCT gameid) = 2 THEN '第2局流失'
            WHEN COUNT(DISTINCT gameid) >= 3 THEN '完成3局'
        END AS dropout_stage
    FROM mode78_games
    GROUP BY user_id, data_day
),

-- 每个流失阶段的武将使用统计
general_usage_stats AS (
    SELECT
        uds.dropout_stage,
        mg.role1 AS general,
        COUNT(DISTINCT mg.user_id) AS user_count,
        COUNT(DISTINCT mg.gameid) AS game_count,
        SUM(CASE WHEN mg.issuccess = '1' THEN 1 ELSE 0 END) AS win_count,
        SUM(CASE WHEN mg.issuccess = '2' THEN 1 ELSE 0 END) AS lose_count,
        ROUND(SUM(CASE WHEN mg.issuccess = '1' THEN 1 ELSE 0 END) * 1.0 / COUNT(DISTINCT mg.gameid), 4) AS win_rate
    FROM mode78_games mg
    INNER JOIN user_dropout_stage uds ON mg.user_id = uds.user_id AND mg.data_day = uds.data_day
    WHERE mg.role1 IS NOT NULL AND mg.role1 != ''
    GROUP BY uds.dropout_stage, mg.role1
),

-- 次日登录
next_day_login AS (
    SELECT DISTINCT
        l.user_id,
        l.data_day
    FROM mg_metabase.sgsnew_login_his_aso l
    WHERE l.data_day BETWEEN '2026-03-27' AND '2026-04-16'
        AND l.is_aso = '0'
        AND l.isyjcm = 'true'
),

-- 每个流失阶段用户的次留率
user_retention AS (
    SELECT
        uds.dropout_stage,
        uds.user_id,
        CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
    FROM user_dropout_stage uds
    LEFT JOIN next_day_login ndl ON uds.user_id = ndl.user_id AND DATE_ADD(uds.data_day, 1) = ndl.data_day
)

-- 主查询：按流失阶段和武将统计（Top15武将）
SELECT
    gus.dropout_stage,
    gus.general,
    gus.user_count,
    gus.game_count,
    gus.win_count,
    gus.lose_count,
    gus.win_rate,
    ROUND(gus.user_count * 1.0 / SUM(gus.user_count) OVER (PARTITION BY gus.dropout_stage), 4) AS user_pct,
    ROUND(AVG(ur.is_retained) OVER (PARTITION BY gus.dropout_stage), 4) AS stage_retention_rate
FROM general_usage_stats gus
LEFT JOIN user_retention ur ON gus.dropout_stage = ur.dropout_stage
GROUP BY gus.dropout_stage, gus.general, gus.user_count, gus.game_count, gus.win_count, gus.lose_count, gus.win_rate, ur.dropout_stage
ORDER BY gus.dropout_stage, gus.user_count DESC
LIMIT 45;  -- 每个阶段Top15武将