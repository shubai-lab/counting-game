# -*- coding: utf-8 -*-
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预\官阶的SQL.xlsx'
wb = openpyxl.load_workbook(path)
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
