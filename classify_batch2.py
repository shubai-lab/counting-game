import pickle
import json

# 读取pkl文件
with open('temp_valid_generals_v2.pkl', 'rb') as f:
    data = pickle.load(f)

print(f'总武将数: {len(data)}')
print(f'字段列表: {list(data[0].keys())}')
print()

# 筛选 GeneralID 136-270
filtered = [g for g in data if 136 <= g['GeneralID'] <= 270]
print(f'筛选后武将数 (136-270): {len(filtered)}')

def classify_general(g):
    """按优先级对武将进行分类"""
    general_id = g['GeneralID']
    name = g['Name']
    lamp_type = g.get('LampType', '')
    price = g.get('Price', 0)
    get_value = g.get('GetValue', 0)
    ways = g.get('Ways', '')
    operate_info = g.get('operate_info', '')
    source_ways = g.get('source_ways', [])
    source_names = g.get('source_names', [])

    # 转换source_ways为字符串便于搜索
    source_ways_str = str(source_ways) if source_ways else ''

    # === 第一优先级：固定档位来源 ===
    # 1101高山仰止/1102武庙珍藏 → 限定
    if 1101 in source_ways or 1102 in source_ways:
        return '限定', '高山仰止/武庙珍藏', 'source_ways'
    if '高山仰止' in source_names or '武庙' in source_names:
        return '限定', '高山仰止/武庙珍藏', 'source_names'

    # 1004祈福 → 传说
    if 1004 in source_ways:
        return '传说', '祈福', 'source_ways'
    if '祈福' in source_names:
        return '传说', '祈福', 'source_names'

    # 1001纳贤/5002神将任务/2000首充/2002充值奖励/2003累充奖励/3001山河令/1005星河宝箱 → 史诗
    epic_sources = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    if any(s in source_ways for s in epic_sources):
        return '史诗', '纳贤/神将任务/首充/充值奖励/累充/山河令/星河宝箱', 'source_ways'

    epic_names = ['纳贤', '神将任务', '首充', '充值奖励', '累充奖励', '山河令', '星河宝箱']
    if any(n in str(source_names) for n in epic_names):
        return '史诗', '纳贤/神将任务/首充/充值奖励/累充/山河令/星河宝箱', 'source_names'

    # LampType包含"武庙"或"高山仰止" → 限定
    if '武庙' in str(lamp_type) or '高山仰止' in str(lamp_type):
        return '限定', 'LampType武庙/高山仰止', 'lamp_type'

    # === 第二优先级：将星价格 ===
    if price >= 10000:
        return '传说', f'将星价格{price}', 'price'
    if 2000 <= price <= 9999:
        return '史诗', f'将星价格{price}', 'price'
    if 100 <= price <= 1999:
        return '稀有', f'将星价格{price}', 'price'
    if price > 0 and price < 100:
        return '普通', f'将星价格{price}', 'price'

    # === 第三优先级：珍宝定价 ===
    if get_value >= 200000:
        return '限定', f'珍宝定价{get_value}', 'get_value'
    if 100000 <= get_value <= 199999:
        return '传说', f'珍宝定价{get_value}', 'get_value'
    if 10000 <= get_value <= 99999:
        return '史诗', f'珍宝定价{get_value}', 'get_value'
    if 1001 <= get_value <= 9999:
        return '稀有', f'珍宝定价{get_value}', 'get_value'
    if get_value > 0 and get_value <= 1000:
        return '普通', f'珍宝定价{get_value}', 'get_value'

    # === 第四优先级：待手动确认 ===
    return '待手动确认', f'price={price}, get_value={get_value}', 'unclassified'

# 执行分类
results = []
for g in filtered:
    tier, reason, source = classify_general(g)
    results.append({
        'general_id': g['GeneralID'],
        'name': g['Name'],
        'tier': tier,
        'reason': reason,
        'source': source
    })

# 按档位统计
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print()
print('=== 分类统计 ===')
for tier in ['限定', '传说', '史诗', '稀有', '普通', '待手动确认']:
    if tier in tier_counts:
        print(f'{tier}: {tier_counts[tier]}')

print()
print('=== 待手动确认武将 ===')
manual = [r for r in results if r['tier'] == '待手动确认']
for r in manual:
    print(f"  ID:{r['general_id']} {r['name']}")

# 保存结果
output_path = 'temp_classification_batch2.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print()
print(f'结果已保存到: {output_path}')