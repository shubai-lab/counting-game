# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('excel_content_utf8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

generals = data['content']['武将名单']['data'][2:]
name_to_quality = {row[1]: row[2] for row in generals if row[0] and row[1] and row[2]}

# 网页原始将池
pools = {
    '祈福SSS': ['司马徽', '兀突骨', '庞德公', '王烈', '沙摩柯', '陆郁生'],
    '限定SSS': ['关索', '赵襄', '鲍三娘', '徐荣', '曹婴', '张琪瑛', '曹纯', '花鬘'],
    '限定(高级)': ['刘宏', '刘永', '张勋', '麴义', '祢衡', '胡金定'],
    '限定(普通)': ['皇甫嵩', '赵昂', '何进', '严夫人', '陆凯', '管辂', '王昶'],
}

# 计算限定武将池（限定SSS + 限定高级 + 限定普通）的品质分布
limited_pool = pools['限定SSS'] + pools['限定(高级)'] + pools['限定(普通)']

print('=== 限定武将池（限定SSS + 限定高级 + 限定普通）===')
print(f'总人数: {len(limited_pool)}')
print()

quality_count = {'限定': 0, '传说': 0, '史诗': 0, '稀有': 0, '普通': 0}
unmatched = []

for name in limited_pool:
    q = name_to_quality.get(name, '未找到')
    if q in quality_count:
        quality_count[q] += 1
    else:
        unmatched.append((name, q))

print('品质分布:')
for q, count in quality_count.items():
    if count > 0:
        print(f'  {q}: {count}人')

if unmatched:
    print(f'\n未匹配: {unmatched}')
