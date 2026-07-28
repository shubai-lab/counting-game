# -*- coding: utf-8 -*-
"""
对 GeneralID 541-673 范围的武将进行品质分级
"""
import pandas as pd

# 读取pickle文件
df = pd.read_pickle('temp_valid_generals.pkl')

# 筛选541-673 范围
df_filtered = df[(df['GeneralID'] >= 541) & (df['GeneralID'] <= 673)].copy()

# 获取途径映射
DROPWAY_MAP = {
    1: "普通招募",
    2: "将星招募",
    11: "将符商店",
    12: "公会商店",
    13: "赛事商店",
    14: "国士商城",
    21: "会员",
    22: "官阶",
    23: "武将收集",
    24: "官阶",
    25: "官阶",
    26: "官阶",
    27: "官阶",
    28: "官阶礼包",
    101: "烽火连天",
    102: "斗地主",
    103: "武将列传",
    1001: "纳贤",
    1002: "如意签",
    1003: "珍宝",
    1004: "祈福",
    1005: "星河宝箱",
    1101: "宝玉兑换",
    1102: "武庙",
    2000: "首充",
    2001: "砸蛋",
    2002: "充值奖励",
    2003: "累充奖励",
    2004: "连连看",
    3001: "山河令",
    3002: "战令",
    3003: "战令",
    4001: "新人特惠",
    5001: "活跃任务",
    5002: "神将任务",
    5003: "移动奖励",
    5004: "周年庆",
    5005: "喵喵杀",
    5006: "活跃活动",
    5007: "商城礼包",
}

def get_quality(row):
    """根据评级规则确定品质"""
    general_name = row['GeneralName']
    level_two_type = str(row.get('LevelTwoGeneralLampType', ''))
    get_way = row.get('GetWay', 0)
    price = row.get('Price', 0)

    # 1. 武庙或高山仰止 -> 限定
    if '武庙' in level_two_type or '高山仰止' in level_two_type:
        return "限定", "武庙/高山仰止系列"

    # 2. 获取途径 1101 或 1102 -> 限定
    if get_way in [1101, 1102]:
        return "限定", f"获取途径{get_way}"

    # 3. 获取途径 1004 (祈福) -> 传说
    if get_way == 1004:
        return "传说", "祈福"

    # 4. 获取途径 1001 (纳贤) -> 史诗
    if get_way == 1001:
        return "史诗", "纳贤"

    # 5. 获取途径 5002 (神将任务) -> 史诗
    if get_way == 5002:
        return "史诗", "神将任务"

    # 6. 价格 >= 200000 -> 限定
    if price >= 200000:
        return "限定", f"价格≥20万({price})"

    # 7. 价格 >= 100000 -> 传说
    if price >= 100000:
        return "传说", f"价格≥10万({price})"

    # 8. 价格 >= 10000 -> 史诗
    if price >= 10000:
        return "史诗", f"价格≥1万({price})"

    # 9. 价格 >= 1001 -> 稀有
    if price >= 1001:
        return "稀有", f"价格≥1001({price})"

    # 10. 其他 -> 普通
    return "普通", f"其他(价格{price})"

# 应用评级
results = []
for _, row in df_filtered.iterrows():
    general_id = row['GeneralID']
    general_name = row['GeneralName']
    level_two_type = str(row.get('LevelTwoGeneralLampType', ''))
    get_way = row.get('GetWay', 0)
    price = row.get('Price', 0)

    quality, reason = get_quality(row)

    results.append({
        'GeneralID': general_id,
        '名称': general_name,
        '品质': quality,
        '分级依据': reason,
        'LevelTwoType': level_two_type,
        '获取途径ID': get_way,
        '获取途径': DROPWAY_MAP.get(get_way, f'未知({get_way})'),
        '价格': price
    })

results_df = pd.DataFrame(results)

# 输出结果
print("=" * 80)
print("GeneralID 541-673 武将品质分级结果")
print("=" * 80)
print()

# 按品质分类输出
for quality in ["限定", "传说", "史诗", "稀有", "普通"]:
    quality_data = results_df[results_df['品质'] == quality]
    print(f"\n【{quality}】({len(quality_data)}个)")
    print("-" * 60)
    for _, row in quality_data.iterrows():
        print(f"  {row['GeneralID']:4d} | {row['名称']:12s} | {row['分级依据']}")

# 统计
print()
print("=" * 80)
print("统计汇总")
print("=" * 80)
print()

quality_counts = results_df['品质'].value_counts()
total = len(results_df)

for quality in ["限定", "传说", "史诗", "稀有", "普通"]:
    count = quality_counts.get(quality, 0)
    pct = count / total * 100 if total > 0 else 0
    print(f"{quality}: {count}个 ({pct:.1f}%)")

print(f"\n总计: {total}个")

# 保存详细结果到文件
output_path = 'grade_541_673_result.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("GeneralID 541-673 武将品质分级结果\n")
    f.write("=" * 80 + "\n\n")

    for quality in ["限定", "传说", "史诗", "稀有", "普通"]:
        quality_data = results_df[results_df['品质'] == quality]
        f.write(f"\n【{quality}】({len(quality_data)}个)\n")
        f.write("-" * 60 + "\n")
        for _, row in quality_data.iterrows():
            f.write(f"  {row['GeneralID']:4d} | {row['名称']:12s} | {row['分级依据']}\n")

    f.write("\n" + "=" * 80 + "\n")
    f.write("统计汇总\n")
    f.write("=" * 80 + "\n\n")

    for quality in ["限定", "传说", "史诗", "稀有", "普通"]:
        count = quality_counts.get(quality, 0)
        pct = count / total * 100 if total > 0 else 0
        f.write(f"{quality}: {count}个 ({pct:.1f}%)\n")

    f.write(f"\n总计: {total}个\n")

print(f"\n结果已保存到: {output_path}")