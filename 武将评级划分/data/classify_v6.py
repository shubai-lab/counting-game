import pandas as pd
import json
import re

print('='*60)
print('武将品质分类 v6.0')
print('='*60)

# 1. 读取主表
df = pd.read_excel('sgs_general_conf.xlsx')
df = df.iloc[2:].reset_index(drop=True)
df['GeneralID'] = pd.to_numeric(df['GeneralID'], errors='coerce')
print(f'\n主表武将数: {len(df)}')

# 2. 读取获取途径表 (sgs_general_activity_operate_info)
operate_info = pd.read_excel('sgs_general_activity_operate_info.xlsx')
print(f'获取途径详情表: {len(operate_info)}条')

# 3. 读取获取途径定义表 (sgs_general_activity_operate)
operate = pd.read_excel('sgs_general_activity_operate.xlsx')
operate = operate.iloc[3:].reset_index(drop=True)  # 跳过前3行描述
operate['DropWayID'] = pd.to_numeric(operate['DropWayID'], errors='coerce')
# 构建DropWayID ->名称 的映射
dropway_names = {}
for _, row in operate.iterrows():
    if pd.notna(row['DropWayID']):
        dropway_names[int(row['DropWayID'])] = row['DropWayName']
print(f'获取途径定义: {len(dropway_names)}条')

# 解析GetValue或ActiveDropWay字段，提取途径ID
def parse_get_value(text):
    """解析获取途径，提取途径ID列表"""
    if pd.isna(text):
        return []
    ways = []
    drop_str = str(text)
    # 匹配 "获取途径:1001" 格式
    way_matches = re.findall(r'获取途径[：:](\d+)', drop_str)
    for w in way_matches:
        ways.append(int(w))
    return ways

# 构建武将ID -> 获取途径列表 的映射
general_ways = {}
for _, row in df.iterrows():
    gid = row['GeneralID']
    if pd.isna(gid):
        continue
    gid = int(gid)

    #优先使用主表GetValue
    get_value = row.get('GetValue', '')
    ways = parse_get_value(get_value)

    # 如果主表没有，到operate_info表查找
    if not ways and gid in operate_info['GeneralID'].values:
        operate_row = operate_info[operate_info['GeneralID'] == gid]
        if len(operate_row) > 0:
            active_drop_way = operate_row.iloc[0]['ActiveDropWay']
            ways = parse_get_value(active_drop_way)

    if ways:
        general_ways[gid] = ways

print(f'有获取途径的武将: {len(general_ways)}')

# 4. 读取珍宝定价表
price_table = pd.read_excel('新三国杀道具定价表.xlsx')
price_table = price_table.iloc[2:].reset_index(drop=True)
price_table['item_id'] = pd.to_numeric(price_table['item_id'], errors='coerce')
price_table['price'] = pd.to_numeric(price_table['price'], errors='coerce')

# 读取武将道具表，建立GeneralID -> ItemID -> 珍宝定价 的映射
item_conf = pd.read_excel('sgs_item_general_conf.xlsx')
item_conf = item_conf.iloc[2:].reset_index(drop=True)
item_conf['GeneralID'] = pd.to_numeric(item_conf['GeneralID'], errors='coerce')
item_conf['ItemID'] = pd.to_numeric(item_conf['ItemID'], errors='coerce')

# 建立 GeneralID -> 珍宝定价 的映射
price_dict = {}
for _, row in item_conf.iterrows():
    gid = row['GeneralID']
    item_id = row['ItemID']
    if pd.notna(gid) and pd.notna(item_id):
        matched = price_table[price_table['item_id'] == int(item_id)]
        if len(matched) > 0:
            p = matched.iloc[0]['price']
            if pd.notna(p) and p > 0:
                price_dict[int(gid)] = int(p)

print(f'珍宝定价关联武将: {len(price_dict)}')

# 5. 读取将星价格表
jiangxing = pd.read_excel('sgs_item_goods_activity_conf.xlsx')
jiangxing_jiangxing = jiangxing[jiangxing['ShopType'] == '将星']
print(f'将星商品数: {len(jiangxing_jiangxing)}')

# 构建道具ID -> 将星价格 的映射
jiangxing_price_by_item = {}
for _, row in jiangxing_jiangxing.iterrows():
    item_id = row['ItemID']
    price = row['Price']
    if pd.notna(item_id) and pd.notna(price):
        jiangxing_price_by_item[int(item_id)] = int(price)

# 建立 GeneralID -> 将星价格 的映射
jiangxing_prices = {}
for _, row in item_conf.iterrows():
    gid = row['GeneralID']
    item_id = row['ItemID']
    if pd.notna(gid) and pd.notna(item_id):
        if int(item_id) in jiangxing_price_by_item:
            jiangxing_prices[int(gid)] = jiangxing_price_by_item[int(item_id)]

print(f'将星价格关联武将: {len(jiangxing_prices)}')

print(f'\n数据准备完成:')
print(f'  获取途径武将: {len(general_ways)}')
print(f'  将星价格武将: {len(jiangxing_prices)}')
print(f'  珍宝定价武将: {len(price_dict)}')

def classify_general(general_id, name, lamp_type, general_ways, jiangxing_prices, price_dict, dropway_names):
    """按优先级对武将进行分类"""
    source_ways = general_ways.get(general_id, [])

    # === 第一优先级：LevelTwoGeneralLampType ===
    if '武庙' in str(lamp_type) or '高山仰止' in str(lamp_type):
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    # === 第一优先级：固定档位来源 ===
    if 1101 in source_ways or 1102 in source_ways:
        return '限定', '高山仰止/武庙珍藏', 'operate_info'

    if 1004 in source_ways:
        return '传说', '祈福', 'operate_info'

    epic_sources = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    if any(s in source_ways for s in epic_sources):
        matched = [dropway_names.get(s, str(s)) for s in source_ways if s in epic_sources]
        return '史诗', '/'.join(matched), 'operate_info'

    # === 第二优先级：将星价格 ===
    if general_id in jiangxing_prices:
        price = jiangxing_prices[general_id]
        if price >= 10000:
            return '传说', f'将星价格{int(price)}', 'jiangxing'
        elif price >= 2000:
            return '史诗', f'将星价格{int(price)}', 'jiangxing'
        elif price >= 100:
            return '稀有', f'将星价格{int(price)}', 'jiangxing'
        elif price > 0:
            return '普通', f'将星价格{int(price)}', 'jiangxing'

    # === 第三优先级：珍宝定价 ===
    if general_id in price_dict:
        price = price_dict[general_id]
        if price >= 200000:
            return '限定', f'珍宝定价{int(price)}', 'price_table'
        elif price >= 100000:
            return '传说', f'珍宝定价{int(price)}', 'price_table'
        elif price >= 10000:
            return '史诗', f'珍宝定价{int(price)}', 'price_table'
        elif price >= 1001:
            return '稀有', f'珍宝定价{int(price)}', 'price_table'
        elif price > 0:
            return '普通', f'珍宝定价{int(price)}', 'price_table'

    # === 第四优先级：待手动确认 ===
    return '待手动确认', f'source_ways={source_ways}', 'unclassified'

# 执行分类
print('\n开始分类...')
results = []
for _, row in df.iterrows():
    general_id = row['GeneralID']
    if pd.isna(general_id):
        continue
    general_id = int(general_id)
    name = str(row['NamePrefix']) + str(row['GeneralName']) if pd.notna(row['NamePrefix']) else str(row['GeneralName'])
    lamp_type = str(row.get('LevelTwoGeneralLampType', ''))

    tier, reason, source = classify_general(general_id, name, lamp_type, general_ways, jiangxing_prices, price_dict, dropway_names)
    results.append({
        'general_id': general_id,
        'name': name,
        'tier': tier,
        'reason': reason,
        'source': source
    })

# 统计
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print('\n' + '='*60)
print('分类统计')
print('='*60)
for tier in ['限定', '传说', '史诗', '稀有', '普通', '待手动确认']:
    if tier in tier_counts:
        print(f'{tier}: {tier_counts[tier]}')
print(f'总计: {len(results)}')

# 待手动确认列表
print('\n' + '='*60)
print('待手动确认武将')
print('='*60)
manual = [r for r in results if r['tier'] == '待手动确认']
print(f'共 {len(manual)} 个待手动确认')
for r in manual[:50]:
    print(f"  ID:{r['general_id']} {r['name']} | {r['reason']}")
if len(manual) > 50:
    print(f'  ... 还有 {len(manual)-50} 个')

# 保存结果
output_path = 'classification_v6_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\n结果已保存到: {output_path}')