# -*- coding: utf-8 -*-
"""
武将品质分类脚本 v4
使用sgs_general_activity_operate_info.xlsx获取获取途径
"""

import pandas as pd
import json
import re

# 读取主武将表
general_df = pd.read_excel('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_general_conf.xlsx',
                          header=None, skiprows=4)

# 读取运营活动获取途径表，跳过前4行（表头+类型+配置+说明）
operate_df = pd.read_excel('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_general_activity_operate_info.xlsx',
                          header=None, skiprows=4)

# 构建获取途径字典 {general_id: get_value_str}
get_value_dict = {}
for i in range(len(operate_df)):
    general_id = operate_df.iloc[i, 0]
    active_drop_way = operate_df.iloc[i, 2]
    if pd.notna(general_id) and pd.notna(active_drop_way):
        try:
            gid = int(general_id)
            get_value_dict[gid] = str(active_drop_way)
        except (ValueError, TypeError):
            continue

print(f"从运营表获取 {len(get_value_dict)} 个武将的获取途径")
print(f"主表武将数: {len(general_df)}")

# 查看样例
print(f"\n样例 - 关索(500): {get_value_dict.get(500, '无')}")
print(f"样例 - 黄忠(27): {get_value_dict.get(27, '无')}")
print(f"样例 - 刘备(1): {get_value_dict.get(1, '无')}")

def parse_get_value(get_value_str):
    """解析GetValue字段，返回途径和价格字典"""
    if not get_value_str or get_value_str == 'nan':
        return {}

    result = {}
    entries = re.split(r'[;；]', str(get_value_str))

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        # 匹配途径
        way_match = re.search(r'途径[：:]?\s*(\d+)', entry)
        value_match = re.search(r'价值[：:]?\s*(\d+)', entry)

        if way_match and value_match:
            way_id = int(way_match.group(1))
            value = int(value_match.group(1))
            result[way_id] = value

    return result

def classify_lamptype(lamp_type_str):
    """根据LampType关键词分类"""
    if pd.isna(lamp_type_str):
        return None

    lamp_str = str(lamp_type_str)

    if '武庙' in lamp_str or '高山仰止' in lamp_str:
        return '限定'
    if lamp_str.startswith('威') or '威' in lamp_str:
        return '限定'
    if '无双上将' in lamp_str:
        return '史诗'
    if '界限突破' in lamp_str:
        return '稀有'
    return None

def classify_general(general_id, name, lamp_type, get_value):
    """根据获取途径分类武将"""
    # 优先级1: LampType特殊规则
    lamp_tier = classify_lamptype(lamp_type)
    if lamp_tier:
        return lamp_tier, f"LampType:{lamp_type}"

    # 解析GetValue
    ways = parse_get_value(get_value) if get_value else {}

    # 优先级2: 祈福(1004) → 传说
    if 1004 in ways:
        return '传说', f"祈福价格:{ways[1004]}"

    # 优先级3: 纳贤(1001)/神将任务(5002) → 史诗
    if 1001 in ways:
        return '史诗', f"纳贤价格:{ways[1001]}"
    if 5002 in ways:
        return '史诗', f"神将任务价格:{ways[5002]}"

    # 优先级4: 将星招募(2)价格分类
    if 2 in ways:
        price = ways[2]
        if price >= 9999:
            return '传说', f"将星价格:{price}"
        elif price >= 2000:
            return '史诗', f"将星价格:{price}"
        elif price >= 100:
            return '稀有', f"将星价格:{price}"
        else:
            return '普通', f"将星价格:{price}"

    # 优先级5: 宝玉兑换(1101)
    if 1101 in ways:
        return '史诗', f"宝玉兑换:{ways[1101]}"

    # 优先级6: 珍宝(1003)
    if 1003 in ways:
        return '史诗', f"珍宝价格:{ways[1003]}"

    # 优先级7: 普通招募(1) → 普通
    if 1 in ways:
        return '普通', f"普通招募价格:{ways[1]}"

    return '待手动确认', f"无匹配途径"

# 分类所有有效武将
results = []
for i in range(len(general_df)):
    general_id = general_df.iloc[i, 0]
    name = general_df.iloc[i, 2]
    lamp_type = general_df.iloc[i, 24]
    ex_type = general_df.iloc[i, 21]

    # 过滤无效武将
    if pd.isna(ex_type):
        continue

    # 获取获取途径
    get_value = get_value_dict.get(int(general_id), None)

    tier, reason = classify_general(general_id, name, lamp_type, get_value)

    results.append({
        'general_id': int(general_id),
        'name': name,
        'lamp_type': str(lamp_type) if pd.notna(lamp_type) else None,
        'tier': tier,
        'reason': reason,
        'get_value': get_value
    })

# 统计
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print(f"\n===== 分类结果统计 =====")
print(f"总计: {len(results)} 个有效武将")
for tier in ['限定', '传说', '史诗', '稀有', '普通', '待手动确认']:
    count = tier_counts.get(tier, 0)
    print(f"  {tier}: {count}")

# 保存结果
output_path = "c:/Users/zhangfan/my-openspec-project/武将评级划分/data/classification_v4_result.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_path}")

# 输出待手动确认的武将样例
pending = [r for r in results if r['tier'] == '待手动确认']
print(f"\n待手动确认: {len(pending)} 个")
for r in pending[:5]:
    print(f"  {r['general_id']} {r['name']} - get_value={r['get_value']}")