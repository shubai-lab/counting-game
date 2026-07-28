import pandas as pd
import json
import re

print('='*60)
print('武将品质分类 Final v5 (正确使用获取价值)')
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

# 4. 解析获取途径和获取价值
def parse_ways_and_values(text):
    """解析获取途径和获取价值"""
    if pd.isna(text):
        return {}, []
    drop_str = str(text)
    way_matches = re.findall(r'获取途径[：:](\d+)', drop_str)
    value_matches = re.findall(r'获取价值[：:](\d+)', drop_str)
    ways = [int(w) for w in way_matches]
    way_value = {}
    for i, w in enumerate(way_matches):
        way_id = int(w)
        value = int(value_matches[i]) if i < len(value_matches) else 0
        way_value[way_id] = value
    return way_value, ways

# 构建武将数据字典
general_data = {}
for _, row in df_valid.iterrows():
    gid = row['GeneralID']
    way_value, ways = parse_ways_and_values(row.get('GetValue', ''))

    # 如果主表没有，从operate_info表获取
    if not ways and gid in operate_info['GeneralID'].values:
        op_row = operate_info[operate_info['GeneralID'] == gid]
        if len(op_row) > 0:
            way_value, ways = parse_ways_and_values(op_row.iloc[0]['ActiveDropWay'])

    general_data[gid] = {
        'ways': ways,
        'way_value': way_value,
        'lamp_type': str(row.get('LevelTwoGeneralLampType', ''))
    }

print(f'\n数据准备完成:')
print(f'  有效武将: {len(general_data)}')

def get_price_by_way(gid, way_id):
    """获取指定途径的价格"""
    if gid in general_data:
        return general_data[gid]['way_value'].get(way_id, 0)
    return 0

def classify_general(general_id, name, lamp_type, general_data, dropway_names):
    data = general_data.get(general_id, {'ways': [], 'way_value': {}})
    source_ways = data['ways']

    # === 第一优先级：LevelTwoGeneralLampType ===
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    # 1102 → 武庙珍藏（限定）
    if 1102 in source_ways:
        return '限定', '武庙珍藏(1102)', 'operate_info'

    # 1101 → 宝玉兑换（按珍宝价格定档，见第三优先级）

    # 1004 → 传说
    if 1004 in source_ways:
        return '传说', '祈福', 'operate_info'

    # 1001/5002/2000/2002/2003/3001/1005 → 史诗
    epic_sources = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    if any(s in source_ways for s in epic_sources):
        matched = [dropway_names.get(s, str(s)) for s in source_ways if s in epic_sources]
        return '史诗', '/'.join(matched), 'operate_info'

    # === 第二优先级：将星(2)价格 ===
    if 2 in source_ways:
        price = get_price_by_way(general_id, 2)
        if price >= 10000:
            return '传说', f'jiangxing_price:{price}', 'jiangxing'
        elif price >= 2000:
            return '史诗', f'jiangxing_price:{price}', 'jiangxing'
        elif price >= 100:
            return '稀有', f'jiangxing_price:{price}', 'jiangxing'
        elif price > 0:
            return '普通', f'jiangxing_price:{price}', 'jiangxing'

    # === 第三优先级：珍宝(1003)/宝玉兑换(1101)价格 ===
    # 珍宝(1003)
    if 1003 in source_ways:
        price = get_price_by_way(general_id, 1003)
        if price >= 200000:
            return '限定', f'珍宝(1003)价格:{price}', 'zhenbao'
        elif price >= 100000:
            return '传说', f'珍宝(1003)价格:{price}', 'zhenbao'
        elif price >= 10000:
            return '史诗', f'珍宝(1003)价格:{price}', 'zhenbao'
        elif price >= 1001:
            return '稀有', f'珍宝(1003)价格:{price}', 'zhenbao'
        elif price > 0:
            return '普通', f'珍宝(1003)价格:{price}', 'zhenbao'

    # 宝玉兑换(1101)
    if 1101 in source_ways:
        price = get_price_by_way(general_id, 1101)
        if price >= 200000:
            return '限定', f'宝玉兑换(1101)价格:{price}', 'baoyu'
        elif price >= 100000:
            return '传说', f'宝玉兑换(1101)价格:{price}', 'baoyu'
        elif price >= 10000:
            return '史诗', f'宝玉兑换(1101)价格:{price}', 'baoyu'
        elif price >= 1001:
            return '稀有', f'宝玉兑换(1101)价格:{price}', 'baoyu'
        elif price > 0:
            return '普通', f'宝玉兑换(1101)价格:{price}', 'baoyu'

    # === 第四优先级：包含普通招募(1)的都归为普通 ===
    if 1 in source_ways:
        return '普通', f'包含普通招募{ways}', 'normal_recruit'

    # === 第五优先级：其他固定档位途径 ===
    # 稀有档途径
    rare_ways = [12, 103, 28, 21, 13, 102, 27, 25, 24, 23, 2004]  # 界限突破/活动大盒/会员商城/碎片商城/团购
    for w in rare_ways:
        if w in source_ways:
            name = dropway_names.get(w, str(w))
            return '稀有', f'{name}({w})', 'operate_info'

    # 史诗档途径
    epic_other_ways = [5003, 101]  # 移动商城/礼包商城
    for w in epic_other_ways:
        if w in source_ways:
            name = dropway_names.get(w, str(w))
            return '史诗', f'{name}({w})', 'operate_info'

    # === 第六优先级：待手动确认 ===
    return '待手动确认', f'ways={ways}', 'unclassified'

# 执行分类
print('\n开始分类...')
results = []
for _, row in df_valid.iterrows():
    general_id = row['GeneralID']
    name = str(row['NamePrefix']) + str(row['GeneralName']) if pd.notna(row['NamePrefix']) else str(row['GeneralName'])
    lamp_type = str(row.get('LevelTwoGeneralLampType', ''))

    tier, reason, source = classify_general(general_id, name, lamp_type, general_data, dropway_names)
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
for r in manual[:20]:
    print(f"  ID:{r['general_id']} {r['name']} | {r['reason']}")
if len(manual) > 20:
    print(f'  ... 还有 {len(manual)-20} 个')

# 保存结果
output_path = 'classification_final5_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\n结果已保存到: {output_path}')