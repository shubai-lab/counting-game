# -*- coding: utf-8 -*-
"""
武将评级划分 - 完整名单生成 + Excel 更新 v18
档位：天地玄黄勇

新增：详细获取途径匹配（sgs_general_activity_operate_info）
修复：张宝/夏侯霸固定玄档
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

# ════════════════════════════════════════════════════════════════════════
# 配置
# ════════════════════════════════════════════════════════════════════════
DATA_DIR = r"c:\Users\zhangfan\my-openspec-project\武将评级划分\data"
SGS_CONF_PATH = os.path.join(DATA_DIR, "sgs_general_conf.xlsx")
PRICE_PATH = os.path.join(DATA_DIR, "新三国杀道具定价表.xlsx")
GENERAL_DATA_PATH = os.path.join(DATA_DIR, "武将综合数据表.xlsx")
OPERATE_PATH = os.path.join(DATA_DIR, "sgs_general_activity_operate.xlsx")
OPERATE_INFO_PATH = os.path.join(DATA_DIR, "sgs_general_activity_operate_info.xlsx")
OUTPUT_PATH = os.path.join(DATA_DIR, "武将评级完整名单_v18.xlsx")
SUMMARY_PATH = os.path.join(DATA_DIR, "武将评级分布汇总_v18.xlsx")

# 档位颜色配置
TIER_COLORS = {
    "天": "FFD700",
    "地": "C0C0C0",
    "玄": "CD7F32",
    "黄": "FF8C00",
    "勇": "A9A9A9",
}

TIER_ORDER = ["天", "地", "玄", "黄", "勇"]

def fill(h): return PatternFill("solid", fgColor=h)
def bfont(sz=10, bold=False, color="333333"):
    return Font(name="微软雅黑", bold=bold, size=sz, color=color)
def center(): return Alignment(horizontal="center", vertical="center", wrap_text=True)
def left():   return Alignment(horizontal="left",   vertical="center", wrap_text=True)

def thin_border():
    s = Side(style="thin", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

# ════════════════════════════════════════════════════════════════════════
# 读取数据
# ════════════════════════════════════════════════════════════════════════
print("=== 读取数据 ===")

# 1. 读取 sgs_general_conf
wb_conf = openpyxl.load_workbook(SGS_CONF_PATH)
ws_conf = wb_conf.active

conf_data = []
headers = [cell.value for cell in ws_conf[1]]

for row in ws_conf.iter_rows(min_row=2, values_only=True):
    if row[0] is None:
        continue
    conf_data.append(dict(zip(headers, row)))

print(f"共读取 {len(conf_data)} 条武将配置")

# 2. 读取 sgs_item_goods_activity_conf（将星价格）
ITEM_GOODS_PATH = os.path.join(DATA_DIR, "sgs_item_goods_activity_conf.xlsx")
wb_goods = openpyxl.load_workbook(ITEM_GOODS_PATH)
ws_goods = wb_goods.active

goods_headers = [cell.value for cell in ws_goods[1]]
shop_type_idx = goods_headers.index('ShopType')
price_idx = goods_headers.index('Price')
item_name_idx = goods_headers.index('ItemName')

jiangxing_price_by_name = {}
for row in ws_goods.iter_rows(min_row=4, values_only=True):
    shop_type = row[shop_type_idx]
    if shop_type == '将星':
        name = row[item_name_idx]
        price = row[price_idx]
        if name and price:
            jiangxing_price_by_name[str(name)] = price

JIANGXING_PRICE_OVERRIDE = {
    '张梁': 20,
    '马忠': 20,
    'SP太史慈': 20,
    'SP庞德': 20,
    '诸葛果': 65280,
}

print(f"共读取 {len(jiangxing_price_by_name)} 条将星商品价格")

# 3. 读取定价表
wb_price = openpyxl.load_workbook(PRICE_PATH)
ws_price = wb_price.active

price_data = {}
for row in ws_price.iter_rows(min_row=8, values_only=True):
    if row[0] is None or not isinstance(row[0], (int, str)):
        continue
    item_id = str(row[0])
    price = row[3] if row[3] else 0
    price_data[item_id] = price

print(f"共读取 {len(price_data)} 条定价数据")

# 4. 读取武将综合数据表
wb_general = openpyxl.load_workbook(GENERAL_DATA_PATH)
ws_general = wb_general.active

general_headers = [cell.value for cell in ws_general[1]]

general_data = {}
for row in ws_general.iter_rows(min_row=2, values_only=True):
    if row[1] is None:
        continue
    row_dict = dict(zip(general_headers, row))
    name = row_dict.get('武将名称', '')
    if name:
        general_data[name] = row_dict

print(f"共读取 {len(general_data)} 条武将数据")

# 5. 读取 sgs_general_activity_operate（获取途径ID->名称映射）
wb_operate = openpyxl.load_workbook(OPERATE_PATH)
ws_operate = wb_operate.active

dropway_map = {}  # DropWayID -> DropWayName
for row in ws_operate.iter_rows(min_row=4, values_only=True):
    dropway_id = row[0]
    dropway_name = row[1]
    if dropway_id and dropway_name:
        try:
            dropway_map[int(dropway_id)] = str(dropway_name).strip()
        except:
            pass

print(f"共读取 {len(dropway_map)} 条获取途径映射")

# 6. 读取 sgs_general_activity_operate_info（武将->详细途径）
wb_operate_info = openpyxl.load_workbook(OPERATE_INFO_PATH)
ws_operate_info = wb_operate_info.active

general_detailed_path = {}  # GeneralName -> [详细途径列表]
for row in ws_operate_info.iter_rows(min_row=4, values_only=True):
    general_name = row[1]
    active_dropway = row[2]

    if not general_name or not active_dropway:
        continue

    ways = []
    parts = str(active_dropway).split(' ')
    for part in parts:
        if '获取途径:' in part:
            try:
                way_id = int(part.split(':')[1])
                way_name = dropway_map.get(way_id, f'未知({way_id})')
                ways.append(way_name)
            except:
                pass

    if general_name not in general_detailed_path:
        general_detailed_path[general_name] = []
    general_detailed_path[general_name].extend(ways)

print(f"共读取 {len(general_detailed_path)} 条武将详细途径")

# ════════════════════════════════════════════════════════════════════════
# 建立 GeneralID -> GeneralItemId 的映射
# ════════════════════════════════════════════════════════════════════════

general_id_to_item_id = {}
for c in conf_data:
    general_id = c.get('GeneralID')
    item_id = c.get('GeneralItemId')
    if general_id and item_id:
        general_id_to_item_id[general_id] = item_id

print(f"GeneralID -> GeneralItemId 映射: {len(general_id_to_item_id)} 条")

# ════════════════════════════════════════════════════════════════════════
# 获取途径 -> 档位 映射规则
# ════════════════════════════════════════════════════════════════════════

# 固定档位（按途径）
PATH_TO_TIER_FIXED = {
    # 固定天档
    '武庙': '天',
    '高山仰止': '天',
    # 固定地档
    '祈福': '地',
    # 固定玄档
    '纳贤': '玄',
    '神将任务': '玄',
    '宝玉兑换': '玄',  # 神将兑换，归入玄
    # 充值类 -> 玄档
    '充值奖励': '玄',
    '首充': '玄',
    '累充奖励': '玄',
}

# 依据强度的途径（按价格或原分级）
PATH_TO_TIER_BY_STRENGTH = [
    '战令',
    '活跃活动',
    '活跃任务',
    '周年庆',
    '如意签',
    '砸蛋',
    '连连看',
    '喵喵杀',
    '商城礼包',
    # 商店途径
    '将符商店',
    '公会商店',
    '赛事商店',
    '国士商城',
    # 玩法途径
    '烽火连天',
    '斗地主',
    '武将列传',
    '山河令',
]

# 固定玄档的武将
FIXED_XUAN_GENERALS = [
    '张宝',
    '夏侯霸',
]

# ════════════════════════════════════════════════════════════════════════
# 武将评级逻辑
# ════════════════════════════════════════════════════════════════════════

def get_price_from_price_table(general_id, item_id_map, price_data):
    """从定价表获取价格"""
    item_id = item_id_map.get(general_id, 0)
    if not item_id:
        return 0
    return price_data.get(str(item_id), 0)

def get_effective_price(data, general_id, item_id_map, price_data, jiangxing_price_by_name, get_path):
    """获取有效价格"""
    name = data.get('武将名称', '')

    if name in JIANGXING_PRICE_OVERRIDE:
        return JIANGXING_PRICE_OVERRIDE[name]

    if get_path == '将星招募':
        if name in jiangxing_price_by_name:
            return jiangxing_price_by_name[name]
        return 0

    min_price = data.get('价值_定价', 0) or 0
    if min_price > 0:
        return min_price

    item_id = item_id_map.get(general_id, 0)
    if item_id:
        price = price_data.get(str(item_id), 0)
        if price > 0:
            return price

    return 0

def get_tier(name, series, get_path, price, detailed_paths):
    """根据获取途径和价格确定档位"""

    # 0. 特殊武将固定档位
    if name in ['SP赵云', 'SP马超', 'SP关羽']:
        return "玄"
    if name == '谋黄盖':
        return "地"
    if series in ['无双上将', '无双上将军']:
        return "玄"
    # 张宝/夏侯霸固定玄档
    if name in FIXED_XUAN_GENERALS:
        return "玄"

    # 1. 武庙/高山仰止系列 → 天
    if series in ['武庙', '高山仰止']:
        return "天"

    # 2. 珍宝 → 价格分层
    if get_path == '珍宝':
        if price >= 200000:
            return "天"
        elif price >= 50000:
            return "玄"
        else:
            return "勇"

    # 3. 祈福 → 地
    if get_path == '祈福':
        return "地"

    # 4. 将星招募 → 价格分层
    if get_path == '将星招募':
        if price >= 10000:
            return "地"
        elif price >= 2000:
            return "玄"
        elif price >= 100:
            return "黄"
        else:
            return "勇"

    # 5. 纳贤 → 玄
    if get_path == '纳贤':
        return "玄"

    # 6. 神将任务 → 玄
    if get_path == '神将任务':
        return "玄"

    # 7. 检查详细途径（从sgs_general_activity_operate_info获取）
    name_detailed_paths = detailed_paths.get(name, [])
    for path in name_detailed_paths:
        # 固定档位途径
        if path in PATH_TO_TIER_FIXED:
            return PATH_TO_TIER_FIXED[path]

    # 8. 依据强度的途径 → 根据价格/分级分层
    for path in name_detailed_paths:
        if path in PATH_TO_TIER_BY_STRENGTH:
            # 价格 >= 10000 -> 地
            if price >= 10000:
                return "地"
            # 价格 2000-9999 -> 玄
            elif price >= 2000:
                return "玄"
            # 价格 > 1000 -> 黄
            elif price > 1000:
                return "黄"
            # 价格 <= 1000 -> 勇
            else:
                return "勇"

    # 9. 运营活动/更多方式 → 统一按价格分级
    if get_path in ['运营活动', '更多方式']:
        if price >= 200000:
            return "地"
        elif price >= 100000:
            return "玄"
        elif price > 1000:
            return "黄"
        else:
            return "勇"

    # 默认勇
    return "勇"

def get_tier_rule(tier, path):
    """获取档位评级规则说明"""
    rules = {
        ("天", "武庙"): "武庙系列",
        ("天", "高山仰止"): "高山仰止系列",
        ("天", "珍宝"): "珍宝价格≥20万",
        ("地", "祈福"): "祈福",
        ("地", "将星招募"): "将星价格≥1万",
        ("地", "充值奖励"): "充值奖励",
        ("地", "首充"): "首充",
        ("地", "累充奖励"): "累充奖励",
        ("地", "谋黄盖"): "谋黄盖",
        ("玄", "纳贤"): "纳贤",
        ("玄", "神将任务"): "神将任务",
        ("玄", "宝玉兑换"): "宝玉兑换",
        ("玄", "珍宝"): "珍宝价格10-20万",
        ("玄", "将星招募"): "将星价格2000-9999",
        ("玄", "新手"): "SP赵云/SP马超/SP关羽",
        ("玄", "无双上将军"): "无双上将军系列",
        ("黄", "珍宝"): "珍宝价格5-10万",
        ("黄", "将星招募"): "将星价格100-2000",
        ("黄", "运营活动"): "运营活动价格1001-10万",
        ("黄", "更多方式"): "更多方式价格1001-10万",
        ("勇", "珍宝"): "珍宝价格<5万",
        ("勇", "将星招募"): "将星价格<100",
        ("勇", "运营活动"): "运营活动价格≤1000",
        ("勇", "更多方式"): "更多方式价格≤1000",
    }
    return rules.get((tier, path), "-")

# ════════════════════════════════════════════════════════════════════════
# 生成名单
# ════════════════════════════════════════════════════════════════════════

print("\n=== 开始评级 ===")

all_generals = []
tier_counts = {"天": 0, "地": 0, "玄": 0, "黄": 0, "勇": 0, "排除": 0}

exclude_keywords = ['界限突破', '自走棋', '国战', '体验', '测试']

for name, data in general_data.items():
    series = data.get('系列', '')
    should_exclude = False
    for kw in exclude_keywords:
        if kw in str(name) or kw in str(series):
            should_exclude = True
            break

    if should_exclude:
        tier_counts["排除"] += 1
        continue

    get_path = data.get('获取途径', '')
    general_id = data.get('武将ID', 0)

    price = get_effective_price(data, general_id, general_id_to_item_id, price_data, jiangxing_price_by_name, get_path)

    tier = get_tier(name, series, get_path, price, general_detailed_path)

    all_generals.append({
        '武将名称': name,
        '档位': tier,
        '获取途径': get_path,
        '详细途径': ' / '.join(general_detailed_path.get(name, [])) or '-',
        '价格': price,
        '系列': series,
        '分级': data.get('分级', '')
    })

    tier_counts[tier] += 1

print(f"\n=== 评级结果 ===")
total = len(all_generals)
for tier in TIER_ORDER:
    count = tier_counts[tier]
    pct = count / total * 100 if total > 0 else 0
    print(f"{tier}: {count}个 ({pct:.1f}%)")
print(f"排除: {tier_counts['排除']}个")
print(f"总计: {total}个")

# ════════════════════════════════════════════════════════════════════════
# 生成Excel文件
# ════════════════════════════════════════════════════════════════════════

print("\n=== 生成Excel文件 ===")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "武将评级完整名单"
ws.sheet_view.showGridLines = False

headers = ["武将名称", "档位", "获取途径", "详细途径", "价格", "系列", "原分级"]
set_widths(ws, [18, 8, 12, 20, 12, 18, 10])

ws.merge_cells("A1:G1")
c = ws.cell(1, 1)
c.value = f"武将评级完整名单（共 {len(all_generals)} 个武将）"
c.fill = fill("2D2D44")
c.font = Font(name="微软雅黑", bold=True, size=14, color="FFD700")
c.alignment = center()
ws.row_dimensions[1].height = 36

for i, h in enumerate(headers, 1):
    c = ws.cell(2, i)
    c.value = h
    c.fill = fill("4A4A6A")
    c.font = Font(name="微软雅黑", bold=True, size=11, color="FFFFFF")
    c.alignment = center()
    c.border = thin_border()
ws.row_dimensions[2].height = 28

BG_COLORS = {
    "天": "FFF8DC",
    "地": "F5F5F5",
    "玄": "FFF5E6",
    "黄": "FFF3E0",
    "勇": "FAFAFA",
}

row = 3
for tier in TIER_ORDER:
    tier_gens = [g for g in all_generals if g['档位'] == tier]
    tier_gens.sort(key=lambda x: x['武将名称'])

    for g in tier_gens:
        bg_color = BG_COLORS.get(g['档位'], "FFFFFF")

        vals = [
            g['武将名称'],
            g['档位'],
            g['获取途径'],
            g['详细途径'],
            f"{g['价格']:,}" if g['价格'] > 0 else "-",
            g['系列'],
            g['分级']
        ]

        for col, v in enumerate(vals, 1):
            c = ws.cell(row, col)
            c.value = v
            c.fill = fill(bg_color)
            c.font = bfont(10, bold=(col==2))
            c.alignment = center() if col in [2, 3, 4, 5, 7] else left()
            c.border = thin_border()

        ws.row_dimensions[row].height = 22
        row += 1

wb.save(OUTPUT_PATH)
print(f"已保存: {OUTPUT_PATH}")

# ════════════════════════════════════════════════════════════════════════
# 统计报表
# ════════════════════════════════════════════════════════════════════════

print("\n=== 详细统计 ===")

tier_path_stats = {}
for g in all_generals:
    tier = g['档位']
    path = g['获取途径']
    key = (tier, path)
    if key not in tier_path_stats:
        tier_path_stats[key] = 0
    tier_path_stats[key] += 1

print("\n--- 档位+获取途径分布 ---")
for tier in TIER_ORDER:
    print(f"\n{tier}档:")
    tier_data = [(k[1], v) for k, v in tier_path_stats.items() if k[0] == tier]
    tier_data.sort(key=lambda x: -x[1])
    for path, count in tier_data:
        print(f"  {path}: {count}个")

# 生成汇总表格
wb_summary = openpyxl.Workbook()
ws_sum = wb_summary.active
ws_sum.title = "分布汇总"
ws_sum.sheet_view.showGridLines = False

set_widths(ws_sum, [10, 12, 8, 10, 8, 10, 35])

ws_sum.merge_cells("A1:G1")
c = ws_sum.cell(1, 1)
c.value = "武将评级分布汇总"
c.fill = fill("2D2D44")
c.font = Font(name="微软雅黑", bold=True, size=14, color="FFD700")
c.alignment = center()
ws_sum.row_dimensions[1].height = 36

sum_headers = ["档位", "获取途径", "数量", "档位小计", "总占比", "档位占比", "评级规则"]
for i, h in enumerate(sum_headers, 1):
    c = ws_sum.cell(2, i)
    c.value = h
    c.fill = fill("4A4A6A")
    c.font = Font(name="微软雅黑", bold=True, size=11, color="FFFFFF")
    c.alignment = center()
    c.border = thin_border()
ws_sum.row_dimensions[2].height = 28

row = 3
for tier in TIER_ORDER:
    tier_data = [(k[1], v) for k, v in tier_path_stats.items() if k[0] == tier]
    tier_data.sort(key=lambda x: -x[1])
    tier_total = sum(v for _, v in tier_data)

    for path, count in tier_data:
        bg = TIER_COLORS.get(tier, "FFFFFF")
        tier_rule = get_tier_rule(tier, path)

        vals = [
            tier,
            path,
            count,
            tier_total,
            f"{count/total*100:.1f}%",
            f"{tier_total/total*100:.1f}%",
            tier_rule
        ]

        for col, v in enumerate(vals, 1):
            c = ws_sum.cell(row, col)
            c.value = v
            c.fill = fill(bg) if col == 1 else fill("FFFFFF")
            c.font = bfont(10, bold=(col in [1, 4]))
            c.alignment = center() if col != 7 else left()
            c.border = thin_border()

        ws_sum.row_dimensions[row].height = 22
        row += 1

row += 1
for col, v in enumerate(["合计", "-", total, total, "100%", "100%", ""], 1):
    c = ws_sum.cell(row, col)
    c.value = v
    c.fill = fill("2D2D44")
    c.font = Font(name="微软雅黑", bold=True, size=11, color="FFFFFF")
    c.alignment = center()
    c.border = thin_border()
ws_sum.row_dimensions[row].height = 26

summary_path = SUMMARY_PATH
wb_summary.save(summary_path)
print(f"已保存汇总: {summary_path}")

# ════════════════════════════════════════════════════════════════════════
# 输出各档位武将名单
# ════════════════════════════════════════════════════════════════════════

print("\n=== 各档位武将名单 ===")
for tier in TIER_ORDER:
    tier_gens = [g['武将名称'] for g in all_generals if g['档位'] == tier]
    tier_gens.sort()
    print(f"\n{tier}档 ({len(tier_gens)}个):")
    for i in range(0, len(tier_gens), 10):
        print("  " + ", ".join(tier_gens[i:i+10]))

print("\n=== 完成 ===")
print(f"完整名单: {OUTPUT_PATH}")
print(f"分布汇总: {summary_path}")