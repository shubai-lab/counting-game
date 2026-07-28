-- SQL 11: 模式78流失局数、胜率、武将分析
WITH return_users AS (
    SELECT
        r.user_id,
        r.data_day AS return_date,
        CASE
            WHEN r.data_day BETWEEN '2026-03-05' AND '2026-03-25' THEN 'before'
            WHEN r.data_day BETWEEN '2026-03-26' AND '2026-04-15' THEN 'after'
        END AS period
    FROM mg_metabase.sgsnew_return_his r
    WHERE r.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND r.user_level BETWEEN 60 AND 200
        AND r.is_aso = 0
),

-- 模式78的牌局记录（含胜负、武将）
mode78_games AS (
    SELECT
        g.user_id,
        g.data_day,
        g.gameid,
        g.start_time,
        g.issuccess,
        g.role1,
        ROW_NUMBER() OVER (PARTITION BY g.user_id, g.data_day ORDER BY g.start_time) AS game_seq
    FROM mg_metabase.sgsnew_game_his g
    INNER JOIN return_users ru ON g.user_id = ru.user_id AND g.data_day = ru.return_date
    WHERE g.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND g.playground = '78'
),

-- 每个用户在模式78的统计数据
user_mode78_stats AS (
    SELECT
        user_id,
        data_day,
        COUNT(DISTINCT gameid) AS total_games,
        MAX(game_seq) AS max_seq,
        SUM(CASE WHEN issuccess = '1' THEN 1 ELSE 0 END) AS win_count,
        SUM(CASE WHEN issuccess = '2' THEN 1 ELSE 0 END) AS lose_count,
        SUM(CASE WHEN issuccess = '3' THEN 1 ELSE 0 END) AS draw_count,
        ROUND(SUM(CASE WHEN issuccess = '1' THEN 1 ELSE 0 END) * 1.0 / COUNT(DISTINCT gameid), 4) AS win_rate
    FROM mode78_games
    GROUP BY user_id, data_day
),

-- 每个用户最常用的武将
user_main_general AS (
    SELECT
        user_id,
        data_day,
        role1,
        COUNT(*) AS use_count,
        ROW_NUMBER() OVER (PARTITION BY user_id, data_day ORDER BY COUNT(*) DESC) AS rn
    FROM mode78_games
    WHERE role1 IS NOT NULL AND role1 != ''
    GROUP BY user_id, data_day, role1
),

-- 取每个用户的第一常用武将
user_top_general AS (
    SELECT user_id, data_day, role1 AS main_general, use_count
    FROM user_main_general
    WHERE rn = 1
),

-- 次日登录
next_day_login AS (
    SELECT DISTINCT
        l.user_id,
        l.data_day
    FROM mg_metabase.sgsnew_login_his_aso l
    WHERE l.data_day BETWEEN '2026-03-06' AND '2026-04-16'
        AND l.is_aso = '0'
        AND l.isyjcm = 'true'
)

-- 主查询：按流失局数分段，含胜率和武将统计
SELECT
    ru.period,
    CASE
        WHEN ums.total_games IS NULL THEN '未进入模式78'
        WHEN ums.total_games = 0 THEN '未进入模式78'
        WHEN ums.total_games = 1 THEN '第1局流失'
        WHEN ums.total_games = 2 THEN '第2局流失'
        WHEN ums.total_games >= 3 THEN '完成3局'
    END AS dropout_stage,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT CASE WHEN ndl.user_id IS NOT NULL THEN ru.user_id END) AS retained_users,
    ROUND(COUNT(DISTINCT CASE WHEN ndl.user_id IS NOT NULL THEN ru.user_id END) * 1.0 / COUNT(DISTINCT ru.user_id), 4) AS retention_rate,
    ROUND(AVG(ums.total_games), 2) AS avg_games,
    ROUND(AVG(ums.win_rate), 4) AS avg_win_rate,
    ROUND(AVG(ums.win_count), 2) AS avg_win_count,
    ROUND(AVG(ums.lose_count), 2) AS avg_lose_count
FROM return_users ru
LEFT JOIN user_mode78_stats ums ON ru.user_id = ums.user_id AND ru.return_date = ums.data_day
LEFT JOIN next_day_login ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.return_date, 1) = ndl.data_day
WHERE ru.period = 'after'
GROUP BY ru.period,
         CASE
             WHEN ums.total_games IS NULL THEN '未进入模式78'
             WHEN ums.total_games = 0 THEN '未进入模式78'
             WHEN ums.total_games = 1 THEN '第1局流失'
             WHEN ums.total_games = 2 THEN '第2局流失'
             WHEN ums.total_games >= 3 THEN '完成3局'
         END
ORDER BY ru.period,
         CASE dropout_stage
             WHEN '未进入模式78' THEN 0
             WHEN '第1局流失' THEN 1
             WHEN '第2局流失' THEN 2
             WHEN '完成3局' THEN 3
         END;
