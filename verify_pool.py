# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('excel_content_utf8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

generals = data['content']['武将名单']['data'][2:]
name_to_quality = {row[1]: row[2] for row in generals if row[0] and row[1] and row[2]}

# 网页原始将池（从snap结果中提取）
pools = {
    '祈福SSS': ['司马徽', '兀突骨', '庞德公', '王烈', '沙摩柯', '陆郁生'],
    '限定SSS': ['关索', '赵襄', '鲍三娘', '徐荣', '曹婴', '张琪瑛', '曹纯', '花鬘'],
    '限定(高级)': ['刘宏', '刘永', '张勋', '麴义', '祢衡', '胡金定'],
    '限定(普通)': ['皇甫嵩', '赵昂', '何进', '严夫人', '陆凯', '管辂', '王昶'],
}

print("=== 核实各将池的实际品质 ===\n")
for pool_name, names in pools.items():
    print(f"【{pool_name}】")
    quality_count = {}
    for name in names:
        q = name_to_quality.get(name, '未找到')
        quality_count[q] = quality_count.get(q, 0) + 1
        print(f"  {name} -> {q}")
    print(f"  品质分布: {quality_count}")
    print()
