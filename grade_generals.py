import pandas as pd

# 读取pkl文件
df = pd.read_pickle('temp_valid_generals.pkl')

# 筛选 GeneralID 1-135 范围
df_filtered = df[(df['GeneralID'] >= 1) & (df['GeneralID'] <= 135)].copy()

# 定义分级函数
def grade_general(row):
    lamp_type = str(row['LampType']) if pd.notna(row['LampType']) else ''
    ways = str(row['Ways']) if pd.notna(row['Ways']) else ''
    price = row['Price'] if pd.notna(row['Price']) else 0

    # 优先级1: 武庙或高山仰止
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
        return '限定', 'LevelTwoGeneralLampType包含武庙/高山仰止'

    # 优先级2: 获取途径1101或1102
    if '1101' in ways or '1102' in ways:
        return '限定', '获取途径1101或1102'

    # 优先级3: 祈福1004
    if '1004' in ways:
        return '传说', '获取途径1004(祈福)'

    # 优先级4: 纳贤1001
    if '1001' in ways:
        return '史诗', '获取途径1001(纳贤)'

    # 优先级5: 神将任务5002
    if '5002' in ways:
        return '史诗', '获取途径5002(神将任务)'

    # 优先级6: 价格>=200000
    if price >= 200000:
        return '限定', f'价格{price}>=200000'

    # 优先级7: 价格>=100000
    if price >= 100000:
        return '传说', f'价格{price}>=100000'

    # 优先级8: 价格>=10000
    if price >= 10000:
        return '史诗', f'价格{price}>=10000'

    # 优先级9: 价格>=1001
    if price >= 1001:
        return '稀有', f'价格{price}>=1001'

    # 优先级10: 其他
    return '普通', f'价格{price}<1001'

# 应用分级
results = df_filtered.apply(grade_general, axis=1)
df_filtered['品质'] = results.apply(lambda x: x[0])
df_filtered['分级依据'] = results.apply(lambda x: x[1])

# 输出结果
print('=' * 80)
print(f'武将分级结果 (GeneralID: 1-135，共 {len(df_filtered)} 个武将)')
print('=' * 80)

for _, row in df_filtered.sort_values('GeneralID').iterrows():
    print(f"{row['GeneralID']:3d} | {row['Name'][:10]:10s} | {row['品质']:4s} | {row['分级依据']}")

print('=' * 80)

# 统计各品质数量
print('\n品质分布统计:')
grade_counts = df_filtered['品质'].value_counts()
for grade, count in grade_counts.items():
    print(f'  {grade}: {count}个')
print(f'  总计: {len(df_filtered)}个')