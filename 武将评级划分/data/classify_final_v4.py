# -*- coding: utf-8 -*-
"""
武将品质分类脚本 v4.1
按正确的优先级分类：
1. LampType特殊规则（武庙/威前缀/谋前缀/无双上将/界限突破）
2. 获取途径固定规则（祈福→传说，纳贤/神将→史诗）
3. 将星价格
4. 普通招募
5. 武将道具定价（兜底）
"""

import pandas as pd
import json
import re

# 读取主武将表
general_df = pd.read_excel('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_general_conf.xlsx',
                          header=None, skiprows=4)

# 读取运营活动获取途径表（用于纳贤等特殊途径）
operate_df = pd.read_excel('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_general_activity_operate_info.xlsx',
                          header=None, skiprows=4)

# 读取武将道具表和定价表
item_df = pd.read_excel('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_item_general_conf.xlsx',
                        header=None, skiprows=4)
pricing_df = pd.read_excel('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/新三国杀道具定价表.xlsx',
                          header=None, skiprows=2)

# 构建GeneralID → ItemID映射
general_to_item = {}
for i in range(len(item_df)):
    general_id = item_df.iloc[i, 3]  # 列3是GeneralID
    item_id = item_df.iloc[i, 0]      # 列0是ItemID
    if pd.notna(general_id) and pd.notna(item_id):
        try:
            general_to_item[int(general_id)] = int(item_id)
        except:
            pass

# 构建ItemID → Price映射
item_to_price = {}
for i in range(len(pricing_df)):
    item_id = pricing_df.iloc[i, 0]
    price = pricing_df.iloc[i, 3]  # 列3是price
    if pd.notna(item_id) and pd.notna(price):
        try:
            item_to_price[int(item_id)] = float(price)
        except:
            pass

print(f"武将道具映射: {len(general_to_item)} 个")
print(f"道具定价映射: {len(item_to_price)} 个")

# 构建运营表获取途径字典 {general_id: {way_id: price}}
operate_ways = {}
for i in range(len(operate_df)):
    general_id = operate_df.iloc[i, 0]
    active_drop_way = operate_df.iloc[i, 2]
    if pd.notna(general_id) and pd.notna(active_drop_way):
        try:
            gid = int(general_id)
            ways = {}
            entries = re.split(r'[;；]', str(active_drop_way))
            for entry in entries:
                way_match = re.search(r'途径[：:]?\s*(\d+)', entry)
                value_match = re.search(r'价值[：:]?\s*(\d+)', entry)
                if way_match and value_match:
                    ways[int(way_match.group(1))] = int(value_match.group(1))
            operate_ways[gid] = ways
        except (ValueError, TypeError):
            continue

print(f"主表武将数: {len(general_df)}")
print(f"运营表获取途径: {len(operate_ways)} 个")

def is_guozhan(lamp_type_str):
    """检查是否是国战系列武将"""
    if pd.isna(lamp_type_str):
        return False
    lamp_str = str(lamp_type_str)
    # 排除国战相关
    if '国战' in lamp_str:
        return True
    return False

def classify_lamptype(lamp_type_str):
    """根据LampType关键词分类"""
    if pd.isna(lamp_type_str):
        return None, None
    lamp_str = str(lamp_type_str)

    # 优先级1: 武庙/高山仰止 → 限定
    if '武庙' in lamp_str or '高山仰止' in lamp_str:
        return '限定', '武庙/高山仰止'

    # 优先级2: 威前缀 → 限定
    if lamp_str.startswith('威') or '威' in lamp_str:
        return '限定', '威前缀'

    # 优先级3: 神武灯 → 传说
    if '神武' in lamp_str:
        return '传说', '神武灯'

    # 优先级4: 神灯 → 史诗
    if lamp_str == '神':
        return '史诗', '神灯'

    # 优先级4: 谋前缀 → 传说
    if lamp_str.startswith('谋'):
        return '传说', '谋前缀'

    # 优先级5: 无双上将 → 史诗
    if '无双上将' in lamp_str:
        return '史诗', '无双上将'

    # 优先级6: 界限突破 → 稀有
    if '界限突破' in lamp_str:
        return '稀有', '界限突破'

    return None, None

def parse_tag(tag_str):
    """解析武将标签字段，格式如'普通|1'返回途径1"""
    if pd.isna(tag_str):
        return {}
    result = {}
    tag_str = str(tag_str)
    parts = tag_str.split(';')
    for part in parts:
        if '|' in part:
            way_name = part.split('|')[0].strip()
            # 普通招募 → 途径1
            if way_name == '普通':
                result[1] = 0  # 价格未知，设为0
            # 其他途径名...
    return result

def has_tag_way1(tag_str):
    """检查标签是否包含途径1（如'普通|1'）"""
    if pd.isna(tag_str):
        return False
    return '|1' in str(tag_str)

def parse_get_value(get_value_str):
    """解析获取途径字段，如'获取途径:2 获取价值:9999'"""
    if pd.isna(get_value_str):
        return {}
    result = {}
    entries = re.split(r'[;；]', str(get_value_str))
    for entry in entries:
        way_match = re.search(r'途径[：:]?\s*(\d+)', entry)
        value_match = re.search(r'价值[：:]?\s*(\d+)', entry)
        if way_match and value_match:
            result[int(way_match.group(1))] = int(value_match.group(1))
    return result

def merge_ways(main_ways, operate_ways):
    """合并主表和运营表的获取途径，运营表优先级更高"""
    merged = dict(main_ways)
    for way_id, price in operate_ways.items():
        if way_id not in merged:
            merged[way_id] = price
    return merged

def get_item_price(general_id, general_to_item, item_to_price):
    """根据武将ID获取道具定价"""
    item_id = general_to_item.get(int(general_id))
    if item_id and item_id in item_to_price:
        return item_to_price[item_id]
    return None

def classify_general(general_id, lamp_type, get_value_str, tag_str, operate_ways_dict, general_to_item, item_to_price):
    """根据获取途径分类武将"""
    # 优先级1: LampType特殊规则
    lamp_tier, lamp_reason = classify_lamptype(lamp_type)
    if lamp_tier:
        return lamp_tier, f"LampType:{lamp_reason}"

    # 解析主表获取途径（列60）
    main_ways = parse_get_value(get_value_str)

    # 合并运营表获取途径
    operate_ways = operate_ways_dict.get(int(general_id), {})
    ways = merge_ways(main_ways, operate_ways)

    # 优先级2: 获取途径固定规则
    # 祈福(1004) → 传说
    if 1004 in ways:
        return '传说', f"祈福价格:{ways[1004]}"

    # 纳贤(1001) → 史诗（固定）
    if 1001 in ways:
        return '史诗', f"纳贤价格:{ways[1001]}"

    # 神将任务(5002) → 史诗（固定）
    if 5002 in ways:
        return '史诗', f"神将任务价格:{ways[5002]}"

    # 优先级3: 将星招募(2)价格分类
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

    # 优先级4: 宝玉兑换(1101) → ≥1000史诗
    if 1101 in ways:
        price = ways[1101]
        if price >= 200000:
            return '限定', f"宝玉兑换:{price}"
        elif price >= 100000:
            return '传说', f"宝玉兑换:{price}"
        elif price >= 1000:
            return '史诗', f"宝玉兑换:{price}"
        else:
            return '普通', f"宝玉兑换:{price}"

    # 优先级5: 珍宝(1003) → 按价格
    if 1003 in ways:
        price = ways[1003]
        if price >= 200000:
            return '限定', f"珍宝价格:{price}"
        elif price >= 100000:
            return '传说', f"珍宝价格:{price}"
        elif price >= 10000:
            return '史诗', f"珍宝价格:{price}"
        elif price >= 1000:
            return '稀有', f"珍宝价格:{price}"
        else:
            return '普通', f"珍宝价格:{price}"

    # 优先级6: 普通招募(1) → 普通
    if 1 in ways:
        return '普通', f"普通招募价格:{ways[1]}"

    # 优先级7: 检查武将标签(列58)如"普通|1"
    if has_tag_way1(tag_str):
        return '普通', f"普通招募(标签)"

    # 优先级8: 武将道具定价（兜底）
    item_price = get_item_price(general_id, general_to_item, item_to_price)
    if item_price is not None and item_price > 0:
        if item_price >= 200000:
            return '限定', f"道具定价:{int(item_price)}"
        elif item_price >= 100000:
            return '传说', f"道具定价:{int(item_price)}"
        elif item_price >= 10000:
            return '史诗', f"道具定价:{int(item_price)}"
        elif item_price >= 1000:
            return '稀有', f"道具定价:{int(item_price)}"
        else:
            return '普通', f"道具定价:{int(item_price)}"

    return '待手动确认', '无匹配途径'

# 分类所有有效武将（去重）
seen_ids = set()
results = []
for i in range(len(general_df)):
    general_id = general_df.iloc[i, 0]
    name_prefix = general_df.iloc[i, 1]  # 列1是NamePrefix
    name_body = general_df.iloc[i, 2]    # 列2是GeneralName

    # 拼接名字：如果前缀不在主体开头，则拼接
    name = str(name_body) if pd.notna(name_body) else ''
    prefix = str(name_prefix) if pd.notna(name_prefix) else ''
    if prefix and not name.startswith(prefix):
        name = prefix + name

    lamp_type = general_df.iloc[i, 23]  # LevelTwoGeneralLampType
    ex_type = general_df.iloc[i, 21]

    # 过滤无效武将（ExType、LampType非空，且Star>0）
    if pd.isna(ex_type):
        continue
    if pd.isna(lamp_type):
        continue
    star = general_df.iloc[i, 26] if general_df.shape[1] > 26 else None
    if pd.isna(star) or float(star) <= 0:
        continue

    # 过滤国战武将
    if is_guozhan(lamp_type):
        continue

    # 获取获取途径（列60）
    get_value_str = general_df.iloc[i, 60] if general_df.shape[1] > 60 else None

    # 获取武将标签(列58)
    tag_str = general_df.iloc[i, 58] if general_df.shape[1] > 58 else None

    tier, reason = classify_general(general_id, lamp_type, get_value_str, tag_str, operate_ways, general_to_item, item_to_price)

    # 去重：只保留第一个出现的武将
    gid = int(general_id)
    if gid in seen_ids:
        continue
    seen_ids.add(gid)

    # 名字已包含前缀，直接使用
    lamp_str = str(lamp_type) if pd.notna(lamp_type) else ''

    results.append({
        'general_id': gid,
        'name': name,  # 名字已包含前缀
        'lamp_type': lamp_str,
        'tier': tier,
        'reason': reason
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
    pct = count / len(results) * 100
    print(f"  {tier}: {count} ({pct:.1f}%)")

#验证纳贤武将
naxian_in_epic = sum(1 for r in results if '纳贤' in r['reason'] and r['tier'] == '史诗')
print(f"\n纳贤武将验证: {naxian_in_epic}个在史诗档")

# 保存结果
output_path = "c:/Users/zhangfan/my-openspec-project/武将评级划分/data/classification_final_v4_result.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_path}")