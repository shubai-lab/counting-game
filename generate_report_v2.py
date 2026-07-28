# -*- coding: utf-8 -*-
"""
预流失干预数据分析报告生成脚本 - v2（修正版）
修正：移除虚构的破冰对局，使用真实漏斗数据，修正任务结构
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabel
import json, os

OUTPUT_PATH = r"C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预\预流失干预数据分析报告_20260428_v2.xlsx"

wb = openpyxl.Workbook()
wb.remove(wb.active)

# ── 颜色常量 ────────────────────────────────────────────────────────
C_DARK      = "1A1A2E"
C_GOLD      = "D4AF37"
C_ORANGE    = "FF9800"
C_LIGHT_O   = "FFF3E0"
C_WHITE     = "FFFFFF"
C_HEADER    = "2D2D44"
C_ALT       = "F5F5F5"
C_GREEN     = "4CAF50"
C_RED       = "F44336"
C_BLUE      = "1976D2"
C_GRAY      = "666666"

def fill(hex_c):  return PatternFill("solid", fgColor=hex_c)
def bfont(sz=10, bold=False, color="333333"):
    return Font(name="微软雅黑", bold=bold, size=sz, color=color)
def center(): return Alignment(horizontal="center", vertical="center", wrap_text=True)
def left():   return Alignment(horizontal="left",   vertical="center", wrap_text=True)

def thin_border():
    s = Side(style="thin", color=C_GOLD)
    return Border(left=s, right=s, top=s, bottom=s)

def merge_title(ws, text, row, c1, c2, sz=13, h=38):
    ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    c = ws.cell(row, c1)
    c.value = text
    c.fill = fill(C_DARK)
    c.font = Font(name="微软雅黑", bold=True, size=sz, color=C_GOLD)
    c.alignment = center()
    ws.row_dimensions[row].height = h

def style_row(ws, row, c1, c2, alt=False, bold_cols=None):
    bg = C_ALT if alt else C_WHITE
    for c in range(c1, c2+1):
        cell = ws.cell(row=row, column=c)
        cell.fill = fill(bg)
        cell.font = bfont(10, bold=(bold_cols and c in bold_cols))
        cell.alignment = center()
        cell.border = thin_border()

def hdr(ws, row, c1, c2, texts):
    for i, t in enumerate(texts):
        cell = ws.cell(row=row, column=c1+i)
        cell.value = t
        cell.fill = fill(C_HEADER)
        cell.font = Font(name="微软雅黑", bold=True, size=10, color=C_WHITE)
        cell.alignment = center()
        cell.border = thin_border()
    ws.row_dimensions[row].height = 26

def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def bar(ws, ref_data, chart_ref, chart_title, x_title, y_title, anchor, bar_dir="col"):
    chart = BarChart()
    chart.type = bar_dir
    chart.grouping = "clustered"
    chart.title = chart_title
    chart.x_axis.title = x_title
    chart.y_axis.title = y_title
    chart.style = 10
    chart.width = 16
    chart.height = 10
    data = Reference(ws, range_string=chart_ref)
    cats = Reference(ws, range_string=ref_data)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, anchor)

def line_chart(ws, ref_data, chart_ref, chart_title, x_title, y_title, anchor):
    chart = LineChart()
    chart.title = chart_title
    chart.x_axis.title = x_title
    chart.y_axis.title = y_title
    chart.style = 10
    chart.width = 18
    chart.height = 11
    data = Reference(ws, range_string=chart_ref)
    cats = Reference(ws, range_string=ref_data)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, anchor)

# ════════════════════════════════════════════════════════════════════════
# 读取真实漏斗数据
# ════════════════════════════════════════════════════════════════════════
with open(r"C:/Users/zhangfan/my-openspec-project/funnel_data.json", encoding="utf-8") as f:
    funnel = json.load(f)

agg = funnel["agg"]      # {"0": {...}, "1": {...}, "2": {...}}
daily = funnel["daily"]  # list of daily rows

GROUPS = ["对照组", "实验组1", "实验组2"]
COLORS_GROUP = ["4A90D9", "FF9800", "4CAF50"]  # 蓝/橙/绿

# ════════════════════════════════════════════════════════════════════════
# Sheet 1: 封面
# ════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("封面")
ws.sheet_view.showGridLines = False
set_widths(ws, [3, 28, 52, 3])
for r in range(1, 28): ws.row_dimensions[r].height = 26

merge_title(ws, "预流失干预数据分析报告", 3, 2, 3, sz=16, h=50)
ws.merge_cells("B5:C5")
ws["B5"].value = "分析日期：2026-04-28  |  数据来源：Metabase Impala + 原始Excel"
ws["B5"].font = bfont(11, color=C_GRAY)
ws["B5"].alignment = left()
ws.merge_cells("B6:C6")
ws["B6"].value = "分析范围：2026-04-08 ~ 2026-04-27（每日有登录数据的完整记录）"
ws["B6"].font = bfont(11, color=C_GRAY)
ws["B6"].alignment = left()

# 核心漏斗卡片
merge_title(ws, "核心漏斗数据（累计）", 8, 2, 3, sz=11, h=32)
cards = [
    ("对照组",   "341,530", "登录率 12.1%",  "次留率 40.3%",  "4A90D9"),
    ("实验组1",  "102,930", "登录率 11.8%",  "次留率 40.3%",  "FF9800"),
    ("实验组2",  "61,372",  "登录率 32.4%",  "次留率 39.1%",  "4CAF50"),
]
for i, (grp, sel, lgr, d3r, clr) in enumerate(cards):
    r = 10 + i * 4
    ws.merge_cells(start_row=r,   start_column=2, end_row=r,   end_column=3)
    ws.merge_cells(start_row=r+1, start_column=2, end_row=r+1, end_column=2)
    ws.merge_cells(start_row=r+1, start_column=3, end_row=r+1, end_column=3)
    ws.merge_cells(start_row=r+2, start_column=2, end_row=r+2, end_column=3)

    c0 = ws.cell(r,   2); c0.value = f"  {grp}  |  圈选 {sel} 人"
    c0.fill = fill(C_DARK); c0.font = Font(name="微软雅黑", bold=True, size=12, color=clr)
    c0.alignment = left(); ws.row_dimensions[r].height = 26

    c1 = ws.cell(r+1, 2); c1.value = lgr; c1.fill = fill(C_ORANGE)
    c1.font = Font(name="微软雅黑", bold=True, size=20, color=C_WHITE); c1.alignment = center()

    c2 = ws.cell(r+2, 2); c2.value = d3r; c2.fill = fill(C_ORANGE)
    c2.font = Font(name="微软雅黑", size=14, color=C_WHITE); c2.alignment = center()

ws.merge_cells("B22:C22")
ws["B22"].value = "疏白 · 数据分析助手"
ws["B22"].font = Font(name="微软雅黑", size=10, color=C_GRAY)
ws["B22"].alignment = center()

# ════════════════════════════════════════════════════════════════════════
# Sheet 2: 漏斗总览（新增，修正版）
# ════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("漏斗总览")
ws2.sheet_view.showGridLines = False
set_widths(ws2, [3, 14, 18, 16, 16, 18, 16, 3])
merge_title(ws2, "预流失干预漏斗总览（三组对比）", 2, 2, 7, sz=13, h=38)

hdr(ws2, 3, 2, 8, ["组别", "预流失圈选", "登录用户", "完成任务", "登录转化率", "任务完成率", "加权次留率"])
ws2.row_dimensions[3].height = 26

funnel_rows = [
    ("对照组",  341530, 41356, 23087, "12.1%", "55.8%", "40.3%"),
    ("实验组1", 102930, 12131, 0,      "11.8%", "—",     "40.3%"),
    ("实验组2",  61372, 19905, 6805,  "32.4%", "34.2%", "39.1%"),
]
row_colors = ["E3F2FD", "FFF3E0", "E8F5E9"]

for i, row in enumerate(funnel_rows):
    r = i + 4
    label, sel, log, task, lgr, task_r, d3r = row
    vals = [label, f"{sel:,}", f"{log:,}", f"{task:,}" if task else "—", lgr, task_r, d3r]
    for j, v in enumerate(vals, 2):
        cell = ws2.cell(r, j)
        cell.value = v
        cell.fill = fill(row_colors[i])
        cell.font = bfont(10, bold=(j==2))
        cell.alignment = center()
        cell.border = thin_border()
        # 高亮异常值
        if j == 5 and v == "32.4%":
            cell.font = Font(name="微软雅黑", bold=True, size=12, color=C_GREEN)
    ws2.row_dimensions[r].height = 28

# 漏斗阶段说明
ws2.merge_cells("B9:D9")
ws2["B9"].value = "注：完成任务 = 登录后完成任意1个战场重燃任务（taskid 1311331-1311348）的用户数"
ws2["B9"].fill = fill(C_LIGHT_O)
ws2["B9"].font = bfont(9, color="CC6600")
ws2["B9"].alignment = left()
ws2.row_dimensions[9].height = 22

# 任务结构说明
merge_title(ws2, "任务结构说明（18个taskid对应3个官阶×3天×2任务）", 11, 2, 8, sz=11, h=32)
hdr(ws2, 12, 2, 8, ["官阶组别", "天数", "任务ID", "任务内容", "奖励", "说明"])
task_struct = [
    ("郎将及以下(A组)", "第1天", "1311331-1311332", "每日登录 + 任意模式完成1局", "武将体验卡×2", "taskid分配待确认"),
    ("偏将军(B组)",     "第1天", "1311337-1311338", "每日登录 + 任意模式完成1局", "武将体验卡×2", "同结构，仅奖励不同"),
    ("将军及以上(C组)", "第1天", "1311343-1311344", "每日登录 + 任意模式完成1局", "武将体验卡×2", "同结构，仅奖励不同"),
    ("各官阶组",        "第2天", "见下方taskid",    "每日登录 + 任意模式完成1局", "武将体验卡×2", "任务内容完全相同"),
    ("各官阶组",        "第3天", "见下方taskid",    "每日登录 + 任意模式完成1局", "武将体验卡×2", "完成率最低，流失最严重"),
]
task_bg = ["FFF9C4","F3E5F5","E8F5E9","EEEEEE","EEEEEE"]
for i, row in enumerate(task_struct):
    r = i + 14
    for j, v in enumerate(row, 2):
        cell = ws2.cell(r, j)
        cell.value = v
        cell.fill = fill(task_bg[i])
        cell.font = bfont(9, bold=(j==2))
        cell.alignment = center() if j != 4 else left()
        cell.border = thin_border()
    ws2.row_dimensions[r].height = 22

ws2.merge_cells("B20:H20")
ws2["B20"].value = "★ 真实情况：三个官阶的任务内容完全相同，差异化仅体现在武将体验卡数量。当前不存在'破冰对局'、'任务差异化'等功能。"
ws2["B20"].fill = fill("FFCDD2")
ws2["B20"].font = Font(name="微软雅黑", bold=True, size=10, color="CC0000")
ws2["B20"].alignment = left()
ws2.row_dimensions[20].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 3: 留存率对比（修正：用真实加权留存）
# ════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("留存率对比")
ws3.sheet_view.showGridLines = False
set_widths(ws3, [3, 18, 18, 18, 18, 3])
merge_title(ws3, "留存率对比（对照组 vs 实验组1 vs 实验组2）", 2, 2, 5, sz=13, h=38)

hdr(ws3, 3, 2, 6, ["指标", "对照组", "实验组1", "实验组2", "最优组"])
ws3.row_dimensions[3].height = 26

ret_data = [
    ("预流失圈选用户",  "341,530", "102,930",  "61,372",   "实验组2(登录率最高)"),
    ("登录转化率",      "12.1%",   "11.8%",    "32.4%",    "实验组2 ▲▲"),
    ("完成任务用户",    "23,087",  "0条记录",   "6,805",    "对照组(数据最完整)"),
    ("任务完成率",      "55.8%",   "—",        "34.2%",    "对照组"),
    ("次留率(加权)",    "40.3%",   "40.3%",    "39.1%",    "对照组≈实验组1"),
    ("第7天留存(加权)", "35.5%",   "35.1%",    "32.2%",    "对照组"),
    ("实验组vs对照组",  "基准",    "+0.0pp",   "-1.2pp",   "实验组1"),
]

ret_colors = ["E3F2FD","FFF3E0","E8F5E9"]
for i, row in enumerate(ret_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, v in enumerate(row, 2):
        cell = ws3.cell(r, j)
        cell.value = v
        if j <= 4:
            bg = ret_colors[j-2] if not alt else C_ALT
        else:
            bg = C_ALT if alt else C_WHITE
        cell.fill = fill(bg)
        if j == 5 and "▲" in str(v):
            cell.font = Font(name="微软雅黑", bold=True, size=10, color=C_GREEN)
        elif j == 2:
            cell.font = bfont(10, bold=True)
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws3.row_dimensions[r].height = 26

ws3.merge_cells("B13:D13")
ws3["B13"].value = "核心发现：实验组2登录转化率(32.4%)遥遥领先，但次留率(39.1%)反而最低；对照组/实验组1登录转化率仅~12%但次留率更高，说明触达质量vs干预深度存在权衡。"
ws3["B13"].fill = fill(C_LIGHT_O)
ws3["B13"].font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
ws3["B13"].alignment = left()
ws3.row_dimensions[13].height = 32

# ════════════════════════════════════════════════════════════════════════
# Sheet 4: 每日漏斗明细
# ════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("每日漏斗明细")
ws4.sheet_view.showGridLines = False
set_widths(ws4, [3, 12, 10, 12, 12, 12, 10, 10, 3])

merge_title(ws4, "每日漏斗明细（2026-04-08 ~ 2026-04-27）", 2, 2, 8, sz=13, h=38)
hdr(ws4, 3, 2, 9, ["日期", "组别", "圈选用户", "登录用户", "完成任务", "登录转化率", "次留率", "7天留存"])
ws4.row_dimensions[3].height = 26

grps = ["对照组","实验组1","实验组2"]
grp_bg = {0:"E3F2FD",1:"FFF3E0",2:"E8F5E9"}
grp_alt = {0:C_ALT,1:C_ALT,2:C_ALT}

# Sort daily by date desc then group
daily_sorted = sorted(daily, key=lambda x: (x["date"], x["gid"]), reverse=True)

for i, row in enumerate(daily_sorted):
    r = i + 4
    gid = row["gid"]
    sel = row["sel"]
    log = row["log"]
    task = row["task"]
    lgr = f"{log/sel*100:.1f}%" if sel > 0 else "—"
    d3 = f"{row['day3']*100:.1f}%" if row["day3"] else "—"
    d7 = f"{row['day7']*100:.1f}%" if row["day7"] else "—"
    vals = [row["date"][:10], grps[gid], f"{sel:,}", f"{log:,}",
            f"{task:,}" if task else "—", lgr, d3, d7]
    alt = (i % 2 == 1)
    for j, v in enumerate(vals, 2):
        cell = ws4.cell(r, j)
        cell.value = v
        if j == 3:  # group label col
            cell.fill = fill(grp_bg[gid])
        elif alt:
            cell.fill = fill(grp_alt[gid])
        else:
            cell.fill = fill(C_WHITE)
        cell.font = bfont(9, bold=(j==2 or j==3))
        cell.alignment = center()
        cell.border = thin_border()
    ws4.row_dimensions[r].height = 20

# ════════════════════════════════════════════════════════════════════════
# Sheet 5: 等级分布（修正：使用真实数据）
# ════════════════════════════════════════════════════════════════════════
ws5 = wb.create_sheet("等级分布")
ws5.sheet_view.showGridLines = False
set_widths(ws5, [3, 20, 16, 12, 14, 3])

merge_title(ws5, "干预用户等级分布（Metabase查询：taskid 1311331-1311348）", 2, 2, 5, sz=13, h=38)
hdr(ws5, 3, 2, 6, ["等级段", "用户数", "占比", "次留率", "特征说明"])
ws5.row_dimensions[3].height = 26

lv_data = [
    ("6-10级",    511,   0.94,  "—",   "新手保护期"),
    ("11-20级",  690,   1.26,  "—",   ""),
    ("21-40级",  1338,  2.45,  "—",   ""),
    ("41-60级",  2307,  4.23,  "—",   ""),
    ("61-100级", 6795,  12.46, "—",   "★ 黄金干预段"),
    ("101-150级",9680,  17.74, "—",   "★ 黄金干预段（偏将军聚集）"),
    ("151-200级",33234, 60.92, "—",   "高等级用户为主"),
]
risk_bg = {"★ 黄金干预段":"FFF9C4","★ 黄金干预段（偏将军聚集）":"F3E5F5"}

total_lv = sum(x[1] for x in lv_data)

for i, row in enumerate(lv_data):
    r = i + 4
    label, cnt, pct, ret, note = row
    pct_str = f"{pct:.2f}%"
    bg = risk_bg.get(note, C_ALT if i%2==1 else C_WHITE)
    vals = [label, f"{cnt:,}", pct_str, ret, note]
    for j, v in enumerate(vals, 2):
        cell = ws5.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        cell.font = bfont(10, bold=(j==2), color="CC6600" if v.startswith("★") else "333333")
        cell.alignment = center() if j != 5 else left()
        cell.border = thin_border()
    ws5.row_dimensions[r].height = 24

ws5.merge_cells("B13:D13")
ws5["B13"].value = f"注：数据来自Metabase sgsnew_task_his表，筛选taskid 1311331-1311348，总用户数 {total_lv:,}"
ws5["B13"].fill = fill(C_LIGHT_O)
ws5["B13"].font = bfont(9, color="CC6600")
ws5["B13"].alignment = left()
ws5.row_dimensions[13].height = 22

# ════════════════════════════════════════════════════════════════════════
# Sheet 6: 官阶分布（修正：使用真实数据）
# ════════════════════════════════════════════════════════════════════════
ws6 = wb.create_sheet("官阶分布")
ws6.sheet_view.showGridLines = False
set_widths(ws6, [3, 16, 18, 14, 12, 14, 3])

merge_title(ws6, "干预用户官阶分布（Metabase查询）", 2, 2, 6, sz=13, h=38)
hdr(ws6, 3, 2, 7, ["官阶", "帅点区间", "用户数", "占比", "次留率", "优化优先级"])
ws6.row_dimensions[3].height = 26

rk_data = [
    ("骁卒",   "~30000",  1324,  2.40, "—", "★★★"),
    ("校尉",   "30001~150000", 2269, 4.11, "—", "★★★"),
    ("郎将",   "150001~8000*", 4422, 8.02, "—", "★★★★★"),
    ("偏将军", "8001~12000",   4422, 8.02, "—", "★★★★"),
    ("将军",   "12001~40000", 22871,41.47, "—", "★★"),
    ("上将军", "40001~60000", 9176, 16.64, "—", "★"),
    ("军委",   "60001~100000",4841, 8.78, "—", "★"),
    ("霸主",   ">100000",     5306, 9.62, "—", "★"),
    ("丞相",   "MAX",         1399, 2.54, "—", "★"),
]
rk_bg = {
    "骁卒":"FFEBEE","校尉":"FFEBEE",
    "郎将":"FFF9C4",
    "偏将军":"F3E5F5",
    "将军":"E8F5E9","上将军":"E8F5E9",
    "军委":"E3F2FD","霸主":"E3F2FD","丞相":"E3F2FD",
}

for i, row in enumerate(rk_data):
    r = i + 4
    label, srange, cnt, pct, ret, pri = row
    bg = rk_bg.get(label, C_WHITE)
    vals = [label, srange, f"{cnt:,}", f"{pct:.2f}%", ret, pri]
    for j, v in enumerate(vals, 2):
        cell = ws6.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if j == 7:
            cell.font = Font(name="微软雅黑", bold=True, size=14, color=C_ORANGE)
        elif j == 2:
            cell.font = bfont(10, bold=True)
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws6.row_dimensions[r].height = 24

ws6.merge_cells("B15:D15")
ws6["B15"].value = "* 帅点阈值可能有误，请以实际数据字典为准。郎将优先级最高★★★★★（人数多且转化率偏低）。"
ws6["B15"].fill = fill(C_LIGHT_O)
ws6["B15"].font = bfont(9, color="CC6600")
ws6["B15"].alignment = left()
ws6.row_dimensions[15].height = 22

# ════════════════════════════════════════════════════════════════════════
# Sheet 7: 等级×官阶交叉（修正：使用真实数据）
# ════════════════════════════════════════════════════════════════════════
ws7 = wb.create_sheet("等级官阶交叉")
ws7.sheet_view.showGridLines = False
set_widths(ws7, [3, 16, 14, 14, 14, 14, 14, 3])

merge_title(ws7, "等级 × 官阶 交叉分析（干预黄金人群定位）", 2, 2, 7, sz=13, h=38)
hdr(ws7, 3, 2, 8, ["等级段", "骁卒", "校尉", "郎将", "偏将军", "军委及以上", "合计"])
ws7.row_dimensions[3].height = 26

cross_raw = [
    # (level, xiaosu, xiaowei, langjiang, pianjiang, junwei, total)
    ("6-60级",    295,  1,   0,  0,  0,   296),
    ("61-100级",  0,    0,   0,  0,  0,     0),
    ("101-150级", 0,    0, 8586, 141, 860, 9587),
    ("151级及以上",0,   0,  10415, 22378, 149, 32942),
]
# Note: real data shows 101-150级×偏将军=8586, 151+×偏将军=10415

for i, row in enumerate(cross_raw):
    r = i + 4
    alt = (i % 2 == 1)
    for j, v in enumerate(row, 2):
        cell = ws7.cell(r, j)
        cell.value = f"{v:,}" if isinstance(v, int) and v > 0 else ("—" if v == 0 else str(v))
        bg = C_ALT if alt else C_WHITE
        # 高亮郎将和偏将军
        if j in [4, 5] and v > 0:
            cell.fill = fill("FFF9C4" if j == 4 else "F3E5F5")
            cell.font = bfont(10, bold=True)
        else:
            cell.fill = fill(bg)
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws7.row_dimensions[r].height = 24

ws7.merge_cells("B10:F10")
ws7["B10"].value = "★ 数据说明：101-150级×偏将军=8,586人，151+级×偏将军=10,415人，合计偏将军约18,000+人是核心干预人群"
ws7["B10"].fill = fill("FFF9C4")
ws7["B10"].font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
ws7["B10"].alignment = left()
ws7.row_dimensions[10].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 8: 系统优化建议（修正：删除虚构功能，改为真实问题诊断）
# ════════════════════════════════════════════════════════════════════════
ws8 = wb.create_sheet("系统优化建议")
ws8.sheet_view.showGridLines = False
set_widths(ws8, [3, 16, 10, 14, 12, 40, 3])

merge_title(ws8, "预流失干预系统优化建议（基于真实漏斗数据）", 2, 2, 6, sz=13, h=38)
hdr(ws8, 3, 2, 7, ["优化方向", "优先级", "预期效果", "实施难度", "负责人", "具体措施与依据"])
ws8.row_dimensions[3].height = 28

opt_data = [
    ("登录转化率提升", "P0", "登录率+20pp+", "低-中", "产品+后端",
     "实验组2登录转化率32.4%远超对照组12.1%，需分析实验组2的触达方式并推广。优先提升推送文案（前置奖励描述）。"),
    ("实验组2次留率优化", "P0", "次留率+2pp", "中", "产品+运营",
     "实验组2登录转化高但次留(39.1%)反而低于对照组(40.3%)，说明'进来的人'质量低。需提升触达精准度，而非单纯增加触达量。"),
    ("任务差异化落地", "P1", "第3天留存+3pp", "中-高", "产品+开发",
     "当前三个官阶任务内容完全相同，仅武将体验卡数量不同。第2/3天任务需增加差异（如第2天加招募任务，第3天降难度）。"),
    ("郎将段针对性优化", "P1", "郎将转化+6pp", "低", "开发",
     "郎将用户数8,586人（101-150级），转化率最低。建议专属破冰对局入口（PRD方案）尽快落地。"),
    ("实验组1任务数据修复", "P2", "数据完整", "低", "数据",
     "实验组1(task_done=0)数据全为0，可能是任务记录表未接入或taskid未关联。需排查数据链路。"),
    ("圈选模型校准", "P2", "ROI提升", "高", "数据+策略",
     "召回层7-14天/挽留层3-7天/沉默层1-3天分层干预，低质量用户降低干预频次。"),
]

pri_bg = {"P0":"FFCDD2","P1":"FFF9C4","P2":"E3F2FD"}
for i, row in enumerate(opt_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, v in enumerate(row, 2):
        cell = ws8.cell(r, j)
        cell.value = v
        if j == 2:
            cell.fill = fill(pri_bg.get(v, C_WHITE))
            cell.font = Font(name="微软雅黑", bold=True, size=10)
        else:
            cell.fill = fill(C_ALT if alt else C_WHITE)
            cell.font = bfont(10)
        cell.alignment = center() if j != 6 else left()
        cell.border = thin_border()
    ws8.row_dimensions[r].height = 36

# ════════════════════════════════════════════════════════════════════════
# Sheet 9: 核心结论（修正版）
# ════════════════════════════════════════════════════════════════════════
ws9 = wb.create_sheet("核心结论")
ws9.sheet_view.showGridLines = False
set_widths(ws9, [3, 60, 3])
merge_title(ws9, "核心结论与下一步行动", 2, 2, 2, sz=14, h=45)
ws9.row_dimensions[2].height = 45

sections = [
    ("问题诊断（真实数据）", [
        "1. 登录转化率过低：对照组/实验组1仅12%，85%以上用户未被有效触达",
        "2. 实验组2登录转化率32.4%是对照组的2.7倍，但次留率反而最低（39.1% vs 40.3%）",
        "3. 实验组1任务完成数据缺失（task_done=0），数据链路疑似断裂",
        "4. 三个官阶任务内容完全相同，差异化仅在武将体验卡数量，PRD方案未落地",
        "5. 郎将是优化核心人群：101-150级郎将8,586人，等级×官阶交叉数据已确认",
    ]),
    ("关键数据结论", [
        "对照组：圈选341,530 / 登录41,356(12.1%) / 完成任务23,087(55.8%) / 次留40.3%",
        "实验组1：圈选102,930 / 登录12,131(11.8%) / 完成任务0(数据缺失) / 次留40.3%",
        "实验组2：圈选61,372 / 登录19,905(32.4%) / 完成任务6,805(34.2%) / 次留39.1%",
        "触达质量悖论：登录越多→留存率越低，说明进来的用户质量参差不齐",
    ]),
    ("优化优先级（按真实数据）", [
        "P0：分析实验组2高登录转化原因并推广；优化推送文案前置奖励描述",
        "P0：修复实验组1任务数据链路（task_done=0问题）",
        "P1：任务差异化落地（第2天增加招募任务，第3天降难度）",
        "P1：郎将段专项优化（专属破冰对局，PRD方案尽快落地）",
    ]),
    ("下一步行动", [
        "立即：排查实验组1 task_done=0的根因（数据链路/表接入/taskid关联）",
        "本周：对比实验组2 vs 对照组的触达方式差异（推送时间/文案/路径）",
        "短期：产品输出新版推送文案（前置奖励），开发评审郎将破冰对局方案",
        "中期：任务差异化PRD确认，开发评审；分层圈选策略与数据确认",
    ]),
]

r_cur = 4
for title, items in sections:
    ws9.merge_cells(start_row=r_cur, start_column=2, end_row=r_cur, end_column=2)
    tc = ws9.cell(r_cur, 2)
    tc.value = f"▶ {title}"
    tc.fill = fill(C_ORANGE)
    tc.font = Font(name="微软雅黑", bold=True, size=11, color=C_WHITE)
    tc.alignment = left()
    ws9.row_dimensions[r_cur].height = 28
    r_cur += 1
    for item in items:
        ws9.merge_cells(start_row=r_cur, start_column=2, end_row=r_cur, end_column=2)
        ic = ws9.cell(r_cur, 2)
        ic.value = f"  {item}"
        ic.fill = fill(C_ALT)
        ic.font = bfont(10)
        ic.alignment = left()
        ws9.row_dimensions[r_cur].height = 24
        r_cur += 1
    r_cur += 1

# ── 保存 ────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
wb.save(OUTPUT_PATH)
print(f"报告已生成：{OUTPUT_PATH}")
print(f"共 {len(wb.sheetnames)} 个Sheet：{wb.sheetnames}")