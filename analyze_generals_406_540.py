import pandas as pd
import pickle

# 读取pickle文件
with open('temp_valid_generals.pkl', 'rb') as f:
    df = pd.read_pickle(f)

print("=== 数据基本信息 ===")
print(f"总行数: {len(df)}")
print(f"列名: {df.columns.tolist()}")
print()

# 筛选406-540范围
df_filtered = df[(df['GeneralID'] >= 406) & (df['GeneralID'] <= 540)].copy()
print(f"406-540范围武将数: {len(df_filtered)}")
print()

# 显示所有列的数据类型
print("=== 列数据类型 ===")
print(df_filtered.dtypes)
print()

# 显示前20行数据
print("=== 前20行数据 ===")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)
print(df_filtered.head(20).to_string())
print()

# 查看关键列的唯一值
key_cols = ['LevelTwoGeneralLampType', 'AccessMethod', 'Price', 'GetValue', 'GetTitle']
for col in key_cols:
    if col in df_filtered.columns:
        print(f"=== {col} 唯一值 ===")
        unique_vals = df_filtered[col].dropna().unique()
        print(f"唯一值数量: {len(unique_vals)}")
        print(f"值列表: {unique_vals[:20]}")
        print()