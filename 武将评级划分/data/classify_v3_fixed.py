import pandas as pd
import json
import re

print('='*60)
print('武将品质分类 v3.0 (v2.1分类逻辑 - 修正版)')
print('='*60)

# 1. 读取主表
df = pd.read_excel('sgs_general_conf.xlsx')
df = df.iloc[2:].reset_index(drop=True)
df['GeneralID'] = pd.to_numeric(df['GeneralID'], errors='coerce')
df_valid = df[df['LevelTwoGeneralLampType'].notna() & df['GeneralID'].notna()].copy()
df_valid['GeneralID'] = df_valid['GeneralID'].astype(int)
print(f'\n主表有效武将数: {len(df_valid)}')

# 2. 读取获取途径详情表 (主要数据源)
operate_info = pd.read_excel('sgs_general_activity_operate_info.xlsx')
print(f'获取途径详情表: {len(operate_info)}条')

# 3. 解析获取途径和获取价值
def parse_ways_and_values(text):
    """解析获取途径和获取价值，返回 {途径ID: 获取价值} 字典"""
    if pd.isna(text):
        return {}
    drop_str = str(text)
    way_matches = re.findall(r'获取途径[：:](\d+)', drop_str)
    value_matches = re.findall(r'获取价值[：:](\d+)', drop_str)
    result = {}
    for i, w in enumerate(way_matches):
        way_id = int(w)
        value = int(value_matches[i]) if i < len(value_matches) else 0
        result[way_id] = value
    return result

# 构建武将数据字典
general_data = {}
for _, row in df_valid.iterrows():
    gid = row['GeneralID']
    way_value = parse_ways_and_values(row.get('GetValue', ''))

    # 如果主表没有，从operate_info表获取
    if not way_value and gid in operate_info['GeneralID'].values:
        op_row = operate_info[operate_info['GeneralID'] == gid]
        if len(op_row) > 0:
            way_value = parse_ways_and_values(op_row.iloc[0]['ActiveDropWay'])

    general_data[gid] = {
        'ways': list(way_value.keys()),
        'way_value': way_value,
        'lamp_type': str(row.get('LevelTwoGeneralLampType', ''))
    }

print(f'数据准备完成: 有效武将 {len(general_data)}')
has_ways = sum(1 for g in general_data.values() if g['ways'])
print(f'有获取途径的武将: {has_ways}')

def classify_general(general_id, name, lamp_type, data):
    """按v2.1分类逻辑对武将进行分类"""
    source_ways = data['ways']
    way_value = data['way_value']

    def get_price(way_id):
        return way_value.get(way_id, 0)

    # === 优先级1: 武庙/高山仰止/威前缀 → 限定（固定）===
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    if '威' in lamp_type and lamp_type.startswith('威'):
        return '限定', f'LampType威前缀({lamp_type})', 'lamp_type'

    # === 优先级2: 祈福(1004) → 传说（固定）===
    if 1004 in source_ways:
        return '传说', '祈福(1004)', 'operate_info'

    # === 优先级3: 纳贤(1001)/神将任务(5002) → 史诗（固定）===
    if 1001 in source_ways:
        return '史诗', '纳贤(1001)', 'operate_info'
    if 5002 in source_ways:
        return '史诗', '神将任务(5002)', 'operate_info'

    # === 优先级4: 将星招募(2)价格 → 按阈值判断 ===
    # 价格阈值：≥9999传说, 2000~9998史诗, 100~1999稀有, <100普通
    if 2 in source_ways:
        price = get_price(2)
        if price >= 9999:
            return '传说', f'jiangxing_price:{price}', 'jiangxing'
        elif price >= 2000:
            return '史诗', f'jiangxing_price:{price}', 'jiangxing'
        elif price >= 100:
            return '稀有', f'jiangxing_price:{price}', 'jiangxing'
        elif price > 0:
            return '普通', f'jiangxing_price:{price}', 'jiangxing'

    # === 优先级5: 宝玉兑换(1101) → 按价格阈值判断 ===
    if 1101 in source_ways:
        price = get_price(1101)
        if price >= 10000:
            return '史诗', f'宝玉兑换(1101)价格:{price}', 'baoyu'
        elif price >= 1000:
            return '稀有', f'宝玉兑换(1101)价格:{price}', 'baoyu'
        else:
            return '普通', f'宝玉兑换(1101)价格:{price}', 'baoyu'

    # === 优先级6: 珍宝(1003) → 稀有（固定）===
    if 1003 in source_ways:
        return '稀有', '珍宝(1003)', 'zhenbao'

    # === 优先级7: 普通招募(1) → 普通 ===
    if 1 in source_ways:
        return '普通', '普通招募(1)', 'normal_recruit'

    # === 优先级8: LampType特殊分类 ===
    if '无双上将' in lamp_type:
        return '史诗', '无双上将', 'lamp_type'

    if '界限突破' in lamp_type:
        return '稀有', '界限突破', 'lamp_type'

    # === 优先级9: 待手动确认 ===
    return '待手动确认', f'ways={source_ways}', 'unclassified'

# 执行分类
print('\n开始分类...')
results = []
for _, row in df_valid.iterrows():
    general_id = row['GeneralID']
    name = str(row['NamePrefix']) + str(row['GeneralName']) if pd.notna(row['NamePrefix']) else str(row['GeneralName'])
    lamp_type = str(row.get('LevelTwoGeneralLampType', ''))
    data = general_data[general_id]

    tier, reason, source = classify_general(general_id, name, lamp_type, data)
    jiangxing_price = data['way_value'].get(2, 0)

    results.append({
        'general_id': general_id,
        'name': name,
        'tier': tier,
        'reason': reason,
        'source': source,
        'jiangxing_price': jiangxing_price
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
output_path = 'classification_v3_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'\n结果已保存到: {output_path}')