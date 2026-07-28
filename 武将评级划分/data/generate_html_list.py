# -*- coding: utf-8 -*-
import pandas as pd
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DELETE_NAMES = {'威马腾', '威曹彰', '谋诸葛亮'}  # 删除

df = pd.read_excel('武将评级合并_v32.xlsx', sheet_name='武将名单')
df = df[~df['武将名称'].isin(DELETE_NAMES)]
tier_order = {'限定': 1, '传说': 2, '史诗': 3, '稀有': 4, '普通': 5}
df['sort_key'] = df['品质'].map(tier_order)
df = df.sort_values(['sort_key', '武将名称'])
df = df.drop('sort_key', axis=1)

# 生成HTML行
for _, row in df.iterrows():
    name = row['武将名称']
    tier = row['品质']
    reason = row['划分依据']
    jx = row['正确将星价格']
    by = row['宝玉数量']

    jx_str = str(int(float(jx))) if pd.notna(jx) and jx != '-' else '-'
    by_str = str(int(float(by))) if pd.notna(by) and by != '-' else '-'

    tier_class = 'danger' if tier == '限定' else 'warning' if tier == '传说' else 'primary' if tier == '史诗' else 'success' if tier == '稀有' else 'gray'

    print(f'<tr class="tier-row" data-tier="{tier}"><td>{name}</td><td><span class="tag tag-{tier_class}">{tier}</span></td><td>{reason}</td><td>{jx_str}</td><td>{by_str}</td></tr>')
