# -*- coding: utf-8 -*-
"""
LampType特殊规则分类脚本
筛选LevelTwoGeneralLampType字段包含关键词的武将
"""

import pandas as pd
import json

# 读取Excel文件
excel_path = "c:/Users/zhangfan/my-openspec-project/武将评级划分/data/sgs_general_conf.xlsx"
df = pd.read_excel(excel_path)

# 查看列名
print("列名:", df.columns.tolist())
print("总行数:", len(df))

# 查看LevelTwoGeneralLampType列的内容
if 'LevelTwoGeneralLampType' in df.columns:
    print("\nLevelTwoGeneralLampType 唯一值:")
    print(df['LevelTwoGeneralLampType'].unique())
    print("\n非空值数量:", df['LevelTwoGeneralLampType'].notna().sum())
else:
    print("未找到 LevelTwoGeneralLampType 列")

# LampType分类规则（优先级从高到低）
# 1. 武庙/高山仰止 → 限定
# 2. 威前缀 → 限定
# 3. 无双上将 → 史诗
# 4. 界限突破 → 稀有

def classify_lamptype(lamp_type_str):
    """根据LampType关键词分类"""
    if pd.isna(lamp_type_str):
        return None, None

    lamp_str = str(lamp_type_str)

    # 优先级1: 武庙/高山仰止 → 限定
    if '武庙' in lamp_str or '高山仰止' in lamp_str:
        return '限定', '武庙/高山仰止关键词'

    # 优先级2: 威前缀 → 限定
    if lamp_str.startswith('威') or '威' in lamp_str:
        return '限定', '威前缀关键词'

    # 优先级3: 无双上将 → 史诗
    if '无双上将' in lamp_str:
        return '史诗', '无双上将关键词'

    # 优先级4: 界限突破 → 稀有
    if '界限突破' in lamp_str:
        return '稀有', '界限突破关键词'

    return None, None

# 筛选包含关键词的武将
results = []
for idx, row in df.iterrows():
    lamp_type = row.get('LevelTwoGeneralLampType', None)
    if pd.isna(lamp_type):
        continue

    tier, reason = classify_lamptype(lamp_type)
    if tier:  # 只保留匹配规则的
        results.append({
            'general_id': row.get('general_id', row.get('GeneralId', None)),
            'name': row.get('general_name', row.get('GeneralName', row.get('name', None))),
            'lamp_type': str(lamp_type),
            'tier': tier,
            'reason': reason
        })

# 输出JSON
output_path = "c:/Users/zhangfan/my-openspec-project/武将评级划分/data/lamptype_tier_result.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_path}")
print(f"共筛选出 {len(results)} 个武将")

# 统计各tier数量
tier_counts = {}
for r in results:
    tier = r['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print("\n各品质数量:")
for tier, count in tier_counts.items():
    print(f"  {tier}: {count}")