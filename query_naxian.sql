-- 查询 sgs_general_activity_operate 表中获取途径包含纳贤的武将
SELECT 
    GeneralID,
    GeneralName,
    ActiveDropWay,
    SpecialDescription
FROM sgs_general_activity_operate
WHERE ActiveDropWay LIKE '%1001%'
   OR ActiveDropWay LIKE '%纳贤%'
   OR SpecialDescription LIKE '%纳贤%'
LIMIT 100
