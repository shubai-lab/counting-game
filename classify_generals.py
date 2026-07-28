import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取pickle文件
df = pd.read_pickle('temp_valid_generals.pkl')

# 筛选 GeneralID 271-405 范围
df_range = df[(df['GeneralID'] >= 271) & (df['GeneralID'] <= 405)].copy()

def classify_general(row):
    """按优先级对武将进行品质分级"""
    lamp_type = str(row['LampType']) if pd.notna(row['LampType']) else ""
    ways = row['Ways'] if pd.notna(row['Ways']) else {}
    price = row['Price'] if pd.notna(row['Price']) else 0

    # 获取途径数字列表
    way_keys = []
    if isinstance(ways, dict):
        way_keys = list(ways.keys())

    # 优先级1: LevelTwoGeneralLampType 包含 "武庙" 或 "高山仰止"
    if "武庙" in lamp_type or "高山仰止" in lamp_type:
        return "限定", "武庙/高山仰止标签"

    # 优先级2: 获取途径 1101 或 1102
    if 1101 in way_keys or 1102 in way_keys:
        return "限定", "获取途径1101/1102"

    # 优先级3: 获取途径 1004 (祈福)
    if 1004 in way_keys:
        return "传说", "祈福获取"

    # 优先级4: 获取途径 1001 (纳贤)
    if 1001 in way_keys:
        return "史诗", "纳贤获取"

    # 优先级5: 获取途径 5002 (神将任务)
    if 5002 in way_keys:
        return "史诗", "神将任务"

    # 优先级6: 价格 >= 200000
    if price >= 200000:
        return "限定", f"价格{price} >= 200000"

    # 优先级7: 价格 >= 100000
    if price >= 100000:
        return "传说", f"价格{price} >= 100000"

    # 优先级8: 价格 >= 10000
    if price >= 10000:
        return "史诗", f"价格{price} >= 10000"

    # 优先级9: 价格 >= 1001
    if price >= 1001:
        return "稀有", f"价格{price} >= 1001"

    # 优先级10: 其他
    return "普通", f"价格{price} < 1001"

# 应用分类
results = []
for idx, row in df_range.iterrows():
    quality, reason = classify_general(row)
    results.append({
        'GeneralID': int(row['GeneralID']),
        '名称': row['Name'],
        '品质': quality,
        '分级依据': reason
    })

# 转为DataFrame
result_df = pd.DataFrame(results)
result_df = result_df.sort_values('GeneralID')

# 输出每个武将
print("=" * 70)
print("GeneralID | 名称 | 品质 | 分级依据")
print("=" * 70)
for _, row in result_df.iterrows():
    print(f"{row['GeneralID']:8d} | {row['名称']:8s} | {row['品质']:4s} | {row['分级依据']}")

# 统计各品质数量
print("\n" + "=" * 70)
print("各品质数量统计:")
print("=" * 70)
stats = result_df['品质'].value_counts()
for quality, count in stats.items():
    print(f"{quality}: {count}个")
print(f"\n总计: {len(result_df)}个武将")