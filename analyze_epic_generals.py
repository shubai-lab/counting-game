import json

# 读取数据
with open('武将评级划分/data/classification_final_v4_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 筛选史诗武将
epic_generals = [g for g in data if g.get('tier') == '史诗']

print(f'史诗武将总数: {len(epic_generals)}')
print('=' * 60)

# 统计各分类依据
categories = {}
for g in epic_generals:
    reason = g.get('reason', '未知')
    if reason not in categories:
        categories[reason] = []
    categories[reason].append({
        'name': g.get('name'),
        'lamp_type': g.get('lamp_type'),
        'item_price': g.get('item_price'),
        'general_id': g.get('general_id')
    })

# 按数量排序
sorted_categories = sorted(categories.items(), key=lambda x: -len(x[1]))

for reason, generals in sorted_categories:
    print(f'\n【{reason}】共 {len(generals)} 个:')
    for g in generals:
        price_info = f", 珍宝价格:{g['item_price']}" if g['item_price'] else ""
        print(f"  - {g['name']} (ID:{g['general_id']}, 灯:{g['lamp_type']}{price_info})")

# 史诗分类规则
print('\n' + '=' * 60)
print('史诗分类规则检查:')
print('=' * 60)

# 1. 神灯 (LampType:神灯)
shendeng = [g for g in epic_generals if '神灯' in g.get('reason', '')]
print(f'\n1. 神灯分类: {len(shendeng)} 个')
for g in shendeng:
    print(f"   - {g['name']}")

# 2. 无双上将 (LampType:无双上将)
wushuang = [g for g in epic_generals if '无双上将' in g.get('reason', '')]
print(f'\n2. 无双上将分类: {len(wushuang)} 个')
for g in wushuang:
    print(f"   - {g['name']}")

# 3. 纳贤价格
naxian = [g for g in epic_generals if '纳贤' in g.get('reason', '')]
print(f'\n3. 纳贤分类: {len(naxian)} 个')
for g in naxian:
    print(f"   - {g['name']} ({g['reason']})")

# 4. 将星价格
jiangxing = [g for g in epic_generals if '将星价格' in g.get('reason', '')]
print(f'\n4. 将星价格分类: {len(jiangxing)} 个')
for g in jiangxing:
    price = g.get('reason', '').replace('将星价格:', '')
    print(f"   - {g['name']} (价格:{price})")

# 5. 手动确认
manual = [g for g in epic_generals if g.get('reason') == '手动确认']
print(f'\n5. 手动确认分类: {len(manual)} 个')
for g in manual:
    print(f"   - {g['name']} (灯:{g['lamp_type']}, 珍宝:{g.get('item_price')})")

# 检查误判
print('\n' + '=' * 60)
print('误判检查 (不符合史诗条件的武将):')
print('=' * 60)

# 检查手动确认的武将是否真的符合史诗条件
print('\n【手动确认的武将 - 需要人工复核】')
for g in manual:
    name = g['name']
    lamp = g.get('lamp_type', '')
    price = g.get('item_price')

    # 检查是否符合史诗条件
    is_valid = False
    reasons = []

    # 神灯
    if lamp == '神':
        is_valid = True
        reasons.append('神灯')
    # 无双上将
    if lamp == '无双上将':
        is_valid = True
        reasons.append('无双上将')
    # 谋前缀 (需要检查名字)
    if name.startswith('谋') and name != '谋定天下':
        is_valid = True
        reasons.append('谋前缀')
    # 星开头
    if name.startswith('星'):
        is_valid = True
        reasons.append('星开头')
    # 纳贤价格 < 120
    if '纳贤' in str(g.get('reason', '')):
        reasons.append('纳贤')
    # 珍宝价格 10000-99999
    if price and 10000 <= price <= 99999:
        is_valid = True
        reasons.append(f'珍宝价格{price}')

    status = "✓" if is_valid else "⚠️需复核"
    print(f"  {status} {name}: {', '.join(reasons) if reasons else '无明显史诗特征'}")
