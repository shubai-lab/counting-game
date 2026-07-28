# -*- coding: utf-8 -*-
import pandas as pd

file_path = r'C:\Users\zhangfan\Downloads\留存分析-2026-07-13~2026-07-26.xlsx'
df = pd.read_excel(file_path)
df.columns = ['channel', 'date', 'new', 'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd30']

df = df[~df['channel'].astype(str).str.contains('汇总', na=False)]
df = df.dropna(subset=['channel', 'date'])
df['date'] = pd.to_datetime(df['date'], format='mixed')

df_w1 = df[(df['date'] >= '2026-07-13') & (df['date'] <= '2026-07-19')]
df_w2 = df[(df['date'] >= '2026-07-20') & (df['date'] <= '2026-07-26')]

# 汇总
w1_agg = df_w1.groupby('channel').agg({
    'new': 'sum',
    'd1': lambda x: (df_w1.loc[x.index, 'new'] * x).sum() / df_w1.loc[x.index, 'new'].sum()
}).reset_index()
w1_agg.columns = ['channel', 'new_w1', 'd1_w1']

w2_agg = df_w2.groupby('channel').agg({
    'new': 'sum',
    'd1': lambda x: (df_w2.loc[x.index, 'new'] * x).sum() / df_w2.loc[x.index, 'new'].sum()
}).reset_index()
w2_agg.columns = ['channel', 'new_w2', 'd1_w2']

merged = w1_agg.merge(w2_agg, on='channel', how='outer').fillna(0)

merged['new_change'] = merged['new_w2'] - merged['new_w1']
merged['new_change_pct'] = (merged['new_change'] / merged['new_w1'].replace(0, 1) * 100).round(1)
merged['d1_change'] = ((merged['d1_w2'] - merged['d1_w1']) * 100).round(2)
merged['impact'] = merged['new_w2'] * merged['d1_change']

# 筛选：新增>50 + 人数增长 + 质量下降
filtered = merged[(merged['new_w1'] > 50) & (merged['new_change'] > 0) & (merged['d1_change'] < 0)].copy()
filtered = filtered.sort_values('impact')

print('=' * 100)
print('W2 vs W1 同周期对比：人数增长 + 质量下降的渠道')
print('（仅显示新增>50且同时满足两个条件的渠道）')
print('=' * 100)
print()
print(f"{'渠道':<30} {'W1新增':>8} {'W2新增':>8} {'新增%':>8} {'W1次留':>8} {'W2次留':>8} {'次留变化':>8} {'影响值':>10}")
print('-' * 100)

for _, row in filtered.iterrows():
    ch = row['channel'][:28]
    ch = ch.ljust(30)
    print(f"{ch} {row['new_w1']:8.0f} {row['new_w2']:8.0f} {row['new_change_pct']:+7.1f}% {row['d1_w1']*100:7.1f}% {row['d1_w2']*100:7.1f}% {row['d1_change']:+7.2f}% {row['impact']:10.1f}")

print()
total_impact = filtered['impact'].sum()
total_new_added = filtered['new_change'].sum()
print(f"合计: {len(filtered)} 个渠道")
print(f"总新增增长: {total_new_added:+,.0f}")
print(f"总影响值: {total_impact:,.1f}")
