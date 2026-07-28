-- 60-200级低官阶用户次留率影响因素分析 - 第一步：基础数据拉取
-- 注意事项：
-- 1. Impala不支持中文列别名，全部使用英文
-- 2. user_level在登录表是string类型，需要CAST
-- 3. 留存率计算：分子分母必须来自不同子查询
-- 4. 工作室账号过滤：is_aso = '0'
-- 5. 帅点分段：骁卒(0)、校尉(4000)、郎将(8000)、偏将军(12000)

-- ==================== SQL 1: 回流用户基础信息+次留情况 ====================
-- 目的：获取60-200级低官阶回流用户的基础信息和次日留存情况
-- 输出：user_id, return_date, channel, os_type, user_level, vip_level, shuaidian, guildid, is_retained

WITH return_users AS (
    -- 回流用户基础信息（来自回流表）
    SELECT
        r.user_id,
        r.data_day AS return_date,
        r.channel,
        r.os_type,
        r.user_level,
        CASE
            WHEN r.data_day BETWEEN '2026-03-05' AND '2026-03-25' THEN 'before'
            WHEN r.data_day BETWEEN '2026-03-26' AND '2026-04-15' THEN 'after'
        END AS period
    FROM mg_metabase.sgsnew_return_his r
    WHERE r.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND CAST(r.user_level AS INT) BETWEEN 60 AND 200  -- 60-200级
        AND r.is_aso = 0
),

-- 用户属性信息（来自登出表，取回流当天的登出记录）
user_attrs AS (
    SELECT
        l.user_id,
        l.data_day,
        l.vip_level,
        l.shuaidian,
        l.guildid,
        l.duration,
        l.silver,
        l.silver2
    FROM mg_metabase.sgsnew_logout_his l
    WHERE l.data_day BETWEEN '2026-03-05' AND '2026-04-16'  -- 多留一天看留存
        AND l.is_aso = 0
),

-- 官阶判断（低官阶：骁卒、校尉、郎将、偏将军）
low_rank_users AS (
    SELECT
        ua.user_id,
        ua.data_day,
        ua.vip_level,
        ua.shuaidian,
        ua.guildid,
        ua.duration,
        ua.silver,
        ua.silver2,
        CASE
            WHEN ua.shuaidian >= 0 AND ua.shuaidian < 4000 THEN 'xiaocu'
            WHEN ua.shuaidian >= 4000 AND ua.shuaidian < 8000 THEN 'xiaowei'
            WHEN ua.shuaidian >= 8000 AND ua.shuaidian < 12000 THEN 'langjiang'
            WHEN ua.shuaidian >= 12000 THEN 'pianjiangjun'
            ELSE 'unknown'
        END AS rank_group
    FROM user_attrs ua
    WHERE ua.shuaidian >= 0 AND ua.shuaidian < 12000  -- 低官阶帅点范围
),

-- 次日登录用户
next_day_login AS (
    SELECT DISTINCT
        l.user_id,
        l.data_day
    FROM mg_metabase.sgsnew_login_his_aso l
    WHERE l.data_day BETWEEN '2026-03-06' AND '2026-04-16'
        AND l.is_aso = '0'
        AND l.isyjcm = 'true'
)

-- 最终输出
SELECT
    ru.user_id,
    ru.return_date,
    ru.channel,
    ru.os_type,
    ru.user_level,
    ru.period,
    lru.vip_level,
    lru.shuaidian,
    lru.rank_group,
    CASE WHEN lru.guildid IS NOT NULL AND lru.guildid != '' THEN 1 ELSE 0 END AS has_guild,
    lru.duration,
    lru.silver,
    lru.silver2,
    CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
FROM return_users ru
LEFT JOIN low_rank_users lru ON ru.user_id = lru.user_id AND ru.return_date = lru.data_day
LEFT JOIN next_day_login ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.return_date, 1) = ndl.data_day
WHERE ru.period IS NOT NULL
    AND lru.rank_group IN ('xiaocu', 'xiaowei', 'langjiang', 'pianjiangjun')  -- 只要低官阶
ORDER BY ru.return_date, ru.channel;


-- ==================== SQL 2: VIP等级分层次留率分析 ====================
-- 目的：看不同VIP等级的次留率差异

WITH return_users_with_vip AS (
    -- 复用SQL1的结果，这里简化展示
    SELECT
        ru.user_id,
        ru.return_date,
        ru.channel,
        ru.os_type,
        ru.period,
        lru.vip_level,
        CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
    FROM mg_metabase.sgsnew_return_his ru
    LEFT JOIN mg_metabase.sgsnew_logout_his lru ON ru.user_id = lru.user_id AND ru.data_day = lru.data_day
    LEFT JOIN mg_metabase.sgsnew_login_his_aso ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.data_day, 1) = ndl.data_day
    WHERE ru.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND CAST(ru.user_level AS INT) BETWEEN 60 AND 200
        AND ru.is_aso = 0
        AND lru.shuaidian >= 0 AND lru.shuaidian < 12000
        AND ndl.is_aso = '0'
        AND ndl.isyjcm = 'true'
)

SELECT
    period,
    vip_level,
    COUNT(DISTINCT user_id) AS return_users,
    SUM(is_retained) AS retained_users,
    ROUND(SUM(is_retained) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM return_users_with_vip
WHERE period IN ('before', 'after')
GROUP BY period, vip_level
ORDER BY period, return_users DESC;


-- ==================== SQL 3: 帅点分层次留率分析 ====================
-- 目的：看帅点分段（0-4000, 4000-8000, 8000-12000）的次留率差异

WITH return_users_with_shuaidian AS (
    SELECT
        ru.user_id,
        ru.period,
        lru.shuaidian,
        CASE
            WHEN lru.shuaidian >= 0 AND lru.shuaidian < 4000 THEN '0-4000'
            WHEN lru.shuaidian >= 4000 AND lru.shuaidian < 8000 THEN '4000-8000'
            WHEN lru.shuaidian >= 8000 AND lru.shuaidian < 12000 THEN '8000-12000'
        END AS shuaidian_range,
        CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
    FROM mg_metabase.sgsnew_return_his ru
    LEFT JOIN mg_metabase.sgsnew_logout_his lru ON ru.user_id = lru.user_id AND ru.data_day = lru.data_day
    LEFT JOIN mg_metabase.sgsnew_login_his_aso ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.data_day, 1) = ndl.data_day
    WHERE ru.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND CAST(ru.user_level AS INT) BETWEEN 60 AND 200
        AND ru.is_aso = 0
        AND lru.shuaidian >= 0 AND lru.shuaidian < 12000
)

SELECT
    period,
    shuaidian_range,
    COUNT(DISTINCT user_id) AS return_users,
    SUM(is_retained) AS retained_users,
    ROUND(SUM(is_retained) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM return_users_with_shuaidian
WHERE period IN ('before', 'after')
GROUP BY period, shuaidian_range
ORDER BY period, shuaidian_range;


-- ==================== SQL 4: 公会参与次留率分析 ====================
-- 目的：看有公会 vs 无公会的次留率差异

WITH return_users_with_guild AS (
    SELECT
        ru.user_id,
        ru.period,
        CASE WHEN lru.guildid IS NOT NULL AND lru.guildid != '' THEN 1 ELSE 0 END AS has_guild,
        CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
    FROM mg_metabase.sgsnew_return_his ru
    LEFT JOIN mg_metabase.sgsnew_logout_his lru ON ru.user_id = lru.user_id AND ru.data_day = lru.data_day
    LEFT JOIN mg_metabase.sgsnew_login_his_aso ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.data_day, 1) = ndl.data_day
    WHERE ru.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND CAST(ru.user_level AS INT) BETWEEN 60 AND 200
        AND ru.is_aso = 0
        AND lru.shuaidian >= 0 AND lru.shuaidian < 12000
)

SELECT
    period,
    has_guild,
    COUNT(DISTINCT user_id) AS return_users,
    SUM(is_retained) AS retained_users,
    ROUND(SUM(is_retained) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM return_users_with_guild
WHERE period IN ('before', 'after')
GROUP BY period, has_guild
ORDER BY period, has_guild;


-- ==================== SQL 5: 渠道分层次留率分析 ====================
-- 目的：看不同渠道的次留率差异（按回流人数排序）

WITH return_users_by_channel AS (
    SELECT
        ru.user_id,
        ru.period,
        ru.channel,
        CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
    FROM mg_metabase.sgsnew_return_his ru
    LEFT JOIN mg_metabase.sgsnew_logout_his lru ON ru.user_id = lru.user_id AND ru.data_day = lru.data_day
    LEFT JOIN mg_metabase.sgsnew_login_his_aso ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.data_day, 1) = ndl.data_day
    WHERE ru.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND CAST(ru.user_level AS INT) BETWEEN 60 AND 200
        AND ru.is_aso = 0
        AND lru.shuaidian >= 0 AND lru.shuaidian < 12000
)

SELECT
    period,
    channel,
    COUNT(DISTINCT user_id) AS return_users,
    SUM(is_retained) AS retained_users,
    ROUND(SUM(is_retained) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM return_users_by_channel
WHERE period IN ('before', 'after')
GROUP BY period, channel
ORDER BY period, return_users DESC;  -- 按回流人数降序


-- ==================== SQL 6: 平台分层次留率分析 ====================
-- 目的：看不同平台的次留率差异

WITH return_users_by_os AS (
    SELECT
        ru.user_id,
        ru.period,
        ru.os_type,
        CASE
            WHEN ru.os_type IN ('android', 'ios', 'harmonyos') THEN 'mobile'
            WHEN ru.os_type IN ('pc', 'web') THEN 'pc'
            ELSE 'other'
        END AS platform,
        CASE WHEN ndl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_retained
    FROM mg_metabase.sgsnew_return_his ru
    LEFT JOIN mg_metabase.sgsnew_logout_his lru ON ru.user_id = lru.user_id AND ru.data_day = lru.data_day
    LEFT JOIN mg_metabase.sgsnew_login_his_aso ndl ON ru.user_id = ndl.user_id AND DATE_ADD(ru.data_day, 1) = ndl.data_day
    WHERE ru.data_day BETWEEN '2026-03-05' AND '2026-04-15'
        AND CAST(ru.user_level AS INT) BETWEEN 60 AND 200
        AND ru.is_aso = 0
        AND lru.shuaidian >= 0 AND lru.shuaidian < 12000
)

SELECT
    period,
    platform,
    COUNT(DISTINCT user_id) AS return_users,
    SUM(is_retained) AS retained_users,
    ROUND(SUM(is_retained) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM return_users_by_os
WHERE period IN ('before', 'after')
GROUP BY period, platform
ORDER BY period, return_users DESC;