# 武将分类最终合并脚本 v3
# 优先级：LampType特殊分类 > 珍宝价格分类 > 主要分类
# 执行: python merge_final_v3.py

import json

print('=' * 60)
print('武将品质最终合并 v3')
print('=' * 60)

# 读取主要分类（将星价格分类）
with open('classification_v3_result.json', 'r', encoding='utf-8') as f:
    v3_data = json.load(f)
print(f'\n主要分类(将星价格): {len(v3_data)} 个武将')

# 读取珍宝价格分类
with open('classification_final5_result.json', 'r', encoding='utf-8') as f:
    final5_data = json.load(f)
print(f'珍宝价格分类: {len(final5_data)} 个武将')

# 构建珍宝价格字典
price_dict = {}
for g in final5_data:
    price_dict[g['general_id']] = {
        'tier': g['tier'],
        'reason': g['reason'],
        'source': g['source']
    }

# 统计v3各档位
def count_tiers(data):
    counts = {}
    for g in data:
        tier = g.get('tier', '未知')
        counts[tier] = counts.get(tier, 0) + 1
    return counts

print('\n主要分类档位分布:', count_tiers(v3_data))
print('珍宝价格分类档位分布:', count_tiers(final5_data))

# 合并逻辑
# 使用v3作为基础，用珍宝价格分类填充"待手动确认"的武将
merged = {}
filled_count = 0

for g in v3_data:
    gid = g['general_id']
    tier = g['tier']
    reason = g['reason']
    source = g['source']

    # 如果是待手动确认，尝试用珍宝价格填充
    if tier == '待手动确认' and gid in price_dict:
        price_data = price_dict[gid]
        if price_data['tier'] != '待手动确认':
            tier = price_data['tier']
            reason = price_data['reason'] + ' (珍宝价格补充)'
            source = 'price_filled'
            filled_count += 1

    merged[gid] = {
        'general_id': gid,
        'name': g['name'],
        'tier': tier,
        'reason': reason,
        'source': source
    }

print(f'\n珍宝价格补充武将数: {filled_count}')

# 转成列表并排序
merged_list = list(merged.values())
merged_list.sort(key=lambda x: x['general_id'])

# 统计最终结果
final_counts = count_tiers(merged_list)

print('\n' + '=' * 60)
print('最终分类结果')
print('=' * 60)

tier_order = ['限定', '传说', '史诗', '稀有', '普通', '待手动确认']
total = 0
for tier in tier_order:
    if tier in final_counts:
        print(f'{tier}: {final_counts[tier]}')
        total += final_counts[tier]
print(f'总计: {total}')

# 显示待手动确认武将
manual_list = [g for g in merged_list if g['tier'] == '待手动确认']
if manual_list:
    print(f'\n待手动确认武将: {len(manual_list)} 个')
    for g in manual_list[:30]:
        print(f"  ID:{g['general_id']} {g['name']} | {g['reason']}")
    if len(manual_list) > 30:
        print(f'  ... 还有 {len(manual_list) - 30} 个')
else:
    print('\n所有武将已完成分类！')

# 保存结果
output_path = 'classification_final_v3_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(merged_list, f, ensure_ascii=False, indent=2)
print(f'\n结果已保存到: {output_path}')