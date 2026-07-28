# -*- coding: utf-8 -*-
"""检查v21中传说武将的分类是否正确"""
import pandas as pd

# 读取Excel文件
df = pd.read_excel(r'C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx', sheet_name='武将名单')

print("=== 列名 ===")
print(df.columns.tolist())
print()

print("=== 数据预览（前20行）===")
print(df.head(20).to_string())
print()

print("=== 总行数 ===")
print(len(df))
print()

# 查看所有品质类型
if '品质' in df.columns:
    print("=== 品质分布 ===")
    print(df['品质'].value_counts())
