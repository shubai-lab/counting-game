# -*- coding: utf-8 -*-
import pandas as pd
import json

file_path = 'C:/Users/zhangfan/Desktop/武将品质划分_ 改版.xlsx'
xl = pd.ExcelFile(file_path)

result = {
    'sheets': xl.sheet_names,
    'content': {}
}

for sheet in xl.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet, header=None)
    result['content'][sheet] = {
        'rows': len(df),
        'cols': len(df.columns),
        'data': df.head(50).values.tolist()
    }

print(json.dumps(result, ensure_ascii=False, indent=2))
