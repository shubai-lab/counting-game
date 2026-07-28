import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取sgs_general_conf获取正确的将星价格
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
        prices = []
        for path in [1, 2, 11]:
            if path in p: prices.append(p[path])
        if prices: return max(prices)  # 取最高价格
    return None

# 读取goods表获取宝玉数量（同时筛选字符串和数值760770）
df_goods = pd.read_excel('sgs_item_goods_activity_conf.xlsx')
baoyu_goods = df_goods[(df_goods['CurrencyItemID'] == 760770) | (df_goods['CurrencyItemID'] == '760770')].copy()
baoyu_goods['PriceNum'] = pd.to_numeric(baoyu_goods['Price'], errors='coerce')

def get_baoyu_count(item_name):
    match = baoyu_goods[baoyu_goods['ItemName'] == item_name]
    if len(match) > 0:
        return match['PriceNum'].min()
    return None

# 读取武将评级表
df = pd.read_excel('武将评级完整名单_v22.xlsx')

# 获取价格
df['正确将星价格'] = df['GeneralID'].apply(get_jx_price)

def get_zhenbao_baoyu(row):
    path = row['获取途径']
    if pd.isna(path): return None
    codes = set(re.findall(r'\d+', str(path)))
    if '1101' in codes:
        return get_baoyu_count(row['武将名称'])
    return None

df['宝玉数量'] = df.apply(get_zhenbao_baoyu, axis=1)

def get_codes(s):
    if pd.isna(s) or s == '[]': return []
    return re.findall(r'\d+', str(s))

# 特殊手动指定
MANUAL_LEGEND = set()  # 手动传说
MANUAL_EPIC = {'潘淑', '杨婉', '吕玲绮', '南华老仙'}  # 手动史诗
MANUAL_RARE = {'诸葛果', '灵雎'}  # 手动稀有
MANUAL_DELETE = {'威马腾', '威曹彰', '谋诸葛亮'}  # 删除（不输出）
# 运营活动定价: 依据元宝价格/100划分档位
MANUAL_ACTIVITY_PRICING = {'清河公主', '关宁', '芮姬', '孙寒华'}
# 手动升为史诗的谋将（普通档位全部）
MANUAL_MOU_EPIC = {
    '谋王凌', '谋关羽', '谋曹昂', '谋黄盖', '谋淳于琼', '谋杨奉',
    '谋胡烈', '谋卫瓘', '谋骆统', '谋徐盛', '谋董承', '谋法正',
    '谋张任', '谋马谡', '谋王平', '谋诸葛亮', '谋程普'
}

# 读取综合数据表元宝价格
df_yuanbao = pd.read_excel('武将综合数据表.xlsx', dtype=str)

def get_yuanbao_price(name):
    """从综合数据表获取元宝价格"""
    for _, row in df_yuanbao.iterrows():
        if str(row.iloc[1]) == name:  # 武将名在第2列
            val = row.get('价值_定价', None)
            if val and val != 'nan':
                try:
                    return int(float(val))
                except:
                    pass
    return None

def classify(row):
    name = row['武将名称']
    codes = set(get_codes(row['获取途径']))
    jx = row['正确将星价格'] if pd.notna(row['正确将星价格']) else 0
    baoyu = row['宝玉数量'] if pd.notna(row['宝玉数量']) else 0

    # 特殊手动指定
    if name in MANUAL_LEGEND: return ('传说', '手动传说')
    if name in MANUAL_EPIC: return ('史诗', '手动史诗')
    if name in MANUAL_RARE: return ('稀有', '手动指定')

    # 谋将升史诗
    if name in MANUAL_MOU_EPIC: return ('史诗', '谋将升史诗')

    # 运营活动定价: 依据元宝价格/100划分档位
    if name in MANUAL_ACTIVITY_PRICING:
        yuanbao = get_yuanbao_price(name) or 0
        jx_equiv = yuanbao / 100  # 元宝价格转换为将星等价
        if jx_equiv >= 10000: return ('传说', '运营活动')
        if jx_equiv >= 2000: return ('史诗', '运营活动')
        if jx_equiv >= 100: return ('稀有', '运营活动')
        return ('普通', '运营活动')

    # 高山仰止: 14 -> 限定
    if '14' in codes: return ('限定', '高山仰止')

    # 珍宝: 1101 -> 用宝玉数量判断
    if '1101' in codes:
        if baoyu >= 20: return ('限定', '珍宝>=20万')
        if baoyu >= 10: return ('史诗', '珍宝10~20万')
        if baoyu >= 5: return ('稀有', '珍宝5~10万')
        if baoyu > 0: return ('稀有', '珍宝<5万')  # <5万也归稀有
        return ('限定', '珍宝<5万')

    # 纳贤: 1001 -> 史诗
    if '1001' in codes: return ('史诗', '纳贤')

    # 将星招募: 1, 2, 11 -> 用正确将星价格
    if '1' in codes or '2' in codes or '11' in codes:
        if jx >= 10000: return ('传说', '将星>=1万')
        if jx >= 2000: return ('史诗', '将星2000~9999')
        if jx >= 100: return ('稀有', '将星100~2000')
        return ('普通', '将星<100')

    # 祈福: 1004 -> 传说
    if '1004' in codes: return ('传说', '祈福')

    # 神将任务: 5002 -> 史诗
    if '5002' in codes: return ('史诗', '神将任务')

    # 运营活动: 2002, 2001, 2004 -> 用宝玉数量判断
    if '2002' in codes or '2001' in codes or '2004' in codes:
        if baoyu >= 20: return ('传说', '运营>=20万')
        if baoyu >= 10: return ('史诗', '运营10~20万')
        if baoyu >= 1: return ('稀有', '运营<10万')
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
df_output = df_list[['武将名称', '品质', '划分依据', '正确将星价格', '宝玉数量']]

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
for col, h in enumerate(['武将名称', '品质', '划分依据', '正确将星价格', '宝玉数量'], 1):
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
ws3.column_dimensions['E'].width = 12

wb.save('武将评级合并_v32.xlsx')
print('已生成: 武将评级合并_v32.xlsx')
print()
print('品质分布:')
print(df_summary.to_string(index=False))
print()
print('详细分布:')
for _, row in df_detail.iterrows():
    print('  %s / %s: %d' % (row['品质'], row['划分依据'], row['数量']))
print()
print('关键武将:')
for name in ['刘备', '关羽', '张飞', '神马超', '武安国', '神陆逊']:
    check = df[df['武将名称'] == name]
    if len(check) > 0:
        row = check.iloc[0]
        jx = row['正确将星价格']
        baoyu = row['宝玉数量']
        print('  %s: 将星价格=%s, 宝玉=%s, 品质=%s, 划分=%s' % (name, jx, baoyu, row['品质'], row['划分依据']))