-- 预流失用户牌局参与情况分析
-- 参数：tag_date（标签日期）、date_range_start、date_range_end

WITH pre_loss_users AS (
    SELECT DISTINCT user_id
    FROM mg_metabase.sgsnew_user_tag
    WHERE data_day = '${tag_date}'
),

battle_records AS (
    SELECT
        user_id,
        SUBSTR(start_time, 1, 10) AS battle_date,
        playground AS mode_id,
        CASE WHEN issuccess = '1' THEN 1 ELSE 0 END AS is_win,
        1 AS battle_cnt
    FROM mg_metabase.sgsnew_game_his
    WHERE data_day BETWEEN '${date_range_start}' AND '${date_range_end}'
      AND start_time IS NOT NULL
),

user_daily_stats AS (
    SELECT
        p.user_id,
        b.battle_date,
        SUM(b.battle_cnt) AS daily_battles,
        SUM(b.is_win) AS daily_wins,
        COUNT(DISTINCT b.mode_id) AS mode_count
    FROM pre_loss_users p
    LEFT JOIN battle_records b ON p.user_id = b.user_id
    GROUP BY p.user_id, b.battle_date
),

daily_stats_with_label AS (
    SELECT
        user_id,
        battle_date,
        daily_battles,
        daily_wins,
        mode_count,
        CASE
            WHEN battle_date < '${tag_date}' THEN CONCAT('D-', CAST(DATEDIFF('${tag_date}', battle_date) AS STRING))
            WHEN battle_date = '${tag_date}' THEN 'D0'
            ELSE CONCAT('D+', CAST(DATEDIFF(battle_date, '${tag_date}') AS STRING))
        END AS day_label
    FROM user_daily_stats
)

SELECT
    day_label AS 日期标签,
    COUNT(DISTINCT user_id) AS 用户数,
    ROUND(AVG(daily_battles), 2) AS 日均牌局数,
    ROUND(SUM(daily_wins) * 1.0 / NULLIF(SUM(daily_battles), 0), 4) AS 平均胜率,
    ROUND(AVG(mode_count), 2) AS 日均参与模式数
FROM daily_stats_with_label
WHERE day_label IS NOT NULL
GROUP BY day_label
ORDER BY
    CASE
        WHEN day_label LIKE 'D-%' THEN 1000 - CAST(REPLACE(day_label, 'D-', '') AS INT)
        WHEN day_label = 'D0' THEN 0
        ELSE 1000 + CAST(REPLACE(day_label, 'D+', '') AS INT)
    END
