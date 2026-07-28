# -*- coding: utf-8 -*-
import pandas as pd
import os

# 设置文件路径
file_path = r"C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx"

# 读取Excel文件
print("=" * 60)
print("读取Excel文件...")
print("=" * 60)

try:
    # 读取武将名单 sheet
    df = pd.read_excel(file_path, sheet_name="武将名单")
    print(f"\n成功读取文件，共 {len(df)} 行数据")
    print(f"列名: {list(df.columns)}")
except Exception as e:
    print(f"读取错误: {e}")
    exit()

# 显示前几行数据，了解数据结构
print("\n" + "=" * 60)
print("数据预览（前5行）:")
print("=" * 60)
print(df.head())

# 查找品质列
quality_col = None
for col in df.columns:
    if '品质' in str(col):
        quality_col = col
        break

print(f"\n品质列名: {quality_col}")

# 筛选稀有武将
print("\n" + "=" * 60)
print("筛选【稀有】品质的武将...")
print("=" * 60)

rare_generals = df[df[quality_col] == '稀有']
print(f"\n稀有武将总数: {len(rare_generals)}")

# 显示稀有武将列表
if len(rare_generals) > 0:
    print("\n稀有武将列表:")
    for idx, row in rare_generals.iterrows():
        print(f"  - {row['武将名称'] if '武将名称' in df.columns else row.iloc[0]}")

# 分析将星和界限突破条件
print("\n" + "=" * 60)
print("检查稀有武将是否符合条件...")
print("=" * 60)
print("条件: 将星 100-1499 或 界限突破")

# 查找相关列
name_col = None
star_col = None
突破_col = None

for col in df.columns:
    col_str = str(col)
    if '武将名称' in col_str or '武将名' in col_str:
        name_col = col
    if '将星' in col_str:
        star_col = col
    if '突破' in col_str:
        突破_col = col

print(f"武将名称列: {name_col}")
print(f"将星列: {star_col}")
print(f"界限突破列: {突破_col}")

# 详细检查稀有武将
print("\n" + "=" * 60)
print("稀有武将详细检查:")
print("=" * 60)

misclassified = []  # 误判的武将
correct = []  # 符合条件

for idx, row in rare_generals.iterrows():
    name = row[name_col] if name_col else f"武将{idx}"
    将星 = row[star_col] if star_col else None
    突破 = row[突破_col] if 突破_col else None

    # 检查条件
    star_valid = False
   突破_valid = False

    # 检查将星是否在100-1499范围内
    if pd.notna(将星):
        try:
            star_val = int(将星)
            if 100 <= star_val <= 1499:
                star_valid = True
        except:
            pass

    # 检查是否是界限突破
    if pd.notna(突破):
        if 突破 in ['是', '有', '界限突破', '✓', True]:
            突破_valid = True

    is_valid = star_valid or 突破_valid

    status = "✓ 符合" if is_valid else "✗ 不符合（误判）"

    print(f"\n  {name}:")
    print(f"    将星: {将星} {'✓' if star_valid else '✗'}")
    print(f"    界限突破: {突破} {'✓' if 突破_valid else '✗'}")
    print(f"    判定: {status}")

    if is_valid:
        correct.append(name)
    else:
        misclassified.append({
            'name': name,
            'star': 将星,
            'breakthrough': 突破
        })

# 输出结果
print("\n" + "=" * 60)
print("分析结果汇总")
print("=" * 60)

print(f"\n【稀有武将总数】: {len(rare_generals)}")

print(f"\n【符合稀有条件的武将】: {len(correct)} 人")
for c in correct:
    print(f"  - {c}")

print(f"\n【误判为稀有的武将】: {len(misclassified)} 人")
if misclassified:
    for m in misclassified:
        print(f"  - {m['name']} (将星: {m['star']}, 界限突破: {m['breakthrough']})")
else:
    print("  无误判")

# 检查结论
print("\n" + "=" * 60)
print("【检查结论】")
print("=" * 60)

if len(misclassified) == 0:
    print("✓ 所有标记为【稀有】的武将都符合条件（将星100-1499 或 界限突破）")
    print("✓ 分类标准执行正确，无误判情况")
else:
    print(f"✗ 发现 {len(misclassified)} 个误判为稀有的武将")
    print("✗ 这些武将在标记为【稀有】时不满足将星100-1499或界限突破的条件")
    print("\n建议：")
    print("1. 检查这些武将的实际品质定义")
    print("2. 确认是否需要调整分类规则或重新标记")

print("\n" + "=" * 60)
