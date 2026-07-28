# -*- coding: utf-8 -*-
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取分类结果
with open('武将评级划分/data/classification_final_v5_result.json', 'r', encoding='utf-8') as f:
    generals = json.load(f)

print(f'武将总数: {len(generals)}')

# 按将灯分组统计
lamp_stats = {}
for g in generals:
    lamp = g.get('lamp_type', '未知')
    if lamp not in lamp_stats:
        lamp_stats[lamp] = {'count': 0, 'old_points_sum': 0}
    lamp_stats[lamp]['count'] += 1
    lamp_stats[lamp]['old_points_sum'] += g.get('old_points', 0)

# 显示各将灯的武将数和原帅点总和
for lamp, stats in sorted(lamp_stats.items(), key=lambda x: -x[1]['count']):
    print(f'{lamp}: {stats["count"]}个武将, 原帅点总和={stats["old_points_sum"]}')