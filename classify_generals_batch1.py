# -*- coding: utf-8 -*-
"""
武将分类脚本 - 批次1 (GeneralID 1-135)
按四优先级分类：
1. 固定档位来源（1101/1102限定, 1004传说, 其他史诗）
2. 将星价格
3. 珍宝定价
4. 待手动确认
"""

import pickle
import json

# 读取pkl文件
with open('temp_valid_generals_v2.pkl', 'rb') as f:
    df = pickle.load(f)

print(f"总数据量: {len(df)}")

# 筛选 GeneralID 1-135
df_batch1 = df[df['GeneralID'].between(1, 135)].copy()
print(f"批次1数据量: {len(df_batch1)}")

# 固定档位来源映射
LIMITED_SOURCES = ['1101', '1102']  # 高山仰止/武庙珍藏 -> 限定
LEGEND_SOURCES = ['1004']  # 祈福 -> 传说
EPIC_SOURCES = ['1001', '5002', '2000', '2002', '2003', '3001', '1005']  # 史诗

def classify_general(row):
    """按优先级分类武将"""
    general_id = row['GeneralID']
    name = row['Name']
    lamp_type = str(row.get('LampType', ''))
    get_value = row.get('GetValue', 0)
    price = row.get('Price', 0)
    source_ways = str(row.get('source_ways', ''))

    tier = None
    reason = ""
    source = ""

    # ============ 第一优先级：固定档位来源 ============
    # 检查LampType
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
        tier = "限定"
        reason = "LampType包含武庙/高山仰止"
        source = "lamp_type"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

    # 检查source_ways
    for src in LIMITED_SOURCES:
        if src in source_ways:
            tier = "限定"
            reason = f"source_ways包含{src}（高山仰止/武庙珍藏）"
            source = f"source_ways:{src}"
            return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

    for src in LEGEND_SOURCES:
        if src in source_ways:
            tier = "传说"
            reason = f"source_ways包含{src}（祈福）"
            source = f"source_ways:{src}"
            return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

    for src in EPIC_SOURCES:
        if src in source_ways:
            tier = "史诗"
            reason = f"source_ways包含{src}"
            source = f"source_ways:{src}"
            return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

    # ============ 第二优先级：将星价格 ============
    if price >= 10000:
        tier = "传说"
        reason = f"将星价格{price} >= 10000"
        source = f"price:{price}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif 2000 <= price <= 9999:
        tier = "史诗"
        reason = f"将星价格{price} in [2000, 9999]"
        source = f"price:{price}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif 100 <= price <= 1999:
        tier = "稀有"
        reason = f"将星价格{price} in [100, 1999]"
        source = f"price:{price}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif price > 0 and price < 100:
        tier = "普通"
        reason = f"将星价格{price} < 100"
        source = f"price:{price}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

    # ============ 第三优先级：珍宝定价 ============
    if get_value >= 200000:
        tier = "限定"
        reason = f"珍宝价值{get_value} >= 200000"
        source = f"get_value:{get_value}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif 100000 <= get_value <= 199999:
        tier = "传说"
        reason = f"珍宝价值{get_value} in [100000, 199999]"
        source = f"get_value:{get_value}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif 10000 <= get_value <= 99999:
        tier = "史诗"
        reason = f"珍宝价值{get_value} in [10000, 99999]"
        source = f"get_value:{get_value}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif 1001 <= get_value <= 9999:
        tier = "稀有"
        reason = f"珍宝价值{get_value} in [1001, 9999]"
        source = f"get_value:{get_value}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}
    elif get_value > 0 and get_value <= 1000:
        tier = "普通"
        reason = f"珍宝价值{get_value} <= 1000"
        source = f"get_value:{get_value}"
        return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

    # ============ 第四优先级：待手动确认 ============
    tier = "待手动确认"
    reason = f"无法自动分类 (price={price}, get_value={get_value}, source_ways={source_ways})"
    source = "manual"
    return {'general_id': general_id, 'name': name, 'tier': tier, 'reason': reason, 'source': source}

# 执行分类
results = []
for _, row in df_batch1.iterrows():
    result = classify_general(row)
    results.append(result)

# 统计各档位数量
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print("\n分类结果统计:")
for tier, count in sorted(tier_counts.items()):
    print(f"  {tier}: {count}个")

# 保存结果
output_path = 'temp_classification_batch1.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_path}")

# 显示待手动确认的武将
manual_results = [r for r in results if r['tier'] == '待手动确认']
if manual_results:
    print(f"\n待手动确认的武将 ({len(manual_results)}个):")
    for r in manual_results:
        print(f"  ID {r['general_id']}: {r['name']} - {r['reason']}")