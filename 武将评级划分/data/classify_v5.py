import pandas as pd
import json
import re

print('='*60)
print('武将品质分类 v5.0 (正确逻辑)')
print('='*60)

# 1. 读取主表
df = pd.read_excel('sgs_general_conf.xlsx')
df = df.iloc[2:].reset_index(drop=True)
df['GeneralID'] = pd.to_numeric(df['GeneralID'], errors='coerce')
print(f'\n主表武将数: {len(df)}')

# 2. 读取获取途径表
operate_info = pd.read_excel('sgs_general_activity_operate_info.xlsx')
print(f'获取途径表: {len(operate_info)}条')

def parse_drop_way(drop_way):
    if pd.isna(drop_way):
        return [], []
    ways = []
    values = []
    drop_str = str(drop_way)
    way_matches = re.findall(r'获取途径[：:](\d+)', drop_str)
    value_matches = re.findall(r'获取价值[：:](\d+)', drop_str)
    for w in way_matches:
        ways.append(int(w))
    for v in value_matches:
        values.append(int(v))
    return ways, values

# 3. 读取将星价格表 (通过道具ID关联)
jiangxing = pd.read_excel('sgs_item_goods_activity_conf.xlsx')
jiangxing_jiangxing = jiangxing[jiangxing['ShopType'] == '将星']
print(f'将星商品数: {len(jiangxing_jiangxing)}')

# 构建道具ID到将星价格的字典
jiangxing_price_by_item = {}
for _, row in jiangxing_jiangxing.iterrows():
    item_id = row['ItemID']
    price = row['Price']
    if pd.notna(item_id) and pd.notna(price):
        jiangxing_price_by_item[int(item_id)] = int(price)

# 读取武将道具表，建立 GeneralID -> ItemID 映射
item_conf = pd.read_excel('sgs_item_general_conf.xlsx')
item_conf = item_conf.iloc[2:].reset_index(drop=True)
item_conf['GeneralID'] = pd.to_numeric(item_conf['GeneralID'], errors='coerce')
item_conf['ItemID'] = pd.to_numeric(item_conf['ItemID'], errors='coerce')

# 建立 GeneralID -> 将星价格 的映射
jiangxing_prices = {}
for _, row in item_conf.iterrows():
    gid = row['GeneralID']
    item_id = row['ItemID']
    if pd.notna(gid) and pd.notna(item_id):
        if int(item_id) in jiangxing_price_by_item:
            jiangxing_prices[int(gid)] = jiangxing_price_by_item[int(item_id)]

print(f'将星价格关联武将: {len(jiangxing_prices)}')

# 4. 读取珍宝定价表，建立 GeneralID -> 珍宝价格 的映射
price_table = pd.read_excel('新三国杀道具定价表.xlsx')
price_table = price_table.iloc[2:].reset_index(drop=True)
price_table['item_id'] = pd.to_numeric(price_table['item_id'], errors='coerce')
price_table['price'] = pd.to_numeric(price_table['price'], errors='coerce')
price_table_valid = price_table[price_table['item_id'].notna() & price_table['price'].notna()]

# 通过ItemID关联珍宝定价
price_dict = {}
for _, row in item_conf.iterrows():
    gid = row['GeneralID']
    item_id = row['ItemID']
    if pd.notna(gid) and pd.notna(item_id):
        matched = price_table_valid[price_table_valid['item_id'] == int(item_id)]
        if len(matched) > 0:
            price_dict[int(gid)] = int(matched.iloc[0]['price'])

print(f'珍宝定价关联武将: {len(price_dict)}')

# 构建获取途径字典
operate_info_dict = {}
for _, row in operate_info.iterrows():
    gid = row['GeneralID']
    ways, values = parse_drop_way(row['ActiveDropWay'])
    operate_info_dict[gid] = {'ways': ways, 'values': values}

print(f'\n数据准备完成:')
print(f'  获取途径武将: {len(operate_info_dict)}')
print(f'  将星价格武将: {len(jiangxing_prices)}')
print(f'  珍宝定价武将: {len(price_dict)}')

def classify_general(general_id, name, lamp_type, operate_info_dict, jiangxing_prices, price_dict):
    """按优先级对武将进行分类"""
    # 从operate_info获取获取途径
    if general_id in operate_info_dict:
        info = operate_info_dict[general_id]
        source_ways = info['ways']
    else:
        source_ways = []

    # === 第一优先级：LevelTwoGeneralLampType ===
    # 武庙/高山仰止 → 限定
    if '武庙' in str(lamp_type) or '高山仰止' in str(lamp_type):
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    # ActiveDropWay中有1101/1102 → 限定
    if 1101 in source_ways or 1102 in source_ways:
        return '限定', '高山仰止/武庙珍藏', 'operate_info'

    # ActiveDropWay中有1004 → 传说
    if 1004 in source_ways:
        return '传说', '祈福', 'operate_info'

    # ActiveDropWay中有1001/5002/2000/2002/2003/3001/1005 → 史诗
    epic_sources = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    if any(s in source_ways for s in epic_sources):
        epic_names = {
            1001: '纳贤', 5002: '神将任务', 2000: '首充',
            2002: '充值奖励', 2003: '累充奖励', 3001: '山河令', 1005: '星河宝箱'
        }
        matched = [epic_names[s] for s in epic_sources if s in source_ways]
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

    tier, reason, source = classify_general(general_id, name, lamp_type, operate_info_dict, jiangxing_prices, price_dict)
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
output_path = 'classification_v5_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\n结果已保存到: {output_path}')