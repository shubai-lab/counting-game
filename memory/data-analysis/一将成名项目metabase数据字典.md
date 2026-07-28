# 一将成名项目metabase数据字典

> **Metabase 地址**: http://metabase.nj.dc.yokagames.com
> 注意：所有表名需要加 `mg_metabase.` 前缀，例如 `mg_metabase.sgsnew_return_his`
>
> **SQL编写注意事项**：
> - Impala **不支持中文列名/列别名**，请使用英文（如 `user_segment`, `period`, `arpu`）
> - 分区字段 `data_day` 格式为 `'YYYY-MM-DD'`，建议使用 `BETWEEN '2026-03-01' AND '2026-03-31'` 而非 `IN`
> - 日期计算函数：`DATE_ADD(date_col, 7)` = 加7天
> - 过滤条件用 `WHERE` 而非 `HAVING`（`HAVING` 仅用于聚合后的条件筛选）
> - 工作室账号过滤：`is_aso = 0` 或 `is_aso = '0'`
> - **字段类型注意**：`user_level` 在登录表是 `string` 类型，比较时需 `CAST(user_level AS INT) < 5`
> - **留存率计算注意**：分子和分母必须来自不同的子查询，否则分子分母相同导致结果永远=100%

# SQL常见错误与解决方案

## 一、字段存在性问题

### 1. sgsnew_logout_his表没有is_aso字段

**错误信息**：
```
AnalysisException: Could not resolve column/field reference: 'l.is_aso'
```

**原因**：
- sgsnew_logout_his表数据字典明确说明"该表未去除工作室账号"
- 该表不存在is_aso字段

**解决方案**：
```sql
-- 错误写法
FROM mg_metabase.sgsnew_logout_his l
WHERE l.is_aso = 0  -- ❌ 该表没有此字段

-- 正确写法
FROM mg_metabase.sgsnew_logout_his l
WHERE ...  -- ✅ 移除is_aso过滤，或通过JOIN其他表过滤
```

**受影响表**：
- sgsnew_logout_his：无is_aso字段
- sgsnew_return_his：有is_aso字段（int类型）
- sgsnew_login_his_aso：有is_aso字段（string类型）

---

## 二、字段类型问题

### 2. user_level字段类型不一致

**错误场景**：
```sql
WHERE r.user_level BETWEEN 60 AND 200  -- ❌ user_level是string类型
```

**解决方案**：
```sql
WHERE CAST(r.user_level AS INT) BETWEEN 60 AND 200  -- ✅ 显式转换
```

**受影响表**：
- sgsnew_login_his_aso：user_level是string类型
- sgsnew_return_his：user_level是int类型

### 3. is_aso字段类型不一致

**问题**：
- sgsnew_return_his：is_aso是int类型
- sgsnew_login_his_aso：is_aso是string类型

**解决方案**：
```sql
-- sgsnew_return_his
WHERE r.is_aso = 0  -- ✅ int类型，不用引号

-- sgsnew_login_his_aso
WHERE l.is_aso = '0'  -- ✅ string类型，用引号
```

---

## 三、留存率计算问题（最常见错误）

### 4. 留存人数计算错误

**错误方法**：
```sql
SELECT
    COUNT(DISTINCT user_id) AS return_users,
    SUM(is_retained) AS retained_users,  -- ❌ 错误！会把一个用户的所有登录记录都加起来
    ROUND(SUM(is_retained) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM ...
```

**错误结果示例**：
- 回流人数：4020人
- 留存人数：117912人（不可能！留存人数应该≤回流人数）
- 次留率：29.3313%（看起来正常，但数据错误）

**原因**：
- is_retained字段可能来自JOIN，一个user_id可能对应多行数据
- SUM会把所有行都加起来，导致留存人数虚高

**正确方法**：
```sql
SELECT
    COUNT(DISTINCT user_id) AS return_users,
    COUNT(DISTINCT CASE WHEN is_retained = 1 THEN user_id END) AS retained_users,  -- ✅ 正确！
    ROUND(COUNT(DISTINCT CASE WHEN is_retained = 1 THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 4) AS retention_rate
FROM ...
```

**验证方法**：
- 留存人数必须 ≤ 回流人数
- 次留率必须 ≤ 100%

**适用场景**：
- 所有聚合分析的留存率计算
- 所有分维度的留存率计算（VIP、帅点、渠道、平台等）

---

## 四、SQL语法问题

### 5. WITH子句后面必须紧跟主查询

**错误信息**：
```
ParseException: Syntax error in line 15: ), ^ Encountered: EOF Expected: DEFAULT, IDENTIFIER
```

**错误写法**：
```sql
WITH return_users AS (
    SELECT ...
),  -- ❌ 只有CTE定义，没有主查询

-- 缺少主查询！
```

**正确写法**：
```sql
WITH return_users AS (
    SELECT ...
),
user_attrs AS (
    SELECT ...
)

-- 主查询（不能省略）
SELECT ...
FROM return_users
LEFT JOIN user_attrs ...
```

**关键点**：
- WITH子句定义的CTE必须有主查询来使用它
- 主查询在最后一个CTE定义之后，用SELECT开始
- 所有CTE定义用逗号分隔，最后一个CTE后面没有逗号

### 6. 字段别名引用问题

**错误信息**：
```
AnalysisException: Could not resolve column/field reference: 'ru.return_date'
```

**错误场景**：
```sql
WITH return_users_with_vip AS (
    SELECT
        ru.user_id,
        ru.return_date,  -- ❌ 基表中没有return_date字段
        ...
    FROM mg_metabase.sgsnew_return_his ru  -- ru表没有return_date
    ...
)
```

**原因**：
- return_date是在SQL 1中定义的别名：`r.data_day AS return_date`
- SQL 2直接查询基表，没有定义这个别名

**解决方案**：
```sql
-- 方案1：移除不需要的字段
SELECT ru.user_id, ...  -- ✅ 不引用return_date

-- 方案2：定义别名
SELECT ru.data_day AS return_date, ...  -- ✅ 定义别名
```

---

## 五、检查清单

在执行SQL前，请检查：

1. ✅ **字段存在性**：确认表中有该字段
2. ✅ **字段类型**：string字段要CAST，is_aso注意int/string差异
3. ✅ **留存计算**：用COUNT(DISTINCT CASE...)，不要用SUM
4. ✅ **WITH语法**：CTE后面必须有主查询
5. ✅ **字段别名**：只引用已定义的别名
6. ✅ **数据验证**：留存人数≤回流人数，留存率≤100%

---

## 六、常见错误速查表

| 错误类型 | 错误信息 | 解决方案 |
|---------|---------|---------|
| 字段不存在 | Could not resolve column/field reference | 确认表结构，移除不存在的字段 |
| 类型错误 | Syntax error | CAST转换类型，注意引号 |
| 留存计算错误 | 留存人数>回流人数 | 用COUNT(DISTINCT CASE...) |
| WITH语法错误 | Encountered: EOF | 添加主查询 |
| 别名不存在 | Could not resolve column | 定义或移除别名引用 |


# Sgsnew Newlogin His 新增账号表

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id        |   string   |  205\_210(一将服务端)  |   |
|   user\_id       |   string   |  通行证账号  |   |
|   device\_id     |   string   |   |   |
|   os\_type       |   string   |   |   |
|   channel       |   string   |  渠道号  |   |
|   ip            |   string   |   |   |
|   province      |   string   |   |   |
|   city          |   string   |   |   |
|   app\_version   |   string   |   |   |
|   start\_time    |   string   |   |   |
|   is\_aso        |   string   |  是否工作室账号，使用时一般限制该字段为0  |   |
|   isyjcm        |   string   |  是否一将成名版本  |  true/false  |
|   data\_day      |   string   |   |   |

# Sgsnew Login His Aso 登录表

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id        |   string   |   |   |
|   user\_id       |   string   |   |   |
|   os\_type       |   string   |   |   |
|   channel       |   string   |   |   |
|   device\_id     |   string   |   |   |
|   bfuser\_id     |   string   |  角色数值ID  |   |
|   ip            |   string   |   |   |
|   province      |   string   |   |   |
|   app\_version   |   string   |   |   |
|   user\_level    |   string   |   |   |
|   vip\_level     |   string   |   |   |
|   age           |   string   |  年龄，不全，渠道的实名认证信息拿不到，首次登录时没有实名信息  |   |
|   is\_aso        |   string   |  是否工作室账号，使用时一般限制该字段为0  |   |
|   start\_time    |   string   |   |   |
|   isyjcm        |   string   |  是否一将成名版本  |   |
|   data\_day      |   string   |   |   |

# Sgsnew Logout His 登出表

该表未去除工作室账号，通常和其他表配合使用取玩家的在线时长、最大等级、帅点、元宝保有等

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id       |   string   |   |   |
|   user\_id      |   string   |   |   |
|   os\_type      |   string   |   |   |
|   channel      |   string   |   |   |
|   ip           |   string   |   |   |
|   province     |   string   |   |   |
|   city         |   string   |   |   |
|   duration     |   bigint   |  当前次在线时长/秒  |   |
|   start\_time   |   string   |   |   |
|   shuaidian    |   bigint   |  帅点，根据帅点计算官阶等级：骁卒=0、校尉=4000、郎将=8000、偏将军=12000（偏将军及以下为低官阶，以上为高官阶）、将军=40000、上将军=60000、国护军=80000、国都护=130000、卫将军=160000、车骑将军=200000、骠骑将军=250000、大将军=350000 ； |   |
|   silver       |   bigint   |  登出时通元保有数  |   |
|   silver2      |   bigint   |  登出时元保有数  |   |
|   user\_level   |   int      |   |   |
|   vip\_level    |   int      |   |   |
|   guildid      |   string   |  公会ID  |   |
|   guildlev     |   string   |   |   |
|   data\_day     |   string   |   |   |

# Sgsnew Recharge His 充值表

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id             |   string   |   |   |
|   user\_id            |   string   |   |   |
|   device\_id          |   string   |   |   |
|   os\_type            |   string   |  操作系统，该字段记录不准确，建议用渠道字段判断充值端  |   |
|   channel            |   string   |  充值渠道（用户充值时所在渠道，非新增渠道）  |   |
|   ip                 |   string   |   |   |
|   province           |   string   |   |   |
|   city               |   string   |   |   |
|   order\_id           |   string   |  订单号  |   |
|   amount             |   double   |  金额  |   |
|   recharge\_channel   |   string   |   |   |
|   start\_time         |   string   |   |   |
|   user\_level         |   int      |   |   |
|   vip\_level          |   int      |   |   |
|   isyjcm             |   string   |  是否一将成名  |   |
|   data\_day           |   string   |   |   |

# Sgsnew Return His 回流玩家表

回流用户定义：连续30日未登录、统计日登录

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   user\_id      |   string   |   |   |
|   server       |   string   |   |   |
|   user\_level   |   int      |  回流时等级  |   |
|   channel      |   string   |  回流的渠道  |   |
|   os\_type      |   string   |  回流的端  |   |
|   app\_id       |   string   |   |   |
|   start\_time   |   string   |   |   |
|   ip           |   string   |   |   |
|   device\_id    |   string   |   |   |
|   is\_aso       |   int      |  是否工作室账号，一般需限制为0  |   |
|   data\_day     |   string   |   |   |

# Sgsnew\_Game\_His 牌局结算表

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id             |   string   |  205\_210(一将服务端)  |   |
|   user\_id            |   string   |  通行证账号  |   |
|   start\_time         |   string   |  牌局结算时间（非开始时间）  |   |
|   device\_id          |   string   |   |   |
|   ip                 |   string   |   |   |
|   os\_type            |   string   |   |  1：android  2：iOS  7：harmony 11：pc  12:web  |
|   user\_level         |   string   |   |   |
|   viplev             |   string   |   |   |
|   gameid             |   string   |  一局的唯一ID，根据该字段可匹配同一局的玩家  |   |
|   playground         |   string   |  模式ID  |   |
|   identity           |   string   |  身份  |   |
|   pushgenerals       |   string   |  推将列表  |   |
|   role1              |   string   |  出场武将  |   |
|   isfirstactor       |   string   |  是否先手  |   |
|   seat               |   string   |  座位  |  和实际牌局表现座次不一致，要结合是否先手字段判断  |
|   issuccess          |   string   |  是否胜利  |  1：胜利 2：失败 3：平局  |
|   isescape           |   string   |  是否逃跑  |  true/false  |
|   ismvp              |   string   |   |   |
|   rank1              |   string   |  开始前段位  |   |
|   rank2              |   string   |  结算后段位  |   |
|   get1               |   string   |  牌局获得道具  |   |
|   duration           |   int      |  牌局时长  |   |
|   aitime             |   int      |  托管时长  |   |
|   waiting\_duration   |   int      |  牌局内等待时长  |   |
|   matchtime          |   int      |  匹配时长  |   |
|   playtime           |   int      |  操作时长  |   |
|   deadtime           |   int      |  死亡后牌局继续时长  |   |
|   gametype           |   string   |  pvp/pve  |   |
|   usercnt            |   string   |  组队ID，0表示未组队  |   |
|   extra\_info         |  json  |  拓展字段，模式个性化字段一般记录在这里，开发新增字段尽量放在这里，否则不会自动在表内新增  |   |
|   shuaidian          |   int      |  帅点  |   |
|   live\_turn          |   string   |  存活轮次  |   |
|   data\_day           |   string   |  日志发生时间  |   |

# Sgsnew Task His 任务完成领奖表

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   start\_time   |   string   |   |   |
|   app\_id       |   string   |   |   |
|   user\_id      |   string   |   |   |
|   get1         |   string   |  任务获得道具列表  |   |
|   taskid       |   string   |  任务ID  |   |
|   user\_level   |   string   |  等级  |   |
|   taskname     |   string   |  任务名称  |   |
|   type         |   string   |   |   |
|   op\_type      |   string   |   |  401：领奖 402：完成  |
|   data\_day     |   string   |   |   |

# Sgsnew Item Get His 道具产出表

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id       |   string   |   |   |
|   user\_id      |   string   |   |   |
|   start\_time   |   string   |   |   |
|   user\_level   |   string   |   |   |
|   itemid       |   string   |  道具ID（将get1列表展开后）  |   |
|   num          |   bigint   |  产出数量  |   |
|   get1         |   string   |  产出道具列表  |   |
|   consume      |   string   |  消耗道具列表  |   |
|   detail       |   string   |  产出详情（具体场景需求可咨询开发）  |   |
|   op\_type      |   string   |   |  // 购买     LTBuy = 202; // 赠送    LTBestowal = 203;  // 使用 LTUseItem = 204;  // 领取礼包道具LTGiftGetReward = 205; // 邮件领取道具  LTEmailGetReward = 206; // 任务获得道具 LTTaskGetReward = 207; // 公共获得道具(三国秀合成分解,签到等其他的)   LTItemCommon = 208;  |
|   data\_day     |   string   |   |   |

# Sgsnew Item Consume His 道具消耗表

源表同产出表。为了便于统计将消耗道具列表展开

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id       |   string   |   |   |
|   user\_id      |   string   |   |   |
|   start\_time   |   string   |   |   |
|   user\_level   |   string   |   |   |
|   itemid       |   string   |   |   |
|   num          |   bigint   |   |   |
|   get1         |   string   |   |   |
|   consume      |   string   |   |   |
|   detail       |   string   |   |   |
|   data\_day     |   string   |   |   |

# Sgsnew Silver Consume His 元宝消耗表（商城购买）

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id       |   string   |   |   |
|   user\_id      |   string   |   |   |
|   start\_time   |   string   |   |   |
|   user\_level   |   string   |   |   |
|   buy          |   string   |  购买礼包  |   |
|   itemid       |   string   |  礼包ID  |   |
|   item\_name    |   string   |  礼包名称  |   |
|   item\_type    |   string   |   |   |
|   num          |   bigint   |  购买数量  |   |
|   silver       |   bigint   |  消耗通元数  |   |
|   silver2      |   bigint   |  消耗绑元数  |   |
|   coin         |   bigint   |  消耗银两数  |   |
|   consume      |   string   |   |   |
|   data\_day     |   string   |   |   |

# Sgsnew Package Detail 近30日登录玩家背包数据

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id     |   string   |   |   |
|   user\_id    |   string   |   |   |
|   item\_id    |   string   |   |   |
|   item\_num   |   string   |   |   |
|   itemtype   |   int      |   |  4：武将 5：皮肤  |
|   level      |   string   |   |   |
|   grade      |   string   |   |  武将是否突破、皮肤是否升级动态  |
|   data\_day   |   string   |  仅保留每月1日的分区数据，为前30日的活跃用户包裹数据  |   |

# Sgsnew Times Event His 客户端点击埋点

|  字段名  |  类型  |  解释  |  枚举值  |
| --- | --- | --- | --- |
|   app\_id       |   string   |   |   |
|   device\_id    |   string   |   |   |
|   user\_id      |   string   |   |   |
|   start\_time   |   string   |   |   |
|   event\_id     |   string   |  事件ID  |  具体事件含义咨询客户端开发或策划同学  |
|   parameters   |   json   |  自定义参数  |   |
|   data\_day     |   string   |   |   |