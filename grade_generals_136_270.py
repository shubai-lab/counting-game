import pandas as pd

# 读取 pkl 文件
df = pd.read_pickle('temp_valid_generals.pkl')

# 筛选 GeneralID 136-270 范围
df_range = df[(df['GeneralID'] >= 136) & (df['GeneralID'] <= 270)].copy()

print(f"GeneralID 136-270 范围内的武将数量: {len(df_range)}")
print(f"\n列名: {df.columns.tolist()}")
print()

# 定义评级函数
def get_quality(row):
    # 1. 武庙或高山仰止
    lamp_type = str(row.get('LevelTwoGeneralLampType', ''))
    if '武庙' in lamp_type or '高山仰止' in lamp_type:
        return '限定', '武庙/高山仰止'

    # 2. 获取途径 1101 或 1102
    obtain_way = row.get('ObtainWay', 0)
    if obtain_way in [1101, 1102]:
        return '限定', f'获取途径{obtain_way}'

    # 3. 获取途径 1004 (祈福)
    if obtain_way == 1004:
        return '传说', f'获取途径{obtain_way}'

    # 4. 获取途径 1001 (纳贤)
    if obtain_way == 1001:
        return '史诗', f'获取途径{obtain_way}'

    # 5. 获取途径 5002 (神将任务)
    if obtain_way == 5002:
        return '史诗', f'获取途径{obtain_way}'

    # 6. 价格 >= 200000
    price = row.get('Price', 0)
    if price >= 200000:
        return '限定', f'价格{price}'

    # 7. 价格 >= 100000
    if price >= 100000:
        return '传说', f'价格{price}'

    # 8. 价格 >= 10000
    if price >= 10000:
        return '史诗', f'价格{price}'

    # 9. 价格 >= 1001
    if price >= 1001:
        return '稀有', f'价格{price}'

    # 10. 其他
    return '普通', '默认'

# 应用评级
df_range['品质'] = df_range.apply(lambda row: get_quality(row)[0], axis=1)
df_range['分级依据'] = df_range.apply(lambda row: get_quality(row)[1], axis=1)

# 输出每个武将
print("=" * 80)
print(f"{'GeneralID':<10} {'名称':<20} {'品质':<8} {'分级依据':<30}")
print("=" * 80)

for _, row in df_range.sort_values('GeneralID').iterrows():
    name = row.get('Name', row.get('GeneralName', '未知'))
    general_id = row.get('GeneralID', 0)
    quality = row.get('品质', '未知')
    reason = row.get('分级依据', '未知')
    print(f"{general_id:<10} {name:<20} {quality:<8} {reason:<30}")

# 统计各品质数量
print("\n" + "=" * 80)
print("\n各品质统计:")
quality_counts = df_range['品质'].value_counts()
for quality, count in quality_counts.items():
    print(f"  {quality}: {count} 个")

print(f"\n总计: {len(df_range)} 个武将")