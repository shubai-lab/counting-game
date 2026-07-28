# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('excel_content_utf8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

generals = data['content']['武将名单']['data'][2:]
name_to_quality = {row[1]: row[2] for row in generals if row[0] and row[1] and row[2]}

# 限定武将池武将及其来源分区
limited_generals = [
    # 限定SSS
    ('关索', '限定SSS'),
    ('赵襄', '限定SSS'),
    ('鲍三娘', '限定SSS'),
    ('徐荣', '限定SSS'),
    ('曹婴', '限定SSS'),
    ('张琪瑛', '限定SSS'),
    ('曹纯', '限定SSS'),
    ('花鬘', '限定SSS'),
    # 限定(高级)
    ('刘宏', '限定(高级)'),
    ('刘永', '限定(高级)'),
    ('张勋', '限定(高级)'),
    ('麴义', '限定(高级)'),
    ('祢衡', '限定(高级)'),
    ('胡金定', '限定(高级)'),
    # 限定(普通)
    ('皇甫嵩', '限定(普通)'),
    ('赵昂', '限定(普通)'),
    ('何进', '限定(普通)'),
    ('严夫人', '限定(普通)'),
    ('陆凯', '限定(普通)'),
    ('管辂', '限定(普通)'),
    ('王昶', '限定(普通)'),
]

print("# 限定武将池 - 品质对照表\n")
print("| 武将名称 | 原分区 | 新品质 |")
print("|----------|--------|--------|")

for name, old_pool in limited_generals:
    new_quality = name_to_quality.get(name, '未找到')
    print(f"| {name} | {old_pool} | {new_quality} |")

# 统计
print("\n## 品质统计\n")
print("| 新品质 | 人数 |")
print("|--------|------|")

quality_count = {}
for name, _ in limited_generals:
    q = name_to_quality.get(name, '未知')
    quality_count[q] = quality_count.get(q, 0) + 1

for q in ['限定', '传说', '史诗', '稀有', '普通']:
    if q in quality_count:
        print(f"| {q} | {quality_count[q]} |")
