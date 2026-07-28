import openpyxl, os

folder = r'C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预'
files = [
    'SQL 1 — 等级分布+次留.xlsx',
    'SQL 2 — 官阶分布+次留.xlsx',
]

for fname in files:
    path = os.path.join(folder, fname)
    print(f'\n=== {fname} ===')
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(values_only=True):
        print(row)