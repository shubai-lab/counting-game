import pandas as pd
import json
import re

print('='*60)
print('武将品质分类 v2.0')
print('='*60)

# 1. 读取主表
df = pd.read_excel('sgs_general_conf.xlsx')
print(f'\n主表武将数: {len(df)}')

# 2. 读取获取途径表
operate_info = pd.read_excel('sgs_general_activity_operate_info.xlsx')
print(f'获取途径表: {len(operate_info)}条')

# 解析ActiveDropWay字段，提取途径ID
def parse_drop_way(drop_way):
    """解析获取途径，提取途径ID列表"""
    if pd.isna(drop_way):
        return [], []
    ways = []
    values = []
    drop_str = str(drop_way)
    # 匹配 "获取途径:1001 获取价值:500" 格式
    way_matches = re.findall(r'获取途径[：:](\d+)', drop_str)
    value_matches = re.findall(r'获取价值[：:](\d+)', drop_str)
    for w in way_matches:
        ways.append(int(w))
    for v in value_matches:
        values.append(int(v))
    return ways, values

# 测试解析
test_sample = operate_info['ActiveDropWay'].iloc[0]
print(f'测试解析: {test_sample}')
parsed = parse_drop_way(test_sample)
print(f'解析结果: {parsed}')

# 3. 读取将星价格表
jiangxing = pd.read_excel('sgs_item_goods_activity_conf.xlsx')
jiangxing_jiangxing = jiangxing[jiangxing['ShopType'] == '将星']
print(f'将星商品数: {len(jiangxing_jiangxing)}')

# 解析DropItemPack获取武将ID
def parse_drop_items(drop_pack):
    """从DropItemPack中提取武将道具ID"""
    if pd.isna(drop_pack):
        return []
    # 格式可能是 "10001,10002" 或其他格式
    items = str(drop_pack).split(',')
    result = []
    for item in items:
        item = item.strip()
        if item.isdigit():
            result.append(int(item))
    return result

# 4. 读取珍宝定价表
price_table = pd.read_excel('新三国杀道具定价表.xlsx')
print(f'珍宝定价表: {len(price_table)}条')

# 构建字典
operate_info_dict = {}
for _, row in operate_info.iterrows():
    gid = row['GeneralID']
    ways, values = parse_drop_way(row['ActiveDropWay'])
    operate_info_dict[gid] = {'ways': ways, 'values': values}

# 构建将星价格字典 (ItemID -> Price)
jiangxing_prices = {}
for _, row in jiangxing_jiangxing.iterrows():
    item_id = row['ItemID']
    price = row['Price']
    general_item_ids = parse_drop_items(row['DropItemPack'])
    for gid in general_item_ids:
        jiangxing_prices[gid] = price

# 构建珍宝定价字典 (item_id -> price)
price_dict = {}
for _, row in price_table.iterrows():
    item_id = row['item_id']
    price = row['price']
    try:
        if pd.notna(item_id) and pd.notna(price):
            price_dict[int(item_id)] = int(price)
    except (ValueError, TypeError):
        pass  # 跳过无效数据

print(f'\n数据准备完成:')
print(f'  获取途径武将: {len(operate_info_dict)}')
print(f'  将星价格道具: {len(jiangxing_prices)}')
print(f'  珍宝定价道具: {len(price_dict)}')

def classify_general(row, operate_info_dict, jiangxing_prices, price_dict):
    """按优先级对武将进行分类"""
    general_id = row['GeneralID']
    name = str(row['NamePrefix']) + str(row['GeneralName']) if pd.notna(row['NamePrefix']) else str(row['GeneralName'])
    lamp_type = str(row.get('LevelTwoGeneralLampType', ''))

    # 从operate_info获取获取途径
    if general_id in operate_info_dict:
        info = operate_info_dict[general_id]
        source_ways = info['ways']
    else:
        source_ways = []

    # === 第一优先级：固定档位来源 ===
    # LevelTwoGeneralLampType包含"武庙"或"高山仰止" → 限定
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
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
    item_id = row.get('GeneralItemId') or row.get('ShopItemId')
    if pd.notna(item_id):
        try:
            item_id = int(item_id)
        except (ValueError, TypeError):
            item_id = None
    if item_id and item_id in jiangxing_prices:
            price = jiangxing_prices[item_id]
            if price >= 10000:
                return '传说', f'将星价格{int(price)}', 'jiangxing'
            elif price >= 2000:
                return '史诗', f'将星价格{int(price)}', 'jiangxing'
            elif price >= 100:
                return '稀有', f'将星价格{int(price)}', 'jiangxing'
            elif price > 0:
                return '普通', f'将星价格{int(price)}', 'jiangxing'

    # === 第三优先级：珍宝定价 ===
    if item_id and item_id in price_dict:
        price = price_dict[item_id]
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

def safe_int(val):
    """安全转换为int"""
    if pd.isna(val):
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

# 执行分类
print('\n开始分类...')
results = []
for idx, row in df.iterrows():
    general_id = safe_int(row['GeneralID'])
    if general_id == 0:
        continue  # 跳过无效数据
    tier, reason, source = classify_general(row, operate_info_dict, jiangxing_prices, price_dict)
    name = str(row['NamePrefix']) + str(row['GeneralName']) if pd.notna(row['NamePrefix']) else str(row['GeneralName'])
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

# 待手动确认列表
print('\n' + '='*60)
print('待手动确认武将')
print('='*60)
manual = [r for r in results if r['tier'] == '待手动确认']
print(f'共 {len(manual)} 个待手动确认')
for r in manual:
    print(f"  ID:{r['general_id']} {r['name']} | {r['reason']}")

# 保存结果
output_path = 'classification_v2_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\n结果已保存到: {output_path}')