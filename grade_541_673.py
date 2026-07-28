# -*- coding: utf-8 -*-
"""
对 GeneralID 541-673 范围的武将进行品质分级
"""
import pandas as pd

# 读取pickle文件
df = pd.read_pickle('temp_valid_generals.pkl')

print("=== 数据结构 ===")
print("列名:", df.columns.tolist())
print("\n总行数:", len(df))
print("\n数据预览 (前5行):")
print(df.head())

# 筛选541-673 范围
df_filtered = df[(df['GeneralID'] >= 541) & (df['GeneralID'] <= 673)]
print(f"\n=== 541-673范围内武将数: {len(df_filtered)} ===")

# 查看关键列
print("\n关键列示例:")
print(df_filtered[['GeneralID', 'GeneralName', 'LevelTwoGeneralLampType', 'GetWay', 'Price']].head(20))

# 保存筛选结果供分析
df_filtered.to_pickle('temp_541_673.pkl')
print("\n已保存筛选结果到 temp_541_673.pkl")