# -*- coding: utf-8 -*-
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("武将品质重新划分 v22 (修正版)")
print("=" * 60)

# ========== 1. 读取数据 ==========
print("\n读取数据...")

# sgs_general_conf
df_raw = pd.read_excel('武将评级划分/data/sgs_general_conf.xlsx', header=None)
general = df_raw.iloc[4:].copy()
general.columns = df_raw.iloc[0].tolist()

# sgs_general_activity_operate_info
df_raw2 = pd.read_excel('武将评级划分/data/sgs_general_activity_operate_info.xlsx', header=None)
activity_info = df_raw2.iloc[4:].copy()
activity_info.columns = ['GeneralID', 'GeneralName', 'ActiveDropWay', 'SpecialDescription']

# 将星商品表
jiangxing = pd.read_excel('武将评级划分/data/sgs_item_goods_activity_conf.xlsx')

print(f"武将基础表: {len(general)} 行")
print(f"获取方式详情: {len(activity_info)} 行")

# ========== 2. 获取途径ID映射（修正版） ==========
way_names = {
    1: '普通招募', 2: '将星招募',
    11: '官阶商店', 12: '官阶商店', 13: '官阶商店', 14: '国士商店',
    21: '会员', 22: '官阶', 23: '武将收集',
    24: '官阶', 25: '官阶', 26: '官阶', 27: '官阶', 28: '官阶奖励',
    101: '烽火连天', 102: '斗地主', 103: '武将列传',
    1001: '纳贤', 1002: '如意签', 1003: '珍宝', 1004: '祈福', 1005: '星河璀璨',
    1101: '高山仰止', 1102: '武庙珍藏',
    2000: '首充', 2001: '杂谈', 2002: '充值', 2003: '充值', 2004: '连连看',
    3001: '山河令', 3002: '战令', 3003: '战令',
    4001: '神将兑换',
    5001: '2v2排位', 5002: '神将任务', 5003: '移动端', 5004: '运营', 5005: '运营', 5006: '运营', 5007: '运营',
}

# ========== 3. 建立数据映射 ==========
id_to_getvalue = {}
for _, row in general.iterrows():
    if pd.notna(row['LevelTwoGeneralLampType']):
        id_to_getvalue[row['GeneralID']] = row['GetValue']

id_to_active = {}
for _, row in activity_info.iterrows():
    id_to_active[row['GeneralID']] = row['ActiveDropWay']

# ========== 4. 解析获取途径 ==========
def parse_ways(get_value, active_drop_way):
    ways_values = {}

    # 先尝试GetValue
    if pd.notna(get_value):
        parts = str(get_value).split(';')
        for part in parts:
            part = part.strip()
            way_match = re.search(r'获取途径[:：](\d+)', part)
            value_match = re.search(r'获取价值[:：](\d+)', part)
            if way_match and value_match:
                way_id = int(way_match.group(1))
                value = int(value_match.group(1))
                if way_id not in ways_values or ways_values[way_id] < value:
                    ways_values[way_id] = value

    # 如果为空，使用ActiveDropWay
    if not ways_values and pd.notna(active_drop_way):
        parts = str(active_drop_way).split(';')
        for part in parts:
            part = part.strip()
            way_match = re.search(r'获取途径[:：](\d+)', part)
            value_match = re.search(r'获取价值[:：](\d+)', part)
            if way_match and value_match:
                way_id = int(way_match.group(1))
                value = int(value_match.group(1))
                if way_id not in ways_values or ways_values[way_id] < value:
                    ways_values[way_id] = value

    return ways_values

# ========== 5. 获取将星价格 ==========
def get_jiangxing_price(general_id):
    jx = jiangxing[jiangxing['ShopType'] == '将星']
    for _, row in jx.iterrows():
        if str(general_id) in str(row['DropItemPack']):
            return row['Price']
    return 0

# ========== 6. 档位划分 ==========
def classify(general_id, ways_values, jx_price):
    """按档位优先级划分（新规则）"""
    # 提取各类型价格
    zb_price = ways_values.get(1003, 0)  # 珍宝(1003)
    qifu_price = ways_values.get(1004, 0)  # 祈福(1004)
    naxian_price = ways_values.get(1001, 0)  # 纳贤(1001)
    shenjiang_price = ways_values.get(5002, 0)  # 神将任务(5002)
    operate_prices = [ways_values.get(w, 0) for w in [5001,5003,5004,5005,5006,5007]]
    operate_price = max(operate_prices) if operate_prices else 0

    # 1. 限定：珍宝>=2000 或 高山仰止(1101)
    if zb_price >= 2000:
        return '限定', f'珍宝>=20万({zb_price})'
    if 1101 in ways_values:
        return '限定', '高山仰止'

    # 2. 传说：祈福（固定档）或 运营>=2000 或 将星>=10000
    if 1004 in ways_values:  # 祈福（固定传说档）
        return '传说', f'祈福({qifu_price})'
    if operate_price >= 2000:
        return '传说', f'运营>=20万({operate_price})'
    if jx_price >= 10000:
        return '传说', f'将星>=1万({jx_price})'

    # 3. 史诗：纳贤（固定档）或 神将任务 或 珍宝10~20万 或 运营10~20万 或 将星2000~9999
    if 1001 in ways_values:  # 纳贤（固定史诗档）
        return '史诗', f'纳贤({naxian_price})'
    if 5002 in ways_values:  # 神将任务（固定史诗档）
        return '史诗', f'神将任务({shenjiang_price})'
    if zb_price >= 1000 and zb_price < 2000:
        return '史诗', f'珍宝10~20万({zb_price})'
    if operate_price >= 1000 and operate_price < 2000:
        return '史诗', f'运营10~20万({operate_price})'
    if jx_price >= 2000 and jx_price < 10000:
        return '史诗', f'将星2000~9999({jx_price})'

    # 4. 稀有：将星100~2000 或 珍宝5~10万 或 运营1001~10万
    if jx_price >= 100 and jx_price < 2000:
        return '稀有', f'将星100~2000({jx_price})'
    if zb_price >= 500 and zb_price < 1000:
        return '稀有', f'珍宝5~10万({zb_price})'
    if operate_price >= 100 and operate_price < 1000:
        return '稀有', f'运营1001~10万({operate_price})'

    # 5. 普通：将星<100
    if jx_price > 0 and jx_price < 100:
        return '普通', f'将星<100({jx_price})'

    # 6. 普通：其他
    return '普通', '其他'

# ========== 7. 处理武将 ==========
valid = general[general['LevelTwoGeneralLampType'].notna()].copy()
print(f"有效武将数量: {len(valid)}")

results = []
for _, row in valid.iterrows():
    gid = row['GeneralID']
    prefix = row['NamePrefix']
    name_val = row['GeneralName']
    full_name = (str(prefix) if pd.notna(prefix) and str(prefix) != 'nan' else '') + str(name_val)

    get_value = id_to_getvalue.get(gid)
    active_drop_way = id_to_active.get(gid)
    ways_values = parse_ways(get_value, active_drop_way)
    jx_price = get_jiangxing_price(gid)
    tier, reason = classify(gid, ways_values, jx_price)

    results.append({
        'GeneralID': gid,
        '武将名称': full_name,
        '获取途径': str(list(ways_values.keys())),
        '获取价值': str(list(ways_values.values())),
        '将星价格': jx_price,
        '品质': tier,
        '划分依据': reason
    })

df_result = pd.DataFrame(results)

# ========== 8. 统计 ==========
print("\n=== v22 档位分布 ===")
dist = df_result['品质'].value_counts()
total = len(df_result)
for q in ['限定', '传说', '史诗', '稀有', '普通']:
    if q in dist:
        count = dist[q]
        pct = count / total * 100
        print(f"{q}: {count} ({pct:.1f}%)")

print(f"\n总计: {total} 武将")

# ========== 9. 详细统计 ==========
print("\n=== 详细统计 ===")
for tier in ['限定', '传说', '史诗', '稀有', '普通']:
    tier_data = df_result[df_result['品质'] == tier]
    print(f"\n{tier} ({len(tier_data)}个):")
    for reason, count in tier_data['划分依据'].value_counts().head(5).items():
        print(f"  {reason}: {count}")

# ========== 10. 保存 ==========
df_result.to_excel('武将评级划分/data/武将评级完整名单_v22.xlsx', index=False)
print("\n已保存: 武将评级划分/data/武将评级完整名单_v22.xlsx")

dist_df = pd.DataFrame({
    '品质': ['限定', '传说', '史诗', '稀有', '普通'],
    '数量': [dist.get('限定', 0), dist.get('传说', 0), dist.get('史诗', 0), dist.get('稀有', 0), dist.get('普通', 0)],
    '占比': [f"{dist.get('限定', 0)/total*100:.1f}%", f"{dist.get('传说', 0)/total*100:.1f}%",
             f"{dist.get('史诗', 0)/total*100:.1f}%", f"{dist.get('稀有', 0)/total*100:.1f}%",
             f"{dist.get('普通', 0)/total*100:.1f}%"]
})
dist_df.to_excel('武将评级划分/data/武将评级分布汇总_v22.xlsx', index=False)
print("已保存: 武将评级划分/data/武将评级分布汇总_v22.xlsx")
