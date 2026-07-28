# -*- coding: utf-8 -*-
"""
武将品质分类脚本 v3
按途径2（将星招募）价格分类，结合LampType特殊规则
"""

import pandas as pd
import json
import re

# 读取Excel，跳过前4行（表头+类型+配置+说明）
excel_path = "c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_general_conf.xlsx"
df = pd.read_excel(excel_path, header=None, skiprows=4)

print(f"总行数: {len(df)}")

# 手动设置列名（根据之前分析的结构）
# GeneralID=0, GeneralName=2, LevelTwoGeneralLampType=24, GetValue=54
column_names = ['GeneralID', 'NamePrefix', 'GeneralName', 'ShortName', 'GeneralCountry', 'GeneralGender',
                'BaseGeneralID', 'NeedBaseGeneralBreakthrough', 'UnionGeneralID', 'IsEmperor',
                'AssignVIPLevelReq', 'AppointVIPLevelReq', 'AssignRatio', 'CanUseDianJiangKa',
                'CanUseShenJiangKa', 'CanUseSuperDianJiangKa', 'ExpLevelReq', 'VipLevelMark',
                'CanNotShield', 'RobotKindReq', 'GeneralSkillTechType', 'ExType',
                'LevelOneGeneralLampType', 'LevelTwoGeneralLampType', 'InGeneralExtType',
                'Star', 'BaseEvaluate', 'MaxGrade', 'GradeLevelReward', 'SkillDesc',
                'RolePoint', 'GeneralItemId', 'ShopItemId', 'Searchkey', 'InRuleType',
                'InRuleTypeEx', 'InGameModeType', 'LuckCardNames', 'LuckCardType',
                'GeneralPosOffSet', 'IsCanGet', 'RecommendRuleType', 'GetTitle', 'GetDesc',
                'PcGetJump', 'YDGetJump', 'YDGetJumpParam', 'BAddUP', 'SellTimeStartStr',
                'SellTimeStart', 'EnterSeasonTime', 'GeneralSkillFAQ', 'PvName',
                'RecommendTip', 'ModeScore', 'GeneralPersonalDesc', 'GetTips',
                'DifficultyPoints', 'TechTypeTips', 'Designer', 'GetValue']
df.columns = column_names[:len(df.columns)]

print(f"列名: {df.columns.tolist()}")

# LampType分类规则（优先级最高）
def classify_lamptype(lamp_type_str):
    """根据LampType关键词分类"""
    if pd.isna(lamp_type_str):
        return None

    lamp_str = str(lamp_type_str)

    # 武庙/高山仰止 → 限定
    if '武庙' in lamp_str or '高山仰止' in lamp_str:
        return '限定'

    # 威前缀 → 限定
    if lamp_str.startswith('威') or '威' in lamp_str:
        return '限定'

    # 无双上将 → 史诗
    if '无双上将' in lamp_str:
        return '史诗'

    # 界限突破 → 稀有
    if '界限突破' in lamp_str:
        return '稀有'

    return None

def parse_get_value(get_value_str):
    """解析GetValue字段，返回途径和价格字典"""
    if pd.isna(get_value_str):
        return {}

    result = {}
    # 支持中文冒号和英文冒号
    entries = re.split(r'[;；]', str(get_value_str))

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        # 匹配途径
        way_match = re.search(r'获取途径[：:]?\s*(\d+)', entry)
        value_match = re.search(r'获取价值[：:]?\s*(\d+)', entry)

        if way_match and value_match:
            way_id = int(way_match.group(1))
            value = int(value_match.group(1))
            result[way_id] = value

    return result

def classify_general(row):
    """根据获取途径分类武将"""
    lamp_type = row.get('LevelTwoGeneralLampType', None)
    get_value = row.get('GetValue', None)

    # 优先级1: LampType特殊规则
    lamp_tier = classify_lamptype(lamp_type)
    if lamp_tier:
        return lamp_tier, f"LampType:{lamp_type}"

    # 解析GetValue
    ways = parse_get_value(get_value)

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

    # 优先级5: 宝玉兑换(1101) → 按珍宝价格（简化处理）
    if 1101 in ways:
        return '史诗', f"宝玉兑换:{ways[1101]}"

    # 优先级6: 珍宝(1003)
    if 1003 in ways:
        return '史诗', f"珍宝价格:{ways[1003]}"

    # 优先级7: 普通招募(1) → 普通
    if 1 in ways:
        return '普通', f"普通招募价格:{ways[1]}"

    # 无法分类
    return '待手动确认', f"无匹配途径: {get_value}"

# 分类所有武将
results = []
for idx, row in df.iterrows():
    general_id = row.get('GeneralID', row.get('general_id', None))
    name = row.get('GeneralName', row.get('GeneralName', row.get('name', None)))
    lamp_type = row.get('LevelTwoGeneralLampType', None)
    get_value = row.get('GetValue', None)

    # 过滤无效武将（ExType为空）
    ex_type = row.get('ExType', None)
    if pd.isna(ex_type):
        continue

    tier, reason = classify_general(row)

    results.append({
        'general_id': int(general_id) if pd.notna(general_id) else None,
        'name': name,
        'lamp_type': str(lamp_type) if pd.notna(lamp_type) else None,
        'tier': tier,
        'reason': reason,
        'get_value': str(get_value) if pd.notna(get_value) else None
    })

#统计
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print(f"\n分类结果统计:")
print(f"总计: {len(results)} 个武将")
for tier, count in sorted(tier_counts.items()):
    print(f"  {tier}: {count}")

# 保存结果
output_path = "c:/Users/zhangfan/my-openspec-project/武将评级划分/data/classification_v3_fixed.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_path}")

# 输出待手动确认的武将
pending = [r for r in results if r['tier'] == '待手动确认']
print(f"\n待手动确认: {len(pending)} 个")
for r in pending[:10]:
    print(f"  {r['general_id']} {r['name']} - {r['get_value']}")