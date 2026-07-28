# -*- coding: utf-8 -*-
"""检查v21中传说武将的分类是否正确"""
import pandas as pd
import sys

# 读取Excel文件
file_path = r'C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx'
df = pd.read_excel(file_path, sheet_name='武将名单')

print("=== 列名 ===")
print(df.columns.tolist())
print()

print("=== 数据预览（前30行）===")
print(df.head(30).to_string())
print()

print("=== 总行数 ===")
print(len(df))
print()

# 筛选传说武将
if '品质' in df.columns:
    legendary = df[df['品质'] == '传说']
    print(f"=== 传说武将总数: {len(legendary)} ===")
    print()
    print("=== 传说武将列表 ===")
    print(legendary.to_string())
