import pickle
import json
import pandas as pd

# 读取pkl文件
df = pd.read_pickle('temp_valid_generals_v2.pkl')

print(f'总武将数: {len(df)}')
print(f'字段列表: {df.columns.tolist()}')
print()

def classify_general(row):
    """按优先级对武将进行分类"""
    general_id = row['GeneralID']
    name = row['Name']
    lamp_type = str(row.get('LampType', ''))
    price = row.get('Price', 0)
    get_value = row.get('GetValue', 0)
    ways = row.get('Ways', '')
    operate_info = row.get('operate_info', '')
    source_ways = row.get('source_ways', [])
    source_names = row.get('source_names', [])

    # === 第一优先级：固定档位来源 ===
    # 1101高山仰止/1102武庙珍藏 → 限定
    if 1101 in source_ways or 1102 in source_ways:
        return '限定', '高山仰止/武庙珍藏', 'source_ways'
    if '高山仰止' in str(source_names) or '武庙' in str(source_names):
        return '限定', '高山仰止/武庙珍藏', 'source_names'

    # 1004祈福 → 传说
    if 1004 in source_ways:
        return '传说', '祈福', 'source_ways'
    if '祈福' in str(source_names):
        return '传说', '祈福', 'source_names'

    # 1001纳贤/5002神将任务/2000首充/2002充值奖励/2003累充奖励/3001山河令/1005星河宝箱 → 史诗
    epic_sources = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    if any(s in source_ways for s in epic_sources):
        return '史诗', '纳贤/神将任务/首充/充值奖励/累充/山河令/星河宝箱', 'source_ways'

    epic_names = ['纳贤', '神将任务', '首充', '充值奖励', '累充奖励', '山河令', '星河宝箱']
    if any(n in str(source_names) for n in epic_names):
        return '史诗', '纳贤/神将任务/首充/充值奖励/累充/山河令/星河宝箱', 'source_names'

    # LampType包含"武庙"或"高山仰止" → 限定
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    # === 第二优先级：将星价格 ===
    if pd.notna(price) and price >= 10000:
        return '传说', f'将星价格{int(price)}', 'price'
    if pd.notna(price) and 2000 <= price <= 9999:
        return '史诗', f'将星价格{int(price)}', 'price'
    if pd.notna(price) and 100 <= price <= 1999:
        return '稀有', f'将星价格{int(price)}', 'price'
    if pd.notna(price) and price > 0 and price < 100:
        return '普通', f'将星价格{int(price)}', 'price'

    # === 第三优先级：珍宝定价 ===
    if pd.notna(get_value) and get_value >= 200000:
        return '限定', f'珍宝定价{int(get_value)}', 'get_value'
    if pd.notna(get_value) and 100000 <= get_value <= 199999:
        return '传说', f'珍宝定价{int(get_value)}', 'get_value'
    if pd.notna(get_value) and 10000 <= get_value <= 99999:
        return '史诗', f'珍宝定价{int(get_value)}', 'price'
    if pd.notna(get_value) and 1001 <= get_value <= 9999:
        return '稀有', f'珍宝定价{int(get_value)}', 'get_value'
    if pd.notna(get_value) and get_value > 0 and get_value <= 1000:
        return '普通', f'珍宝定价{int(get_value)}', 'get_value'

    # === 第四优先级：待手动确认 ===
    return '待手动确认', f'price={price}, get_value={get_value}', 'unclassified'

# 执行分类
results = []
for _, row in df.iterrows():
    tier, reason, source = classify_general(row)
    results.append({
        'general_id': int(row['GeneralID']) if pd.notna(row['GeneralID']) else 0,
        'name': row['Name'],
        'tier': tier,
        'reason': reason,
        'source': source
    })

# 按档位统计
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print('=== 全量分类统计 ===')
for tier in ['限定', '传说', '史诗', '稀有', '普通', '待手动确认']:
    if tier in tier_counts:
        print(f'{tier}: {tier_counts[tier]}')

print()
print('=== 待手动确认武将 ===')
manual = [r for r in results if r['tier'] == '待手动确认']
print(f'共 {len(manual)} 个待手动确认')
for r in manual:
    print(f"  ID:{r['general_id']} {r['name']} | {r['reason']}")

# 保存结果
output_path = 'temp_classification_all.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print()
print(f'结果已保存到: {output_path}')