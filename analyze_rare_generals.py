import pandas as pd
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取Excel文件
file_path = 'C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx'
df = pd.read_excel(file_path, sheet_name='武将名单')

# 显示基本信息
print('='*60)
print('数据基本信息')
print('='*60)
print(f'总行数: {len(df)}')
print(f'列名: {df.columns.tolist()}')
print()

# 显示前5行
print('='*60)
print('前5行数据')
print('='*60)
print(df.head().to_string())
print()

# 查看品质列的唯一值
if '品质' in df.columns:
    print('='*60)
    print('品质列唯一值')
    print('='*60)
    print(df['品质'].unique())
    print()

    # 筛选稀有武将
    rare_df = df[df['品质'] == '稀有']
    print('='*60)
    print(f'稀有武将总数: {len(rare_df)}')
    print('='*60)
    print()

    # 显示所有稀有武将
    print('='*60)
    print('稀有武将完整列表')
    print('='*60)
    print(rare_df.to_string())
    print()

    # 检查相关列
    print('='*60)
    print('检查条件相关列')
    print('='*60)
    print(f'所有列: {df.columns.tolist()}')

    # 查找可能用于判断的列（将星、界限突破等）
    relevant_cols = []
    for col in df.columns:
        col_lower = str(col).lower()
        if '将星' in str(col) or '星' in str(col) or '界限' in str(col) or '突破' in str(col):
            relevant_cols.append(col)

    print(f'可能相关的列: {relevant_cols}')
