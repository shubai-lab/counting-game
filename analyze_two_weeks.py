# -*- coding: utf-8 -*-
import pandas as pd

file_path = r'C:\Users\zhangfan\Downloads\留存分析-2026-07-13~2026-07-26.xlsx'

df = pd.read_excel(file_path)

# 重命名列
df.columns = ['渠道', '日期', '新增', '次留', '3留', '4留', '5留', '6留', '7留', '30留']

# 过滤掉汇总行（日期列包含"汇总"字样的）
df = df[~df['渠道'].astype(str).str.contains('汇总', na=False)]
df = df.dropna(subset=['渠道', '日期'])

# 转换日期 - 使用mixed格式
df['日期'] = pd.to_datetime(df['日期'], format='mixed')

# 筛选两周数据
df_week1 = df[(df['日期'] >= '2026-07-13') & (df['日期'] <= '2026-07-19')]
df_week2 = df[(df['日期'] >= '2026-07-20') & (df['日期'] <= '2026-07-26')]

print(f"W1数据行数: {len(df_week1)}, W2数据行数: {len(df_week2)}")

# 按渠道汇总
agg_cols = {'新增': 'sum', '次留': 'mean', '3留': 'mean', '4留': 'mean', '5留': 'mean', '6留': 'mean', '7留': 'mean'}

week1_sum = df_week1.groupby('渠道').agg(agg_cols).reset_index()
week2_sum = df_week2.groupby('渠道').agg(agg_cols).reset_index()

# 合并
merged = week1_sum.merge(week2_sum, on='渠道', suffixes=('_W1', '_W2'))

# 计算差异
merged['新增变化%'] = ((merged['新增_W2'] - merged['新增_W1']) / merged['新增_W1'] * 100).round(1)
merged['次留变化'] = ((merged['次留_W2'] - merged['次留_W1']) * 100).round(2)
merged['7留变化'] = ((merged['7留_W2'] - merged['7留_W1']) * 100).round(2)

# 筛选两周都有一定数据的渠道
merged = merged[(merged['新增_W1'] > 30) | (merged['新增_W2'] > 30)]

# 按总新增排序
merged['总新增'] = merged['新增_W1'] + merged['新增_W2']
merged = merged.sort_values('总新增', ascending=False)

# 输出结果
print("\n" + "="*120)
print("渠道两周数据对比分析 (7/13-7/19 vs 7/20-7/26)")
print("="*120)

# 表头
header = f"{'渠道':<35} {'W1新增':>8} {'W2新增':>8} {'变化%':>8} {'W1次留':>8} {'W2次留':>8} {'次留差':>8} {'W1_7留':>8} {'W2_7留':>8} {'7留差':>8}"
print(header)
print("-"*120)

for _, row in merged.head(30).iterrows():
    ch = row['渠道'][:35]
    w1_new = row['新增_W1']
    w2_new = row['新增_W2']
    chg = row['新增变化%']
    w1_st = row['次留_W1'] * 100
    w2_st = row['次留_W2'] * 100
    st_diff = row['次留变化']
    w1_d7 = row['7留_W1'] * 100
    w2_d7 = row['7留_W2'] * 100
    d7_diff = row['7留变化']

    print(f"{ch:<35} {w1_new:>8.0f} {w2_new:>8.0f} {chg:>+7.1f}% {w1_st:>6.1f}% {w2_st:>6.1f}% {st_diff:>+6.2f} {w1_d7:>6.1f}% {w2_d7:>6.1f}% {d7_diff:>+6.2f}")

print()
print("="*120)
print("汇总统计")
print("="*120)

total_w1 = merged['新增_W1'].sum()
total_w2 = merged['新增_W2'].sum()
print(f"总新增 W1: {total_w1:.0f}, W2: {total_w2:.0f}, 变化: {(total_w2-total_w1)/total_w1*100:+.1f}%")
print(f"平均次留 W1: {merged['次留_W1'].mean()*100:.2f}%, W2: {merged['次留_W2'].mean()*100:.2f}%, 变化: {(merged['次留_W2'].mean()-merged['次留_W1'].mean())*100:+.2f}%")
print(f"平均7日留存 W1: {merged['7留_W1'].mean()*100:.2f}%, W2: {merged['7留_W2'].mean()*100:.2f}%, 变化: {(merged['7留_W2'].mean()-merged['7留_W1'].mean())*100:+.2f}%")

# 保存到CSV
merged.to_csv(r'c:\Users\zhangfan\my-openspec-project\two_week_comparison.csv', index=False, encoding='utf-8-sig')
print("\n详细数据已保存到 two_week_comparison.csv")
