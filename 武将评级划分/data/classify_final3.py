import pandas as pd
import json
import re

print('='*60)
print('武将品质分类 Final v3')
print('='*60)

# 1. 读取主表并正确过滤
df = pd.read_excel('sgs_general_conf.xlsx')
df = df.iloc[2:].reset_index(drop=True)
df['GeneralID'] = pd.to_numeric(df['GeneralID'], errors='coerce')
df_valid = df[df['LevelTwoGeneralLampType'].notna() & df['GeneralID'].notna()].copy()
df_valid['GeneralID'] = df_valid['GeneralID'].astype(int)
print(f'\n有效武将数: {len(df_valid)}')

# 2. 读取获取途径详情表
operate_info = pd.read_excel('sgs_general_activity_operate_info.xlsx')
print(f'获取途径详情表: {len(operate_info)}条')

# 3. 读取获取途径定义表
operate = pd.read_excel('sgs_general_activity_operate.xlsx')
operate = operate.iloc[3:].reset_index(drop=True)
operate['DropWayID'] = pd.to_numeric(operate['DropWayID'], errors='coerce')
dropway_names = {}
for _, row in operate.iterrows():
    if pd.notna(row['DropWayID']):
        dropway_names[int(row['DropWayID'])] = row['DropWayName']
print(f'获取途径定义: {len(dropway_names)}条')

# 4. 读取将星价格表
jiangxing = pd.read_excel('sgs_item_goods_activity_conf.xlsx')
jiangxing_jiangxing = jiangxing[jiangxing['ShopType'] == '将星']
print(f'将星商品数: {len(jiangxing_jiangxing)}')

def parse_drop_item_pack(text):
    if pd.isna(text):
        return []
    drop_str = str(text)
    matches = re.findall(r'(\d{6})', drop_str)
    return [int(m) for m in matches]

jiangxing_prices = {}
for _, row in jiangxing_jiangxing.iterrows():
    general_ids = parse_drop_item_pack(row['DropItemPack'])
    price = row['Price']
    for gid in general_ids:
        if pd.notna(price) and price > 0:
            jiangxing_prices[gid] = int(price)
print(f'将星价格关联武将: {len(jiangxing_prices)}')

# 5. 解析获取途径(含珍宝价格)
def parse_ways_and_values(text):
    if pd.isna(text):
        return [], {}
    drop_str = str(text)
    way_matches = re.findall(r'获取途径[：:](\d+)', drop_str)
    value_matches = re.findall(r'获取价值[：:](\d+)', drop_str)
    ways = [int(w) for w in way_matches]
    way_value = {}
    for i, w in enumerate(way_matches):
        way_id = int(w)
        value = int(value_matches[i]) if i < len(value_matches) else 0
        way_value[way_id] = value
    return ways, way_value

# 构建获取途径字典和珍宝价格字典
general_ways = {}
general_zhenbao_prices = {}
for _, row in df_valid.iterrows():
    gid = row['GeneralID']
    ways, way_value = parse_ways_and_values(row.get('GetValue', ''))

    # 如果主表没有，从operate_info表获取
    if not ways and gid in operate_info['GeneralID'].values:
        op_row = operate_info[operate_info['GeneralID'] == gid]
        if len(op_row) > 0:
            ways, way_value = parse_ways_and_values(op_row.iloc[0]['ActiveDropWay'])

    general_ways[gid] = ways
    if 1003 in ways:
        general_zhenbao_prices[gid] = way_value.get(1003, 0)

print(f'有获取途径的武将: {len(general_ways)}')
print(f'珍宝1003武将: {len(general_zhenbao_prices)}')

print(f'\n数据准备完成:')
print(f'  有效武将: {len(df_valid)}')
print(f'  获取途径武将: {len(general_ways)}')
print(f'  将星价格武将: {len(jiangxing_prices)}')
print(f'  珍宝1003武将: {len(general_zhenbao_prices)}')

def classify_general(general_id, name, lamp_type, general_ways, jiangxing_prices, general_zhenbao_prices, dropway_names):
    source_ways = general_ways.get(general_id, [])

    # === 第一优先级：LevelTwoGeneralLampType ===
    if '武庙' in str(lamp_type) or '高山仰止' in str(lamp_type):
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    # 1101/1102 → 限定
    if 1101 in source_ways or 1102 in source_ways:
        return '限定', '高山仰止/武庙珍藏', 'operate_info'

    # 1004 → 传说
    if 1004 in source_ways:
        return '传说', '祈福', 'operate_info'

    # 1001/5002/2000/2002/2003/3001/1005 → 史诗
    epic_sources = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    if any(s in source_ways for s in epic_sources):
        matched = [dropway_names.get(s, str(s)) for s in source_ways if s in epic_sources]
        return '史诗', '/'.join(matched), 'operate_info'

    # === 第二优先级：将星价格 ===
    if general_id in jiangxing_prices:
        price = jiangxing_prices[general_id]
        if price >= 10000:
            return '传说', f'jiangxing_price:{int(price)}', 'jiangxing'
        elif price >= 2000:
            return '史诗', f'jiangxing_price:{int(price)}', 'jiangxing'
        elif price >= 100:
            return '稀有', f'jiangxing_price:{int(price)}', 'jiangxing'
        elif price > 0:
            return '普通', f'jiangxing_price:{int(price)}', 'jiangxing'

    # === 第三优先级：珍宝1003价格 ===
    if 1003 in source_ways and general_id in general_zhenbao_prices:
        price = general_zhenbao_prices[general_id]
        if price >= 200000:
            return '限定', f'zhenbao_price:{int(price)}', 'zhenbao'
        elif price >= 100000:
            return '传说', f'zhenbao_price:{int(price)}', 'zhenbao'
        elif price >= 10000:
            return '史诗', f'zhenbao_price:{int(price)}', 'zhenbao'
        elif price >= 1001:
            return '稀有', f'zhenbao_price:{int(price)}', 'zhenbao'
        elif price > 0:
            return '普通', f'zhenbao_price:{int(price)}', 'zhenbao'

    # === 第四优先级：包含普通招募(1)的都归为普通 ===
    if 1 in source_ways:
        return '普通', f'包含普通招募{ways}', 'normal_recruit'

    # === 第五优先级：待手动确认 ===
    return '待手动确认', f'ways={source_ways}', 'unclassified'

# 执行分类
print('\n开始分类...')
results = []
for _, row in df_valid.iterrows():
    general_id = row['GeneralID']
    name = str(row['NamePrefix']) + str(row['GeneralName']) if pd.notna(row['NamePrefix']) else str(row['GeneralName'])
    lamp_type = str(row.get('LevelTwoGeneralLampType', ''))

    tier, reason, source = classify_general(general_id, name, lamp_type, general_ways, jiangxing_prices, general_zhenbao_prices, dropway_names)
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
for r in manual[:30]:
    print(f"  ID:{r['general_id']} {r['name']} | {r['reason']}")
if len(manual) > 30:
    print(f'  ... 还有 {len(manual)-30} 个')

# 保存结果
output_path = 'classification_final3_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\n结果已保存到: {output_path}')