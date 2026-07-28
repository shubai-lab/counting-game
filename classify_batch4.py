# -*- coding: utf-8 -*-
"""
武将分类脚本 - 批次4 (GeneralID 406-540)
分类优先级：
1. 固定档位来源
2. 将星价格
3. 珍宝定价
4. 待手动确认
"""

import pickle
import json

# 读取pkl文件
with open('temp_valid_generals_v2.pkl', 'rb') as f:
    df = pickle.load(f)

print('=== 数据结构 ===')
print('列名:', df.columns.tolist())
print('数据形状:', df.shape)
print()

# 筛选406-540的武将
df_batch4 = df[(df['GeneralID'] >= 406) & (df['GeneralID'] <= 540)].copy()
print(f'筛选后武将数量: {len(df_batch4)}')
print()

# 显示前5行的关键字段
print('=== 前5行数据 ===')
for idx, row in df_batch4.head().iterrows():
    print(f"ID: {row['GeneralID']}, Name: {row['Name']}")
    print(f"  LampType: {row['LampType']}")
    print(f"  Price: {row['Price']}")
    print(f"  Ways: {row['Ways']}")
    print(f"  source_ways: {row['source_ways']}")
    print()

# 定义固定档位来源
LIMITED_SOURCES = ['1101', '1102']  # 高山仰止/武庙珍藏
LEGEND_SOURCES = ['1004']  # 祈福
EPIC_SOURCES = ['1001', '5002', '2000', '2002', '2003', '3001', '1005']  # 纳贤/神将任务/首充/充值奖励/累充奖励/山河令/星河宝箱

def classify_general(row):
    """对武将进行分类"""
    general_id = row['GeneralID']
    name = row['Name']
    lamp_type = str(row['LampType']) if pd.notna(row['LampType']) else ''
    price = row['Price'] if pd.notna(row['Price']) else 0
    source_ways = str(row['source_ways']) if pd.notna(row['source_ways']) else ''
    source_names = str(row['source_names']) if pd.notna(row['source_names']) else ''

    # 第一优先级：固定档位来源
    # 1101高山仰止/1102武庙珍藏 → 限定
    if '1101' in source_ways or '1102' in source_ways or '高山仰止' in lamp_type or '武庙' in lamp_type:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '限定',
            'reason': f"LampType={lamp_type}, source_ways={source_ways}",
            'source': '固定档位(高山仰止/武庙珍藏)'
        }

    # 1004祈福 → 传说
    if '1004' in source_ways or '祈福' in lamp_type:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '传说',
            'reason': f"LampType={lamp_type}, source_ways={source_ways}",
            'source': '固定档位(祈福)'
        }

    # 1001纳贤/5002神将任务/2000首充/2002充值奖励/2003累充奖励/3001山河令/1005星河宝箱 → 史诗
    epic_sources_found = []
    for src in ['1001', '5002', '2000', '2002', '2003', '3001', '1005']:
        if src in source_ways:
            epic_sources_found.append(src)
    if epic_sources_found or '纳贤' in lamp_type or '星河宝箱' in lamp_type or '山河令' in lamp_type:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '史诗',
            'reason': f"LampType={lamp_type}, source_ways={source_ways}",
            'source': f"固定档位(史诗来源: {epic_sources_found})"
        }

    # 第二优先级：将星价格
    if price >= 10000:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '传说',
            'reason': f"将星价格={price}",
            'source': '将星价格'
        }
    elif price >= 2000:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '史诗',
            'reason': f"将星价格={price}",
            'source': '将星价格'
        }
    elif price >= 100:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '稀有',
            'reason': f"将星价格={price}",
            'source': '将星价格'
        }
    elif price > 0:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '普通',
            'reason': f"将星价格={price}",
            'source': '将星价格'
        }

    # 第三优先级：珍宝定价
    # 注意：珍宝定价可能在GetValue字段中，需要检查
    get_value = row['GetValue'] if pd.notna(row['GetValue']) else 0
    if get_value >= 200000:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '限定',
            'reason': f"珍宝定价={get_value}",
            'source': '珍宝定价'
        }
    elif get_value >= 100000:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '传说',
            'reason': f"珍宝定价={get_value}",
            'source': '珍宝定价'
        }
    elif get_value >= 10000:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '史诗',
            'reason': f"珍宝定价={get_value}",
            'source': '珍宝定价'
        }
    elif get_value >= 1001:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '稀有',
            'reason': f"珍宝定价={get_value}",
            'source': '珍宝定价'
        }
    elif get_value > 0:
        return {
            'general_id': int(general_id),
            'name': name,
            'tier': '普通',
            'reason': f"珍宝定价={get_value}",
            'source': '珍宝定价'
        }

    # 第四优先级：待手动确认
    return {
        'general_id': int(general_id),
        'name': name,
        'tier': '待手动确认',
        'reason': f"price={price}, get_value={get_value}, lamp_type={lamp_type}",
        'source': '无匹配来源'
    }

# 对所有武将进行分类
results = []
for idx, row in df_batch4.iterrows():
    result = classify_general(row)
    results.append(result)

# 按general_id排序
results.sort(key=lambda x: x['general_id'])

# 统计各档位数量
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print('=== 分类统计 ===')
for tier, count in sorted(tier_counts.items()):
    print(f"{tier}: {count}")
print()

# 输出JSON结果
output_path = 'temp_classification_batch4.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'分类结果已保存到: {output_path}')
print(f'总计: {len(results)} 个武将')