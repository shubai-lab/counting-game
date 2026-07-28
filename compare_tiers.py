import pandas as pd
import os

# 读取武将评级v19
df = pd.read_excel(r'武将评级划分\data\武将评级完整名单_v19.xlsx', engine='openpyxl')

print('=== 武将评级v19 结构 ===')
print('列名:', df.columns.tolist())
print('行数:', len(df))
print()

# 找档位列（应该是第二个）
tier_col = df.columns[1]
price_col = None
for col in df.columns:
    if '价格' in str(col) or '۸' in str(col):
        price_col = col
        break

print(f'档位列: {tier_col}')
print(f'价格列: {price_col}')
print()

print('=== 档位分布 ===')
print(df[tier_col].value_counts())
print()

# 读取四款游戏对照表
print('=== 读取四款杀类游戏对照表 ===')
wb_xlsx = pd.ExcelFile(r'四款杀类游戏武将品质价格对照表.xlsx')
print('工作表:', wb_xlsx.sheet_names)