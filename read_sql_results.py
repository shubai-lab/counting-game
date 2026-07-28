import openpyxl, os

folder = r'C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预'
files = [f for f in os.listdir(folder) if f.startswith('SQL')]
files.sort()

for fname in files:
    path = os.path.join(folder, fname)
    print(f'\n=== {fname} ===')
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(values_only=True):
        print(row)