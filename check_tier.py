# -*- coding: utf-8 -*-
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('武将评级划分/data/classification_final_v5_result.json', 'r', encoding='utf-8') as f:
    generals = json.load(f)

tier_counts = {'普通': 0, '稀有': 0, '史诗': 0, '传说': 0, '限定': 0, '待手动确认': 0}
for g in generals:
    tier = g.get('tier', '普通')
    if tier in tier_counts:
        tier_counts[tier] += 1
    else:
        tier_counts['待手动确认'] += 1

total = len(generals)
print('=== 最新档位分布 (classification_final_v5_result.json) ===')
for tier, count in tier_counts.items():
    pct = count / total * 100 if total > 0 else 0
    print(f'{tier}: {count}个 ({pct:.1f}%)')
print(f'总计: {total}个武将')