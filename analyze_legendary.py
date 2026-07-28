# -*- coding: utf-8 -*-
import pandas as pd
import re

# 读取Excel文件
df = pd.read_excel(r'C:\Users\zhangfan\Desktop\武将品质划分_v21.xlsx', sheet_name='武将名单')

print("=== 数据结构 ===")
print("列名:", df.columns.tolist())
print(f"总行数: {len(df)}")
print()

# 找出品质列和名称列
quality_col = None
name_col = None
star_col = None
recruit_col = None
jade_col = None
source_col = None

for col in df.columns:
    col_lower = str(col).lower()
    if '品质' in str(col) or '等级' in str(col):
        quality_col = col
    elif '名称' in str(col) or '名字' in str(col) or '武将' in str(col):
        name_col = col
    elif '将星' in str(col):
        star_col = col
    elif '纳贤' in str(col):
        recruit_col = col
    elif '宝玉' in str(col):
        jade_col = col
    elif '途径' in str(col) or '来源' in str(col):
        source_col = col

print(f"品质列: {quality_col}")
print(f"名称列: {name_col}")
print(f"将星列: {star_col}")
print(f"纳贤列: {recruit_col}")
print(f"宝玉列: {jade_col}")
print(f"途径列: {source_col}")
print()

# 打印前几行数据
print("=== 前5行数据 ===")
print(df.head().to_string())
print()

# 筛选传说武将
legendary_df = df[df[quality_col].astype(str).str.contains('传说', na=False)]

print(f"\n=== 传说武将列表 (共 {len(legendary_df)} 人) ===")
for idx, row in legendary_df.iterrows():
    name = row[name_col]
    star = row.get(star_col, None)
    recruit = row.get(recruit_col, None)
    jade = row.get(jade_col, None)
    source = row.get(source_col, None)

    print(f"\n武将: {name}")
    print(f"  将星: {star}")
    print(f"  纳贤: {recruit}")
    print(f"  宝玉: {jade}")
    print(f"  途径: {source}")

    # 检查是否符合传说条件
    conditions = []
    reasons = []

    # 条件1: 乐开头(非乐就乐进)
    if str(name).startswith('乐') and name not in ['乐就', '乐进']:
        conditions.append(True)
        reasons.append("乐开头(非乐就乐进)")

    # 条件2: 将星>=4000
    try:
        if pd.notna(star) and float(star) >= 4000:
            conditions.append(True)
            reasons.append(f"将星={star}>=4000")
    except:
        pass

    # 条件3: 纳贤>=120
    try:
        if pd.notna(recruit) and float(recruit) >= 120:
            conditions.append(True)
            reasons.append(f"纳贤={recruit}>=120")
    except:
        pass

    # 条件4: 宝玉>=12
    try:
        if pd.notna(jade) and float(jade) >= 12:
            conditions.append(True)
            reasons.append(f"宝玉={jade}>=12")
    except:
        pass

    # 条件5: 祈福途径
    if pd.notna(source) and '祈福' in str(source):
        conditions.append(True)
        reasons.append("祈福途径")

    if conditions:
        print(f"  符合条件: {', '.join(reasons)}")
    else:
        print(f"  ❌ 不符合任何传说条件!")

# 误判列表
print("\n" + "="*50)
print("=== 误判为传说的武将列表 ===")
print("="*50)

misclassified = []
for idx, row in legendary_df.iterrows():
    name = row[name_col]
    star = row.get(star_col, None)
    recruit = row.get(recruit_col, None)
    jade = row.get(jade_col, None)
    source = row.get(source_col, None)

    # 检查条件
    is_valid = False

    # 条件1: 乐开头(非乐就乐进)
    if str(name).startswith('乐') and name not in ['乐就', '乐进']:
        is_valid = True

    # 条件2: 将星>=4000
    try:
        if pd.notna(star) and float(star) >= 4000:
            is_valid = True
    except:
        pass

    # 条件3: 纳贤>=120
    try:
        if pd.notna(recruit) and float(recruit) >= 120:
            is_valid = True
    except:
        pass

    # 条件4: 宝玉>=12
    try:
        if pd.notna(jade) and float(jade) >= 12:
            is_valid = True
    except:
        pass

    # 条件5: 祈福途径
    if pd.notna(source) and '祈福' in str(source):
        is_valid = True

    if not is_valid:
        misclassified.append({
            'name': name,
            'star': star,
            'recruit': recruit,
            'jade': jade,
            'source': source
        })

if misclassified:
    print(f"\n共有 {len(misclassified)} 个武将被误判为传说:\n")
    for m in misclassified:
        print(f"武将: {m['name']}")
        print(f"  将星: {m['star']}")
        print(f"  纳贤: {m['recruit']}")
        print(f"  宝玉: {m['jade']}")
        print(f"  途径: {m['source']}")
        print()
else:
    print("\n没有发现误判为传说的武将！")

# 检查结论
print("\n" + "="*50)
print("=== 检查结论 ===")
print("="*50)
print(f"传说武将总数: {len(legendary_df)}")
print(f"误判数量: {len(misclassified)}")
print(f"正确分类数量: {len(legendary_df) - len(misclassified)}")

if len(misclassified) == 0:
    print("\n✅ 所有传说武将的分类都是正确的！")
else:
    print(f"\n⚠️ 发现 {len(misclassified)} 个误判，需要修正！")
