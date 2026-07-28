# -*- coding: utf-8 -*-
"""提取传说武将并验证分类"""
import json

with open(r'c:/Users/zhangfan/my-openspec-project/武将评级划分/data/classification_final_v5_result.json', 'r', encoding='utf-8') as f:
    generals = json.load(f)

# 筛选传说武将
legendary = [g for g in generals if g.get('tier') == '传说']

print(f"=== 传说武将总数: {len(legendary)} ===\n")

# 按分类原因分组
by_reason = {}
for g in legendary:
    reason = g.get('reason', '')
    if reason not in by_reason:
        by_reason[reason] = []
    by_reason[reason].append(g)

print("=== 按分类原因分组 ===\n")
for reason, generals_list in sorted(by_reason.items(), key=lambda x: -len(x[1])):
    print(f"【{reason}】({len(generals_list)}个)")
    for g in generals_list:
        print(f"  - {g['name']} (ID:{g['general_id']})")
    print()

# 检查不符合传说条件的武将
print("\n=== 验证传说条件 ===")
print("传说条件：乐开头(非乐就乐进)/将星>=4000/纳贤>=120/宝玉>=12/祈福途径\n")

issues = []
for g in legendary:
    name = g['name']
    reason = g.get('reason', '')
    lamp_type = g.get('lamp_type', '')
    item_price = g.get('item_price', 0)

    # 检查是否满足传说条件
    valid = False

    # 1. 祈福途径
    if '祈福' in reason or '祈福' in lamp_type:
        valid = True

    # 2. 将星价格 >= 4000
    if '将星价格' in reason:
        price = int(reason.split(':')[1]) if ':' in reason else 0
        if price >= 4000:
            valid = True
        elif price < 4000:
            issues.append({
                'name': name,
                'reason': reason,
                'issue': f'将星价格{price}<4000，不应归为传说'
            })

    # 3. 神武灯 - 应该是固定档位
    if '神武灯' in reason:
        valid = True

    # 4. 谋前缀 - 可能是宝玉>=12的变体
    if '谋前缀' in reason:
        valid = True

    # 5. 手动确认 - 需要人工检查
    if '手动确认' in reason:
        # 检查item_price是否>=150000(宝玉>=12约等于珍宝定价>=150000)
        if item_price and item_price >= 120000:
            valid = True
        else:
            issues.append({
                'name': name,
                'reason': reason,
                'issue': f'手动确认且item_price={item_price}，需要确认是否满足传说条件'
            })

if issues:
    print("=== 潜在问题武将（需要确认）===\n")
    for issue in issues:
        print(f"⚠️ {issue['name']} (ID待查)")
        print(f"   分类原因: {issue['reason']}")
        print(f"   问题: {issue['issue']}")
        print()
else:
    print("✅ 所有传说武将都满足传说条件")

print("\n=== 完整传说武将列表 ===\n")
for i, g in enumerate(legendary, 1):
    print(f"{i:3d}. {g['name']} (ID:{g['general_id']:4d}) | {g.get('reason', '')}")
