# -*- coding: utf-8 -*-
"""
调试脚本 - 检查武将综合数据表所有字段及数据
"""
import openpyxl
import os

DATA_DIR = r"c:\Users\zhangfan\my-openspec-project\武将评级划分\data"

# 读取武将综合数据表
wb_general = openpyxl.load_workbook(os.path.join(DATA_DIR, "武将综合数据表.xlsx"))
ws_general = wb_general.active

general_headers = [cell.value for cell in ws_general[1]]

print("=== 武将综合数据表所有字段 ===")
for i, h in enumerate(general_headers):
    print(f"  列{i}: {h}")

print("\n=== 前3条完整数据 ===")
count = 0
for row in ws_general.iter_rows(min_row=2, values_only=True):
    if row[1] is None:
        continue
    row_dict = dict(zip(general_headers, row))
    print(f"\n--- {row_dict.get('武将名称')} ---")
    for k, v in row_dict.items():
        if v is not None and v != '':
            print(f"  {k}: {v}")
    count += 1
    if count >= 3:
        break