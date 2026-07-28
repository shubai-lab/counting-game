import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

df_conf = pd.read_excel('sgs_general_conf.xlsx')

def parse_getvalue(s):
    if pd.isna(s): return {}
    result = {}
    for part in str(s).split(';'):
        m = re.search(r'获取途径:(\d+) 获取价值:(\d+)', part)
        if m: result[int(m.group(1))] = int(m.group(2))
    return result

def get_jx_price(gid):
    m = df_conf[df_conf['GeneralID'] == gid]
    if len(m) > 0:
        p = parse_getvalue(m.iloc[0]['GetValue'])
        for path in [1, 2, 11]:
            if path in p: return p[path]
    return None

df_price = pd.read_excel('新三国杀道具定价表.xlsx', header=5)
df_price.columns = ['item_id', 'item_name', 'item_type', 'price', 'duration', 'expire_date']
df_permanent = df_price[df_price['item_type'] == '永久'].copy()

def find_gen_price(name):
    exact = df_permanent[df_permanent['item_name'] == name]
    if len(exact) > 0:
        ep = exact[exact['price'] > 0]
        return ep['price'].min() if len(ep) > 0 else exact['price'].min()
    matches = df_permanent[df_permanent['item_name'].str.contains(name, na=False)]
    matches = matches[~matches['item_name'].str.contains(r'经典形象|星|月夜|鹊星|傲睨|迅骛|\*|将灵', na=False, regex=True)]
    if len(matches) > 0:
        ep = matches[matches['price'] > 0]
        return ep['price'].min() if len(ep) > 0 else matches['price'].min()
    return None

df = pd.read_excel('武将评级完整名单_v22.xlsx')
df['正确将星价格'] = df['GeneralID'].apply(get_jx_price)
df['真实定价'] = df['武将名称'].apply(find_gen_price)

def get_codes(s):
    if pd.isna(s) or s == '[]': return []
    return re.findall(r'\d+', str(s))

def classify(row):
    codes = set(get_codes(row['获取途径']))
    jx = row['正确将星价格'] if pd.notna(row['正确将星价格']) else 0
    gp = row['真实定价'] if pd.notna(row['真实定价']) else 0

    # 高山仰止: 14 -> 限定
    if '14' in codes: return ('限定', '高山仰止')
    # 珍宝: 1003 或 1101
    if '1003' in codes or '1101' in codes:
        if gp >= 200000: return ('限定', '珍宝>=20万')
        if gp >= 100000: return ('史诗', '珍宝10~20万')
        if gp >= 50000: return ('稀有', '珍宝5~10万')
        return ('限定', '珍宝<5万')
    # 纳贤: 1001 -> 史诗
    if '1001' in codes: return ('史诗', '纳贤')
    # 将星招募: 1, 2, 11 -> PRD正确规则
    if '1' in codes or '2' in codes or '11' in codes:
        if jx >= 10000: return ('传说', '将星>=1万')
        if jx >= 2000: return ('史诗', '将星2000~9999')
        if jx >= 100: return ('稀有', '将星100~2000')
        return ('普通', '将星<100')
    # 祈福: 1004 -> 传说
    if '1004' in codes: return ('传说', '祈福')
    # 神将任务: 5002 -> 史诗
    if '5002' in codes: return ('史诗', '神将任务')
    # 运营活动: 2002, 2001, 2004
    if '2002' in codes or '2001' in codes or '2004' in codes:
        if gp >= 200000: return ('传说', '运营>=20万')
        if gp >= 100000: return ('史诗', '运营10~20万')
        if gp >= 1000: return ('稀有', '运营1001~10万')
        return ('普通', '运营<1000')
    # 武庙: 1102 -> 限定
    if '1102' in codes: return ('限定', '武庙')
    # 目标投放 -> 普通
    if any(c in codes for c in ['12', '103', '3002', '28', '5006', '21']): return ('普通', '目标投放')
    return ('普通', '其他')

results = df.apply(classify, axis=1)
df['品质'] = results.apply(lambda x: x[0])
df['划分依据'] = results.apply(lambda x: x[1])

tier_order = {'限定': 1, '传说': 2, '史诗': 3, '稀有': 4, '普通': 5}
tier_colors = {'限定': 'FFD700', '传说': 'FF69B4', '史诗': '9370DB', '稀有': '4169E1', '普通': '808080'}

df_summary = df.groupby('品质').size().reset_index(name='数量')
df_summary['排序'] = df_summary['品质'].map(tier_order)
df_summary = df_summary.sort_values('排序').drop('排序', axis=1)
df_summary['占比'] = (df_summary['数量'] / 673 * 100).round(1).astype(str) + '%'

df_detail = df.groupby(['品质', '划分依据']).size().reset_index(name='数量')
df_detail['排序1'] = df_detail['品质'].map(tier_order)
df_detail = df_detail.sort_values(['排序1', '划分依据']).drop('排序1', axis=1)

df_list = df.copy()
df_list['排序'] = df_list['品质'].map(tier_order)
df_list = df_list.sort_values(['排序', 'GeneralID']).drop('排序', axis=1)
df_output = df_list[['武将名称', '品质', '划分依据', '正确将星价格', '真实定价']]

wb = Workbook()
header_fill = PatternFill(start_color='3C3C3C', end_color='3C3C3C', fill_type='solid')
header_font = Font(bold=True, color='FFFFFF', size=12)
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

ws1 = wb.active
ws1.title = '品质分布'
for col, h in enumerate(['品质', '数量', '占比'], 1):
    c = ws1.cell(1, col, h)
    c.fill, c.font, c.border, c.alignment = header_fill, header_font, thin_border, Alignment(horizontal='center', vertical='center')
for r, row in enumerate(df_summary.itertuples(index=False), 2):
    for col, v in enumerate(row, 1):
        cell = ws1.cell(r, col, v)
        cell.border, cell.alignment = thin_border, Alignment(horizontal='center', vertical='center')
        if col == 1 and v in tier_colors:
            cell.fill = PatternFill(start_color=tier_colors[v], end_color=tier_colors[v], fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF' if v in ['传说', '史诗'] else '000000')
ws1.column_dimensions['A'].width = 10
ws1.column_dimensions['B'].width = 10
ws1.column_dimensions['C'].width = 10

ws2 = wb.create_sheet('详细分布')
for col, h in enumerate(['品质', '划分依据', '数量'], 1):
    c = ws2.cell(1, col, h)
    c.fill, c.font, c.border, c.alignment = header_fill, header_font, thin_border, Alignment(horizontal='center', vertical='center')
for r, row in enumerate(df_detail.itertuples(index=False), 2):
    for col, v in enumerate(row, 1):
        cell = ws2.cell(r, col, v)
        cell.border, cell.alignment = thin_border, Alignment(horizontal='center', vertical='center')
        if col == 1 and v in tier_colors:
            cell.fill = PatternFill(start_color=tier_colors[v], end_color=tier_colors[v], fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF' if v in ['传说', '史诗'] else '000000')
ws2.column_dimensions['A'].width = 10
ws2.column_dimensions['B'].width = 20
ws2.column_dimensions['C'].width = 10

ws3 = wb.create_sheet('武将名单')
for col, h in enumerate(['武将名称', '品质', '划分依据', '正确将星价格', '真实定价'], 1):
    c = ws3.cell(1, col, h)
    c.fill, c.font, c.border, c.alignment = header_fill, header_font, thin_border, Alignment(horizontal='center', vertical='center')
for r, row in enumerate(df_output.itertuples(index=False), 2):
    for col, v in enumerate(row, 1):
        val = v if pd.notna(v) else '-'
        cell = ws3.cell(r, col, val)
        cell.border, cell.alignment = thin_border, Alignment(horizontal='center', vertical='center')
        if col == 2 and v in tier_colors:
            cell.fill = PatternFill(start_color=tier_colors[v], end_color=tier_colors[v], fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF' if v in ['传说', '史诗'] else '000000')
ws3.column_dimensions['A'].width = 15
ws3.column_dimensions['B'].width = 10
ws3.column_dimensions['C'].width = 20
ws3.column_dimensions['D'].width = 15
ws3.column_dimensions['E'].width = 15

wb.save('武将评级合并_v31.xlsx')
print('已生成: 武将评级合并_v31.xlsx')
print()
print('品质分布:')
print(df_summary.to_string(index=False))
print()
print('详细分布:')
for _, row in df_detail.iterrows():
    print('  %s / %s: %d' % (row['品质'], row['划分依据'], row['数量']))
print()
print('关键武将:')
for name in ['刘备', '关羽', '张飞', '神马超', '武安国']:
    check = df[df['武将名称'] == name]
    if len(check) > 0:
        row = check.iloc[0]
        jx = row['正确将星价格']
        zp = row['真实定价']
        print('  %s: 将星价格=%s, 真实定价=%s, 品质=%s, 划分=%s' % (name, jx, zp, row['品质'], row['划分依据']))