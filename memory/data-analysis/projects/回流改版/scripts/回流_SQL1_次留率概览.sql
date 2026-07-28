-- SQL1: 回流用户次留率概览
-- 更新前：2026-03-05 ~ 2026-03-25（21天）
-- 更新后：2026-03-26 ~ 2026-04-15（21天）
-- 维度：period × 平台（PC端/移动端/其他）

WITH ru AS (
    SELECT
        user_id,
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
    CASE WHEN ru.os_type IN ('pc','web','11','12') THEN 'PC端'
         WHEN ru.os_type IN ('android','ios','harmonyos','1','2','7') THEN '移动端'
         ELSE '其他' END AS platform_group,
    COUNT(DISTINCT ru.user_id) AS return_users,
    COUNT(DISTINCT ret.user_id) AS retained_users,
    ROUND(COUNT(DISTINCT ret.user_id) * 100.0 / COUNT(DISTINCT ru.user_id), 2) AS retention_rate
FROM ru
LEFT JOIN ret ON ru.user_id = ret.user_id AND ru.data_day = ret.data_day
WHERE ru.period IS NOT NULL
GROUP BY ru.period, CASE WHEN ru.os_type IN ('pc','web','11','12') THEN 'PC端'
                          WHEN ru.os_type IN ('android','ios','harmonyos','1','2','7') THEN '移动端'
                          ELSE '其他' END
ORDER BY ru.period, platform_group