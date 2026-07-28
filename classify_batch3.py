import pickle
import json

# 读取pkl文件
with open('temp_valid_generals_v2.pkl', 'rb') as f:
    data = pickle.load(f)

# 筛选 GeneralID 271-405
filtered = data[(data['GeneralID'] >= 271) & (data['GeneralID'] <= 405)]

def classify_general(d):
    """按优先级分类武将"""
    general_id = int(d['GeneralID'])
    name = str(d['Name'])
    lamp_type = str(d.get('LampType', ''))
    price = d.get('Price', 0)
    source_ways = d.get('source_ways', [])

    # GetValue作为珍宝定价
    get_value = d.get('GetValue', 0)

    # 【第一优先级】固定档位来源
    # 1101高山仰止/1102武庙珍藏 → 限定
    if 1101 in source_ways or 1102 in source_ways:
        return '限定', '武庙/高山仰止', source_ways

    # 1004祈福 → 传说
    if 1004 in source_ways:
        return '传说', '祈福', source_ways

    # 1001纳贤/5002神将任务/2000首充/2002充值奖励/2003累充奖励/3001山河令/1005星河宝箱 → 史诗
    epic_ways = [1001, 5002, 2000, 2002, 2003, 3001, 1005]
    for way in source_ways:
        if way in epic_ways:
            return '史诗', f'史诗途径({way})', source_ways

    # 【第二优先级】将星价格
    if price >= 10000:
        return '传说', f'将星价格>=10000({price})', source_ways
    elif price >= 2000:
        return '史诗', f'将星价格2000-9999({price})', source_ways
    elif price >= 100:
        return '稀有', f'将星价格100-1999({price})', source_ways
    elif price > 0:
        return '普通', f'将星价格<100({price})', source_ways

    # 【第三优先级】珍宝定价
    if get_value >= 200000:
        return '限定', f'珍宝>=200000({get_value})', source_ways
    elif get_value >= 100000:
        return '传说', f'珍宝100000-199999({get_value})', source_ways
    elif get_value >= 10000:
        return '史诗', f'珍宝10000-99999({get_value})', source_ways
    elif get_value >= 1001:
        return '稀有', f'珍宝1001-9999({get_value})', source_ways
    elif get_value > 0:
        return '普通', f'珍宝<=1000({get_value})', source_ways

    # 【第四优先级】待手动确认
    return '待确认', f'无分类依据(price={price}, get_value={get_value})', source_ways

# 执行分类
results = []
for idx, d in filtered.iterrows():
    tier, reason, source = classify_general(d)
    results.append({
        'general_id': int(d['GeneralID']),
        'name': str(d['Name']),
        'tier': tier,
        'reason': reason,
        'source': source
    })

# 按general_id排序
results.sort(key=lambda x: x['general_id'])

# 输出统计
tier_counts = {}
for r in results:
    tier_counts[r['tier']] = tier_counts.get(r['tier'], 0) + 1
print("=== 分类统计 ===")
for tier, count in sorted(tier_counts.items()):
    print(f"{tier}: {count}个")

# 保存结果
with open('temp_classification_batch3.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到 temp_classification_batch3.json")
print(f"共分类 {len(results)} 个武将")

# 显示部分结果
print("\n=== 前15个分类结果 ===")
for r in results[:15]:
    print(f"ID:{r['general_id']} {r['name']} -> {r['tier']} | {r['reason']}")

print("\n=== 待确认武将 ===")
for r in results:
    if r['tier'] == '待确认':
        print(f"ID:{r['general_id']} {r['name']} | {r['reason']}")