# -*- coding: utf-8 -*-
import pandas as pd
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取武将名单Sheet
try:
    df = pd.read_excel(r'C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx', sheet_name='武将名单')

    # 查看数据基本信息
    print('=== 数据列名 ===')
    print(df.columns.tolist())
    print()
    print('=== 数据形状 ===')
    print(f'行数: {len(df)}, 列数: {len(df.columns)}')
    print()
    print('=== 前5行数据 ===')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df.head(5).to_string())
    print()

    # 查找品质列
    quality_cols = [col for col in df.columns if '品质' in col]
    print(f'品质相关列: {quality_cols}')
    print()

    # 如果有品质列，统计分布
    if quality_cols:
        for col in quality_cols:
            print(f'=== {col} 列的唯一值分布 ===')
            print(df[col].value_counts())
            print()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
