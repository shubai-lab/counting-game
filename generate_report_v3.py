# -*- coding: utf-8 -*-
"""
预流失干预数据分析报告生成脚本 - v3
基于 Metabase 真实查询结果 + 原始漏斗 Excel 数据
修正：官阶阈值、组别标签、全部虚构数据
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json, os

OUTPUT_PATH = r"C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预\预流失干预数据分析报告_v5.xlsx"

wb = openpyxl.Workbook()
wb.remove(wb.active)

# ── 颜色常量 ──────────────────────────────────────────────────────────
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

def note_row(ws, row, c1, c2, text, bg=C_LIGHT_O, color="CC6600", h=22):
    ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    c = ws.cell(row, c1)
    c.value = text
    c.fill = fill(bg)
    c.font = bfont(9, color=color)
    c.alignment = left()
    ws.row_dimensions[row].height = h

def section_head(ws, row, c1, c2, text, h=28):
    ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    c = ws.cell(row, c1)
    c.value = f"▶ {text}"
    c.fill = fill(C_ORANGE)
    c.font = Font(name="微软雅黑", bold=True, size=11, color=C_WHITE)
    c.alignment = left()
    ws.row_dimensions[row].height = h

def item_row(ws, row, c1, c2, text, h=22):
    ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    c = ws.cell(row, c1)
    c.value = f"  {text}"
    c.fill = fill(C_ALT)
    c.font = bfont(10)
    c.alignment = left()
    ws.row_dimensions[row].height = h

# ════════════════════════════════════════════════════════════════════════
# 读取真实漏斗数据
# ════════════════════════════════════════════════════════════════════════
with open(r"C:/Users/zhangfan/my-openspec-project/funnel_data.json", encoding="utf-8") as f:
    funnel = json.load(f)

agg = funnel["agg"]   # {"0":数据部实验组, "1":对照组, "2":算法实验组}
daily = funnel["daily"]

# 组别映射：gid → (显示名, 背景色, ALT色)
GROUP_META = {
    0: ("数据部实验组", "E3F2FD", "DDEEFF"),
    1: ("对照组",       "FFF3E0", "FFE8CC"),
    2: ("算法实验组",   "E8F5E9", "CCEECC"),
}

# ════════════════════════════════════════════════════════════════════════
# Sheet 1: 封面
# ════════════════════════════════════════════════════════════════════════
ws_cover = wb.create_sheet("封面")
ws_cover.sheet_view.showGridLines = False
set_widths(ws_cover, [3, 28, 52, 3])
for r in range(1, 28): ws_cover.row_dimensions[r].height = 26

merge_title(ws_cover, "预流失干预数据分析报告", 3, 2, 3, sz=16, h=50)

ws_cover.merge_cells("B5:C5")
ws_cover["B5"].value = "分析日期：2026-04-28  |  数据来源：Metabase Impala + Excel原始数据"
ws_cover["B5"].font = bfont(11, color=C_GRAY)
ws_cover["B5"].alignment = left()

ws_cover.merge_cells("B6:C6")
ws_cover["B6"].value = "数据范围：漏斗 2026-04-08~04-27 / 等级官阶 2026-02-07~03-04"
ws_cover["B6"].font = bfont(11, color=C_GRAY)
ws_cover["B6"].alignment = left()

merge_title(ws_cover, "核心漏斗数据（累计）", 8, 2, 3, sz=11, h=32)

# 三个组的核心指标卡片
cards_data = [
    (0, "341,530", "登录率 12.1%", "次留率 40.3%",  "7天留 35.5%"),
    (1, "102,930", "登录率 11.8%", "次留率 40.3%",  "7天留 35.1%"),
    (2,  "61,372", "登录率 32.4%", "次留率 39.1%",  "7天留 32.2%"),
]
for i, (gid, sel, lgr, d3r, d7r) in enumerate(cards_data):
    name, bg, _ = GROUP_META[gid]
    r = 10 + i * 5

    ws_cover.merge_cells(start_row=r,   start_column=2, end_row=r,   end_column=3)
    c0 = ws_cover.cell(r, 2)
    c0.value = f"  {name}  |  圈选 {sel} 人"
    c0.fill = fill(C_DARK)
    c0.font = Font(name="微软雅黑", bold=True, size=12, color=C_GOLD)
    c0.alignment = left()
    ws_cover.row_dimensions[r].height = 26

    ws_cover.merge_cells(start_row=r+1, start_column=2, end_row=r+1, end_column=2)
    ws_cover.merge_cells(start_row=r+1, start_column=3, end_row=r+1, end_column=3)
    c1 = ws_cover.cell(r+1, 2); c1.value = lgr
    c1.fill = fill(C_ORANGE); c1.font = Font(name="微软雅黑", bold=True, size=18, color=C_WHITE); c1.alignment = center()
    c2 = ws_cover.cell(r+1, 3); c2.value = d3r
    c2.fill = fill(C_ORANGE); c2.font = Font(name="微软雅黑", size=14, color=C_WHITE); c2.alignment = center()

    ws_cover.merge_cells(start_row=r+2, start_column=2, end_row=r+2, end_column=3)
    c3 = ws_cover.cell(r+2, 2); c3.value = d7r
    c3.fill = fill(bg); c3.font = Font(name="微软雅黑", size=13, color=C_GRAY); c3.alignment = center()

ws_cover.merge_cells("B24:C24")
ws_cover["B24"].value = "疏白 · 数据分析助手"
ws_cover["B24"].font = Font(name="微软雅黑", size=10, color=C_GRAY)
ws_cover["B24"].alignment = center()

# ════════════════════════════════════════════════════════════════════════
# Sheet 2: 漏斗总览
# ════════════════════════════════════════════════════════════════════════
ws_funnel = wb.create_sheet("漏斗总览")
ws_funnel.sheet_view.showGridLines = False
set_widths(ws_funnel, [3, 14, 16, 14, 14, 14, 14, 3])

merge_title(ws_funnel, "预流失干预漏斗总览（对照组 vs 数据部实验组 vs 算法实验组）", 2, 2, 7, sz=13, h=40)

hdr(ws_funnel, 3, 2, 8, ["组别", "预流失圈选", "登录用户", "完成任务", "登录转化率", "任务完成率", "加权次留率"])

funnel_rows = [
    ("数据部实验组", 341530, 41356, 23087, "12.1%", "55.8%", "40.3%", "E3F2FD"),
    ("对照组",      102930, 12131, 0,      "11.8%", "—",     "40.3%", "FFF3E0"),
    ("算法实验组",   61372, 19905, 6805,  "32.4%", "34.2%", "39.1%", "E8F5E9"),
]

for i, (name, sel, log, task, lgr, task_r, d3r, bg) in enumerate(funnel_rows):
    r = i + 4
    vals = [name, f"{sel:,}", f"{log:,}", f"{task:,}" if task else "—", lgr, task_r, d3r]
    for j, v in enumerate(vals, 2):
        cell = ws_funnel.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if j == 2:
            cell.font = bfont(10, bold=True)
        elif j == 6 and v == "32.4%":
            cell.font = Font(name="微软雅黑", bold=True, size=12, color=C_GREEN)
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws_funnel.row_dimensions[r].height = 28

note_row(ws_funnel, 8, 2, 7,
    "注：完成任务 = 登录后完成任意1个战场重燃任务（taskid 1311331-1311348），对照组任务数据全为0疑似数据链路问题")

# 任务结构说明
merge_title(ws_funnel, "任务结构说明（18个taskid = 3个官阶组 × 3天 × 2任务）", 11, 2, 8, sz=11, h=32)
hdr(ws_funnel, 12, 2, 8, ["官阶组别", "天数", "任务ID范围", "任务内容", "奖励", "数据状态"])

task_struct = [
    ("郎将及以下", "第1天", "1311331-1311332", "每日登录 + 任意模式完成1局", "武将体验卡×2", "有数据"),
    ("偏将军",     "第1天", "1311337-1311338", "每日登录 + 任意模式完成1局", "武将体验卡×2", "有数据"),
    ("将军及以上", "第1天", "1311343-1311344", "每日登录 + 任意模式完成1局", "武将体验卡×2", "有数据"),
    ("各官阶组",   "第2天", "1311333-1311334等", "每日登录 + 任意模式完成1局", "武将体验卡×2", "有数据"),
    ("各官阶组",   "第3天", "1311335-1311336等", "每日登录 + 任意模式完成1局", "武将体验卡×2", "完成率最低"),
]
task_bg = ["FFF9C4","F3E5F5","E8F5E9","EEEEEE","EEEEEE"]
for i, row in enumerate(task_struct):
    r = i + 14
    for j, v in enumerate(row, 2):
        cell = ws_funnel.cell(r, j)
        cell.value = v
        cell.fill = fill(task_bg[i])
        cell.font = bfont(9, bold=(j==2))
        cell.alignment = center() if j != 4 else left()
        cell.border = thin_border()
    ws_funnel.row_dimensions[r].height = 22

ws_funnel.merge_cells("B20:H20")
c = ws_funnel.cell(20, 2)
c.value = "★ 核心发现：三个官阶任务内容完全相同，差异化仅在武将体验卡数量。PRD方案（破冰对局/任务差异化）尚未落地。"
c.fill = fill("FFCDD2")
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC0000")
c.alignment = left()
ws_funnel.row_dimensions[20].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 3: 留存率对比
# ════════════════════════════════════════════════════════════════════════
ws_ret = wb.create_sheet("留存率对比")
ws_ret.sheet_view.showGridLines = False
set_widths(ws_ret, [3, 18, 18, 18, 18, 3])
merge_title(ws_ret, "留存率对比（对照组 vs 数据部实验组 vs 算法实验组）", 2, 2, 5, sz=13, h=40)

hdr(ws_ret, 3, 2, 6, ["指标", "数据部实验组", "对照组", "算法实验组", "最优组"])

ret_data = [
    ("预流失圈选用户",  "341,530", "102,930",  "61,372",   "数据部实验组(圈选最多)"),
    ("登录转化率",      "12.1%",   "11.8%",    "32.4%",    "算法实验组 ▲▲"),
    ("完成任务用户",    "23,087",  "0(数据缺失)", "6,805",  "数据部实验组"),
    ("任务完成率",      "55.8%",   "—",        "34.2%",    "数据部实验组"),
    ("加权次留率",      "40.3%",   "40.3%",    "39.1%",    "数据部实验组≈对照组"),
    ("加权7天留存",     "35.5%",   "35.1%",    "32.2%",    "数据部实验组"),
    ("实验组 vs 对照组", "基准",    "—",        "-1.2pp",   "对照组更优"),
]

ret_row_bg = ["E3F2FD","FFF3E0","E8F5E9","E3F2FD","FFF3E0","E8F5E9","F0F0F0"]
for i, row in enumerate(ret_data):
    r = i + 4
    for j, v in enumerate(row, 2):
        cell = ws_ret.cell(r, j)
        cell.value = v
        cell.fill = fill(ret_row_bg[i])
        if j == 2:
            cell.font = bfont(10, bold=True)
        elif j == 6 and "▲▲" in v:
            cell.font = Font(name="微软雅黑", bold=True, size=11, color=C_GREEN)
        elif v == "0(数据缺失)":
            cell.font = bfont(10, color=C_RED)
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws_ret.row_dimensions[r].height = 26

ws_ret.merge_cells("B13:D13")
c = ws_ret.cell(13, 2)
c.value = "核心发现：算法实验组登录转化率(32.4%)是其他组的2.7倍，但次留率(39.1%)反而最低——触达量大但用户质量低。对照组/数据部实验组登录率~12%但留存更高，说明干预深度 > 触达广度。"
c.fill = fill(C_LIGHT_O)
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
c.alignment = left()
ws_ret.row_dimensions[13].height = 32

# ════════════════════════════════════════════════════════════════════════
# Sheet 4: 每日漏斗明细
# ════════════════════════════════════════════════════════════════════════
ws_day = wb.create_sheet("每日漏斗明细")
ws_day.sheet_view.showGridLines = False
set_widths(ws_day, [3, 12, 12, 12, 12, 12, 10, 10, 3])

merge_title(ws_day, "每日漏斗明细（2026-04-08 ~ 2026-04-27）", 2, 2, 8, sz=13, h=40)
hdr(ws_day, 3, 2, 9, ["日期", "组别", "圈选用户", "登录用户", "完成任务", "登录转化率", "次留率", "7天留存"])

daily_sorted = sorted(daily, key=lambda x: (x["date"], x["gid"]))

for i, row in enumerate(daily_sorted):
    r = i + 4
    gid = row["gid"]
    sel, log, task = row["sel"], row["log"], row["task"]
    lgr = f"{log/sel*100:.1f}%" if sel > 0 else "—"
    d3  = f"{row['day3']*100:.1f}%" if row["day3"] else "—"
    d7  = f"{row['day7']*100:.1f}%" if row["day7"] else "—"
    task_str = f"{task:,}" if task else ("—" if sel > 0 else "—")

    name, bg, alt_bg = GROUP_META[gid]
    alt = (i % 2 == 1)
    vals = [row["date"][:10], name, f"{sel:,}", f"{log:,}", task_str, lgr, d3, d7]
    for j, v in enumerate(vals, 2):
        cell = ws_day.cell(r, j)
        cell.value = v
        if j == 3:
            cell.fill = fill(bg)
        elif alt:
            cell.fill = fill(alt_bg)
        else:
            cell.fill = fill(C_WHITE)
        cell.font = bfont(9, bold=(j==2 or j==3))
        cell.alignment = center()
        cell.border = thin_border()
    ws_day.row_dimensions[r].height = 20

note_row(ws_day, 4+len(daily_sorted), 2, 8,
    f"共 {len(daily_sorted)} 条记录 | — 表示数据为0或缺失 | 日期最近的几天留存数据尚未计算完成")

# ════════════════════════════════════════════════════════════════════════
# Sheet 5: 等级分布（真实 Metabase 数据，修正版 SQL）
# ════════════════════════════════════════════════════════════════════════
ws_lv = wb.create_sheet("等级分布")
ws_lv.sheet_view.showGridLines = False
set_widths(ws_lv, [3, 16, 14, 10, 12, 22, 3])

merge_title(ws_lv, "干预用户等级分布（Metabase查询，修正版 SQL：task_day 追踪次日留存）", 2, 2, 6, sz=13, h=40)
hdr(ws_lv, 3, 2, 7, ["等级段", "用户数", "占比", "次留率", "特征"])

# 真实数据（SQL 1 更新版：修复 task_day 追踪后次留率）
lv_data = [
    # (等级段, 用户数, 占比, 次留率, 特征)
    ("1-30级",      1576, 2.97, 18.27, "★ 低留存风险"),
    ("31-60级",     2869, 5.41, 30.36, ""),
    ("61-100级",    6734, 12.70, 35.58, "★ 可提升段"),
    ("101-150级",   9649, 18.19, 40.79, "★ 核心干预段"),
    ("151级以上",   33227, 62.64, 49.99, "主力人群"),
]
total_lv = 53055

note_bg = {"★ 低留存风险":"FFCDD2","★ 可提升段":"FFF9C4","★ 核心干预段":"F3E5F5"}
for i, row in enumerate(lv_data):
    r = i + 4
    label, cnt, pct, ret, note = row
    bg = note_bg.get(note, C_ALT if i%2==1 else C_WHITE)
    vals = [label, f"{cnt:,}", f"{pct:.2f}%", f"{ret:.2f}%", note]
    for j, v in enumerate(vals, 2):
        cell = ws_lv.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if v.startswith("★"):
            cell.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
        elif j == 2:
            cell.font = bfont(10, bold=True)
        elif j == 5:  # 次留率
            ret_val = float(v.rstrip('%'))
            cell.font = Font(name="微软雅黑", bold=True, size=10,
                             color=C_GREEN if ret_val >= 45 else (C_RED if ret_val < 35 else "333333"))
        else:
            cell.font = bfont(10)
        cell.alignment = center() if j != 5 else left()
        cell.border = thin_border()
    ws_lv.row_dimensions[r].height = 24

note_row(ws_lv, 10, 2, 5,
    f"总用户数 {total_lv:,} | 次留率=任务完成日次日是否登录（task_day+1） | 数据范围：2026-02-07~03-04")

# 等级分布图数据
ws_lv.merge_cells("B12:C12")
c = ws_lv.cell(12, 2)
c.value = "等级分布比例"
c.fill = fill(C_HEADER)
c.font = Font(name="微软雅黑", bold=True, size=10, color=C_WHITE)
c.alignment = center()

simple_bar = [
    ("1-30级",      2.97),
    ("31-60级",     5.41),
    ("61-100级",   12.70),
    ("101-150级",  18.19),
    ("151级以上",  62.64),
]
bar_start = 13
for i, (label, pct) in enumerate(simple_bar):
    r = bar_start + i
    ws_lv.cell(r, 2).value = label
    ws_lv.cell(r, 2).font = bfont(9)
    ws_lv.cell(r, 2).alignment = center()
    ws_lv.cell(r, 2).border = thin_border()
    bar_chars = int(pct / 3)
    ws_lv.cell(r, 3).value = "█" * bar_chars + "░" * (33-bar_chars) + f" {pct:.1f}%"
    ws_lv.cell(r, 3).font = Font(name="微软雅黑", size=9, color=C_ORANGE)
    ws_lv.cell(r, 3).alignment = left()
    ws_lv.cell(r, 3).border = thin_border()
    ws_lv.row_dimensions[r].height = 18

# ════════════════════════════════════════════════════════════════════════
# Sheet 6: 官阶分布（真实 Metabase 数据，修正版 SQL）
# ════════════════════════════════════════════════════════════════════════
ws_rk = wb.create_sheet("官阶分布")
ws_rk.sheet_view.showGridLines = False
set_widths(ws_rk, [3, 16, 18, 14, 12, 14, 3])

merge_title(ws_rk, "干预用户官阶分布（修正版 SQL：task_day 追踪 + ≤task_day 最近logout官阶）", 2, 2, 6, sz=13, h=40)
hdr(ws_rk, 3, 2, 7, ["官阶", "帅点区间", "用户数", "占比", "次留率", "优化优先级"])

# 真实数据（SQL 2 更新版：修复 task_day 追踪后次留率）
rk_data = [
    # (官阶, 帅点区间, 用户数, 次留率, 优先级)
    ("骁卒",     "< 4000",        4447, 35.96, "★★★"),
    ("校尉",     "4000 ~ 7999",    2326, 30.14, "★★★"),
    ("郎将",     "8000 ~ 11999",   5337, 52.35, "★★★★"),
    ("偏将军",   "12000 ~ 39999",  23034, 43.64, "★★★★★"),
    ("将军",     "40000 ~ 59999",   9240, 47.86, "★★"),
    ("上将军",   "60000 ~ 79999",   4886, 49.59, "★★"),
    ("国护军",   "80000 ~ 129999",  1424, 19.52, "★★★"),
    ("国都护",   "130000 ~ 159999", 1412, 54.75, "★"),
    ("卫将军",   "160000 ~ 199999", 1020, 51.27, "★"),
    ("车骑将军", "200000 ~ 249999",  525, 56.57, "★"),
    ("骠骑将军", "250000 ~ 349999",  256, 55.47, "★"),
    ("大将军",   "≥ 350000",         57, 61.40, "★"),
]
rk_bg = {
    "骁卒":"FFEBEE","校尉":"FFEBEE",
    "郎将":"FFF9C4",
    "偏将军":"F3E5F5",
    "将军":"E8F5E9","上将军":"E8F5E9",
    "国护军":"FFCDD2",
    "国都护":"E3F2FD","卫将军":"E3F2FD","车骑将军":"E3F2FD","骠骑将军":"E3F2FD","大将军":"E3F2FD",
}

total_rk = 53064

for i, row in enumerate(rk_data):
    r = i + 4
    label, srange, cnt, ret, pri = row
    bg = rk_bg.get(label, C_WHITE)
    pct = cnt / total_rk * 100
    vals = [label, srange, f"{cnt:,}", f"{pct:.2f}%", f"{ret:.2f}%", pri]
    for j, v in enumerate(vals, 2):
        cell = ws_rk.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if j == 7:
            cell.font = Font(name="微软雅黑", bold=True, size=14, color=C_ORANGE)
        elif j == 2:
            cell.font = bfont(10, bold=True)
        elif j == 5:  # 次留率
            ret_val = float(v.rstrip('%'))
            cell.font = Font(name="微软雅黑", bold=True, size=10,
                             color=C_GREEN if ret_val >= 50 else (C_RED if ret_val < 40 else "333333"))
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws_rk.row_dimensions[r].height = 24

note_row(ws_rk, 17, 2, 7,
    f"总用户数 {total_rk:,} | 次留率=task_day次日是否登录（task_day+1） | 官阶取≤task_day最近logout | 数据范围：2026-02-07~03-04")

ws_rk.merge_cells("B18:F18")
c = ws_rk.cell(18, 2)
c.value = "★ 高优先级优化：偏将军(23,034人/43.64%)为核心干预人群；骁卒(4,447人/35.96%)、校尉(2,326人/30.14%)、国护军(1,424人/19.52%)次留率最低，需重点关注"
c.fill = fill("FFCDD2")
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC0000")
c.alignment = left()
ws_rk.row_dimensions[18].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 7: 等级×官阶交叉
# ════════════════════════════════════════════════════════════════════════
ws_cross = wb.create_sheet("等级官阶交叉")
ws_cross.sheet_view.showGridLines = False
set_widths(ws_cross, [3, 16, 14, 14, 14, 14, 14, 3])

merge_title(ws_cross, "等级 × 官阶 交叉分析（Metabase查询，同一批用户，口径一致）", 2, 2, 7, sz=13, h=40)
hdr(ws_cross, 3, 2, 8, ["等级段", "骁卒", "校尉", "郎将", "偏将军", "将军及以上", "合计"])
ws_cross.row_dimensions[3].height = 26

# 真实数据（SQL 3 查询结果，整理后）
cross_data = [
    # (等级段, 骁卒, 校尉, 郎将, 偏将军, 将军及以上, 合计)
    ("1-30级",      939,   533,    87,     2,     20,   1581),
    ("31-60级",     294,   850,  1264,   259,      0,   2667),
    ("61-100级",    119,   580,  2137,  3560,      5,   6401),
    ("101-150级",    39,   184,   607,  8349,    127,   9306),
    ("151级以上",    11,    43,    91, 10210,  22301,  32656),
]

hl_colors = {4: "F3E5F5", 5: "E8F5E9"}  # 偏将军、将军及以上高亮
rank_colors_map = {2: "FFEBEE", 3: "FFEBEE", 4: "FFF9C4", 5: "F3E5F5", 6: "E8F5E9"}

for i, row in enumerate(cross_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, v in enumerate(row, 2):
        cell = ws_cross.cell(r, j)
        cell.value = f"{v:,}" if isinstance(v, int) else str(v)
        if j >= 3 and v > 0:
            cell.fill = fill(rank_colors_map.get(j, C_WHITE))
        elif alt:
            cell.fill = fill(C_ALT)
        else:
            cell.fill = fill(C_WHITE)
        cell.font = bfont(10, bold=(j==2 or (j in [5,6] and v > 1000)))
        cell.alignment = center()
        cell.border = thin_border()
    ws_cross.row_dimensions[r].height = 24

note_row(ws_cross, 10, 2, 7,
    "等级分布(53,055人)与官阶分布(53,064人)口径基本一致，误差9人为正常差异 | SQL 3未更新，交叉表沿用旧数据仅供参考")

ws_cross.merge_cells("B11:F11")
c = ws_cross.cell(11, 2)
c.value = "★ 核心干预人群：偏将军23,034人(43.4%)、将军9,240人(17.4%)、郎将5,337人(10.1%)，合计37,611人占70.9%"
c.fill = fill("FFF9C4")
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
c.alignment = left()
ws_cross.row_dimensions[11].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 8: 系统优化建议
# ════════════════════════════════════════════════════════════════════════
ws_opt = wb.create_sheet("系统优化建议")
ws_opt.sheet_view.showGridLines = False
set_widths(ws_opt, [3, 18, 10, 14, 12, 38, 3])

merge_title(ws_opt, "预流失干预系统优化建议（基于真实数据）", 2, 2, 6, sz=13, h=40)
hdr(ws_opt, 3, 2, 7, ["优化方向", "优先级", "预期效果", "实施难度", "负责人", "具体措施与依据"])
ws_opt.row_dimensions[3].height = 28

opt_data = [
    ("分析算法实验组高登录转化原因", "P0", "登录率+20pp+", "中", "产品+数据",
     "算法实验组登录转化32.4%是其他组(12%)的2.7倍，需分析其触达方式（推送时间/文案/路径），找出可复用因素。"),
    ("优化推送文案（前置奖励）", "P0", "触达转化+30-50%", "低", "产品",
     "当前文案五个人名堆叠，缺乏奖励感知。建议：'您的专属回归礼包：招募令×3 + 武将体验卡×2 已就位，点击领取'"),
    ("修复对照组任务数据缺失", "P0", "数据完整", "低", "数据+开发",
     "对照组task_done全为0，疑似数据链路断裂（sgsnew_task_his未关联对应taskid）。需排查数据接入。"),
    ("低留存官阶定向干预（骁卒/校尉/国护军）", "P0", "次留+5-10pp", "中", "产品+数据",
     "骁卒(35.96%)、校尉(30.14%)、国护军(19.52%)次留率极低，合计8,197人(15.4%)。建议专属召回文案+降低任务门槛（移除模式限制）。"),
    ("郎将段破冰机制落地", "P1", "郎将转化+6pp", "中", "产品+开发",
     "郎将用户5,337人(10.1%)，次留率52.35%。专属破冰对局入口（任务完成后弹出AI对局+即时奖励）尚未实现。"),
    ("第3天任务降难度", "P1", "第3天留存+3-5pp", "低", "开发",
     "三个官阶任务内容完全相同。第3天移除模式限制，完成任意1局即可，额外发放战令经验×500激励。"),
    ("分层奖励设计", "P1", "完成率+20%", "中", "产品+开发",
     "骁卒/校尉：资源类奖励（元宝×50、帅点×100）；将军及以上：社交认同奖励（专属称号、头像框）。"),
    ("圈选模型分层校准", "P2", "ROI提升", "高", "数据+策略",
     "召回层7-14天/挽留层3-7天/沉默层1-3天，低质量用户降低干预频次。需与数据确认最优阈值。"),
]

pri_bg = {"P0":"FFCDD2","P1":"FFF9C4","P2":"E3F2FD"}
for i, row in enumerate(opt_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, v in enumerate(row, 2):
        cell = ws_opt.cell(r, j)
        cell.value = v
        if j == 2:
            cell.fill = fill(pri_bg.get(v, C_WHITE))
            cell.font = Font(name="微软雅黑", bold=True, size=10)
        elif j == 4:
            diff = {"低":"C8E6C9","中":"FFF9C4","高":"FFCDD2"}.get(v, C_WHITE)
            cell.fill = fill(diff)
            cell.font = bfont(10)
        else:
            cell.fill = fill(C_ALT if alt else C_WHITE)
            cell.font = bfont(10)
        cell.alignment = center() if j not in [2, 6] else (left() if j == 6 else center())
        cell.border = thin_border()
    ws_opt.row_dimensions[r].height = 36

# ════════════════════════════════════════════════════════════════════════
# Sheet 9: 核心结论
# ════════════════════════════════════════════════════════════════════════
ws_con = wb.create_sheet("核心结论")
ws_con.sheet_view.showGridLines = False
set_widths(ws_con, [3, 62, 3])
merge_title(ws_con, "核心结论与下一步行动", 2, 2, 2, sz=14, h=48)
ws_con.row_dimensions[2].height = 48

sections = [
    ("问题诊断", [
        "1. 次留率偏低：骁卒(35.96%)、校尉(30.14%)、国护军(19.52%)次留率极低，合计8,197人(15.4%)需定向干预",
        "2. 触达转化率过低：对照组/数据部实验组登录率仅~12%，85%以上用户未被有效触达",
        "3. 算法实验组登录转化率32.4%是其他组的2.7倍，但次留率39.1%反而最低——触达量大但用户质量低",
        "4. 对照组任务完成数据全为0（task_done=0），数据链路疑似断裂，需排查",
        "5. 偏将军(23,034人，43.4%)是绝对主力干预人群，次留率43.64%，核心优化对象",
    ]),
    ("关键数据", [
        "数据部实验组：圈选341,530 / 登录41,356(12.1%) / 完成任务23,087(55.8%) / 次留40.3%",
        "对照组：圈选102,930 / 登录12,131(11.8%) / 完成任务0(数据缺失) / 次留40.3%",
        "算法实验组：圈选61,372 / 登录19,905(32.4%) / 完成任务6,805(34.2%) / 次留39.1%",
        "等级分布：151级以上33,227人(62.6%)为主力，次留49.99%；1-30级1,576人(2.97%)次留仅18.27%",
        "官阶分布：偏将军23,034人(43.4%)最多，次留43.64%；高官阶（车骑/骠骑/大将军）次留56-61%表现较好",
    ]),
    ("优化优先级", [
        "P0：低留存官阶定向干预（骁卒30.14%、校尉35.96%、国护军19.52%专属召回文案+任务降门槛）",
        "P0：分析算法实验组高登录转化原因并推广；优化推送文案前置奖励描述",
        "P0：修复对照组任务数据链路（task_done=0根因排查）",
        "P1：偏将军23,034人专项优化（次留43.64%，提升空间大）；郎将段专项（破冰对局）",
        "P2：圈选模型分层校准（召回7-14天/挽留3-7天/沉默1-3天）",
    ]),
    ("下一步行动", [
        "立即（1-2天）：排查对照组task_done=0的数据链路问题；输出低留存官阶专项召回方案",
        "本周：对比算法实验组 vs 对照组的触达方式差异（推送时间/文案/路径）",
        "短期（1-2周）：产品输出新版推送文案（前置奖励）；骁卒/校尉任务降门槛评审",
        "中期（1个月）：任务差异化PRD确认；偏将军专项干预效果追踪",
    ]),
]

r_cur = 4
for title, items in sections:
    section_head(ws_con, r_cur, 2, 2, title)
    r_cur += 1
    for item in items:
        item_row(ws_con, r_cur, 2, 2, item)
        r_cur += 1
    r_cur += 1

# ── 保存 ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
wb.save(OUTPUT_PATH)
print(f"报告已生成：{OUTPUT_PATH}")
print(f"共 {len(wb.sheetnames)} 个Sheet：{wb.sheetnames}")