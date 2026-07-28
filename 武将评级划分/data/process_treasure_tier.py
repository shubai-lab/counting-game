# -*- coding: utf-8 -*-
import pandas as pd
import json
import os

# 设置路径
data_dir = r"c:\Users\zhangfan\my-openspec-project\武将评级划分\data"
output_path = os.path.join(data_dir, "treasure_tier_result.json")

print("=" * 60)
print("读取Excel文件...")
print("=" * 60)

# 读取Excel文件
general_conf = pd.read_excel(os.path.join(data_dir, "sgs_general_conf.xlsx"))
item_general_conf = pd.read_excel(os.path.join(data_dir, "sgs_item_general_conf.xlsx"))
price_table = pd.read_excel(os.path.join(data_dir, "新三国杀道具定价表.xlsx"))

print("\n=== sgs_general_conf.xlsx (武将配置表) ===")
print("Columns:", general_conf.columns.tolist())
print("Shape:", general_conf.shape)
print(general_conf.head(3).to_string())

print("\n=== sgs_item_general_conf.xlsx (武将道具表) ===")
print("Columns:", item_general_conf.columns.tolist())
print("Shape:", item_general_conf.shape)
print(item_general_conf.head(3).to_string())

print("\n=== 新三国杀道具定价表.xlsx (道具定价表) ===")
print("Columns:", price_table.columns.tolist())
print("Shape:", price_table.shape)
print(price_table.head(10).to_string())

# 查找GetValue列
print("\n" + "=" * 60)
print("分析GetValue和珍宝价格关联...")
print("=" * 60)

# 找到包含GetValue的列
getvalue_cols = [col for col in general_conf.columns if 'GetValue' in str(col)]
print(f"\nGetValue相关列: {getvalue_cols}")

# 找到包含珍宝价格的列
price_cols = [col for col in price_table.columns if any(kw in str(col) for kw in ['珍宝', '价格', 'price', 'Price'])]
print(f"价格相关列: {price_cols}")

# 显示道具表的关键列
item_cols = [col for col in item_general_conf.columns if any(kw in str(col) for kw in ['general', 'item', 'value', 'type', 'id'])]
print(f"道具表关键列: {item_cols}")

# 显示道具表内容
print("\n道具表内容预览:")
print(item_general_conf.head(10).to_string())

# 显示定价表内容
print("\n定价表内容预览:")
print(price_table.head(10).to_string())
