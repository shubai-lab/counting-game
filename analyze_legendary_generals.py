# -*- coding: utf-8 -*-
"""
传说武将分析脚本
分析武将品质划分_v21.xlsx中的传说武将
检查每个传说武将是否符合传说条件
"""
import pandas as pd
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 输出文件
output_file = r'c:/Users/zhangfan/my-openspec-project/legendary_general_report.txt'

def main():
    # 读取武将名单Sheet
    print("正在读取Excel文件...")
    df = pd.read_excel(r'C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx', sheet_name='武将名单')

    # 查看数据基本信息
    print("=== 数据列名 ===")
    print(df.columns.tolist())
    print()
    print(f"=== 数据形状 ===")
    print(f"行数: {len(df)}, 列数: {len(df.columns)}")
    print()

    # 找出品质列
    quality_cols = [col for col in df.columns if '品质' in col]
    print(f"品质相关列: {quality_cols}")
    print()

    # 找出名称列
    name_cols = [col for col in df.columns if '名称' in col or '名字' in col or '武将' in col]
    print(f"名称相关列: {name_cols}")
    print()

    # 显示前5行
    print("=== 前10行数据 ===")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    print(df.head(10).to_string())
    print()

    # 假设品质列和名称列
    if quality_cols:
        quality_col = quality_cols[0]
    else:
        # 尝试找到最后一列或特定列
        quality_col = df.columns[-1] if len(df.columns) > 0 else None

    if name_cols:
        name_col = name_cols[0]
    else:
        # 尝试找到第一列或特定列
        name_col = df.columns[0] if len(df.columns) > 0 else None

    print(f"使用的品质列: {quality_col}")
    print(f"使用的名称列: {name_col}")
    print()

    # 找出传说武将
    if quality_col:
        legendary_df = df[df[quality_col] == '传说']
        print(f"=== 传说武将总数: {len(legendary_df)} ===")
        print()

    # 构建报告
    report = []
    report.append("=" * 80)
    report.append("传说武将分析报告")
    report.append("=" * 80)
    report.append("")
    report.append(f"Excel文件: C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx")
    report.append(f"数据表: 武将名单")
    report.append(f"总武将数: {len(df)}")
    report.append(f"传说武将数: {len(legendary_df)}")
    report.append("")
    report.append("=" * 80)
    report.append("传说条件说明")
    report.append("=" * 80)
    report.append("传说武将必须符合以下5个条件中的至少1个:")
    report.append("1. 乐开头(非乐就乐进) - 名字以'乐'开头，但不是'乐就'或'乐进'")
    report.append("2. 将星 >= 4000")
    report.append("3. 纳贤 >= 120")
    report.append("4. 宝玉 >= 12")
    report.append("5. 祈福途径")
    report.append("")
    report.append("=" * 80)
    report.append("数据列名")
    report.append("=" * 80)
    for i, col in enumerate(df.columns):
        report.append(f"{i+1}. {col}")
    report.append("")
    report.append("=" * 80)
    report.append("传说武将列表")
    report.append("=" * 80)

    # 找出各数据列
    jiangxing_col = [col for col in df.columns if '将星' in col]
    naxian_col = [col for col in df.columns if '纳贤' in col]
    baoyu_col = [col for col in df.columns if '宝玉' in col]
    tujing_col = [col for col in df.columns if '途径' in col]

    print(f"将星列: {jiangxing_col}")
    print(f"纳贤列: {naxian_col}")
    print(f"宝玉列: {baoyu_col}")
    print(f"途径列: {tujing_col}")

    # 列表所有传说武将
    for idx, row in legendary_df.iterrows():
        name = row.get(name_col, 'N/A')
        quality = row.get(quality_col, 'N/A')

        # 获取数值列
        jiangxing = row.get(jiangxing_col[0] if jiangxing_col else None, 'N/A')
        naxian = row.get(naxian_col[0] if naxian_col else None, 'N/A')
        baoyu = row.get(baoyu_col[0] if baoyu_col else None, 'N/A')
        tujing = row.get(tujing_col[0] if tujing_col else None, 'N/A')

        report.append(f"\n武将: {name}")
        report.append(f"  品质: {quality}")
        report.append(f"  将星: {jiangxing}")
        report.append(f"  纳贤: {naxian}")
        report.append(f"  宝玉: {baoyu}")
        report.append(f"  途径: {tujing}")

        # 检查是否符合传说条件
        conditions_met = []

        # 条件1: 乐开头(非乐就乐进)
        if isinstance(name, str) and name.startswith('乐') and name not in ['乐就', '乐进']:
            conditions_met.append("乐开头(非乐就乐进)")

        # 条件2: 将星>=4000
        try:
            if float(jiangxing) >= 4000:
                conditions_met.append(f"将星>={jiangxing}")
        except (ValueError, TypeError):
            pass

        # 条件3: 纳贤>=120
        try:
            if float(naxian) >= 120:
                conditions_met.append(f"纳贤>={naxian}")
        except (ValueError, TypeError):
            pass

        # 条件4: 宝玉>=12
        try:
            if float(baoyu) >= 12:
                conditions_met.append(f"宝玉>={baoyu}")
        except (ValueError, TypeError):
            pass

        # 条件5: 祈福途径
        if isinstance(tujing, str) and '祈福' in tujing:
            conditions_met.append("祈福途径")

        if conditions_met:
            report.append(f"  符合条件: {', '.join(conditions_met)}")
        else:
            report.append(f"  【警告】不符合任何传说条件!")

    # 检查不符合条件的传说武将
    report.append("")
    report.append("=" * 80)
    report.append("误判列表 - 不符合传说条件的传说武将")
    report.append("=" * 80)

    misclassified = []
    for idx, row in legendary_df.iterrows():
        name = row.get(name_col, 'N/A')
        jiangxing = row.get(jiangxing_col[0] if jiangxing_col else None, 'N/A')
        naxian = row.get(naxian_col[0] if naxian_col else None, 'N/A')
        baoyu = row.get(baoyu_col[0] if baoyu_col else None, 'N/A')
        tujing = row.get(tujing_col[0] if tujing_col else None, 'N/A')

        # 检查是否符合任何条件
        is_valid = False

        # 条件1
        if isinstance(name, str) and name.startswith('乐') and name not in ['乐就', '乐进']:
            is_valid = True

        # 条件2
        try:
            if float(jiangxing) >= 4000:
                is_valid = True
        except (ValueError, TypeError):
            pass

        # 条件3
        try:
            if float(naxian) >= 120:
                is_valid = True
        except (ValueError, TypeError):
            pass

        # 条件4
        try:
            if float(baoyu) >= 12:
                is_valid = True
        except (ValueError, TypeError):
            pass

        # 条件5
        if isinstance(tujing, str) and '祈福' in tujing:
            is_valid = True

        if not is_valid:
            misclassified.append({
                'name': name,
                'jiangxing': jiangxing,
                'naxian': naxian,
                'baoyu': baoyu,
                'tujing': tujing
            })

    if misclassified:
        report.append(f"\n共有 {len(misclassified)} 个传说武将不符合传说条件:\n")
        for item in misclassified:
            report.append(f"- {item['name']}")
            report.append(f"    将星: {item['jiangxing']}, 纳贤: {item['naxian']}, 宝玉: {item['baoyu']}, 途径: {item['tujing']}")
    else:
        report.append("\n所有传说武将都符合传说条件!")

    # 检查结论
    report.append("")
    report.append("=" * 80)
    report.append("检查结论")
    report.append("=" * 80)

    if misclassified:
        report.append(f"\n【发现问题】共有 {len(misclassified)} 个传说武将的标记可能有误:")
        for item in misclassified:
            report.append(f"  - {item['name']}")
        report.append("\n建议: 核实这些武将的实际数据，确认是否应该标记为传说品质。")
    else:
        report.append("\n【检查通过】所有传说武将的标记都符合传说条件定义。")

    # 写入文件
    report_content = '\n'.join(report)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\n报告已保存到: {output_file}")
    print(report_content)

if __name__ == '__main__':
    main()
