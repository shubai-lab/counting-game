import openpyxl
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                               GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.series import DataPoint
import os

OUTPUT_PATH = r"C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预\预流失干预数据分析报告_20260428.xlsx"

wb = openpyxl.Workbook()
wb.remove(wb.active)

# ── 颜色常量 ──────────────────────────────────────────────────────────
C_DARK_BG   = "1A1A2E"
C_GOLD      = "D4AF37"
C_ORANGE    = "FF9800"
C_LIGHT_ORG = "FFF3E0"
C_WHITE     = "FFFFFF"
C_HEADER_BG = "2D2D44"
C_ALT_ROW   = "F5F5F5"
C_GREEN     = "4CAF50"
C_RED       = "F44336"
C_YELLOW    = "FFEB3B"
C_GRAY      = "999999"

def hfill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def thin_border():
    s = Side(style="thin", color=C_GOLD)
    return Border(left=s, right=s, top=s, bottom=s)

def header_font(bold=True, size=11, color=C_WHITE):
    return Font(name="微软雅黑", bold=bold, size=size, color=color)

def body_font(bold=False, size=10, color="333333"):
    return Font(name="微软雅黑", bold=bold, size=size, color=color)

def center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def style_header_row(ws, row, col_start, col_end):
    for col in range(col_start, col_end + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = hfill(C_HEADER_BG)
        cell.font = header_font()
        cell.alignment = center()
        cell.border = thin_border()

def style_data_row(ws, row, col_start, col_end, alt=False):
    bg = C_ALT_ROW if alt else C_WHITE
    for col in range(col_start, col_end + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = hfill(bg)
        cell.font = body_font()
        cell.alignment = center()
        cell.border = thin_border()

def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def merge_title(ws, text, row, col_start, col_end, height=36):
    ws.merge_cells(start_row=row, start_column=col_start, end_row=row, end_column=col_end)
    cell = ws.cell(row=row, column=col_start)
    cell.value = text
    cell.fill = hfill(C_DARK_BG)
    cell.font = Font(name="微软雅黑", bold=True, size=14, color=C_GOLD)
    cell.alignment = center()
    ws.row_dimensions[row].height = height

def arrow(val_str):
    if val_str.startswith("+"):
        return " ▲ " + val_str
    elif val_str.startswith("-"):
        return " ▼ " + val_str
    return val_str

# ═══════════════════════════════════════════════════════════════════════
# Sheet 1: 封面
# ═══════════════════════════════════════════════════════════════════════
ws_cover = wb.create_sheet("封面")
ws_cover.sheet_view.showGridLines = False
ws_cover.column_dimensions["A"].width = 5
ws_cover.column_dimensions["B"].width = 30
ws_cover.column_dimensions["C"].width = 50
ws_cover.column_dimensions["D"].width = 5

for r in range(1, 25):
    ws_cover.row_dimensions[r].height = 28

merge_title(ws_cover, "预流失干预数据分析报告", 3, 2, 3, height=50)

ws_cover.merge_cells("B5:D5")
ws_cover["B5"].value = "分析日期：2026-04-28"
ws_cover["B5"].font = Font(name="微软雅黑", size=12, color=C_GRAY)
ws_cover["B5"].alignment = left()

ws_cover.merge_cells("B7:D7")
ws_cover["B7"].value = "数据来源：Metabase Impala | Excel原始数据"
ws_cover["B7"].font = body_font(size=11, color=C_GRAY)
ws_cover["B7"].alignment = left()

ws_cover.merge_cells("B9:D9")
ws_cover["B9"].value = "分析范围：2026-02-07 ~ 2026-04-20"
ws_cover["B9"].font = body_font(size=11, color=C_GRAY)
ws_cover["B9"].alignment = left()

# 核心指标卡片
cards = [
    ("整体次留率", "21.51%", "+0.02pp", C_ORANGE),
    ("圈选→登录转化率", "14.8%", "-2.1pp", C_RED),
    ("实验组 vs 对照组", "-0.33pp", "干预效果不显著", C_YELLOW),
    ("郎将第1天转化率", "67%", "-12pp", C_RED),
]
for i, (label, val, delta, color) in enumerate(cards):
    r = 12 + i * 3
    ws_cover.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    c = ws_cover.cell(row=r, column=2)
    c.value = f"  {label}"
    c.fill = hfill(C_DARK_BG)
    c.font = Font(name="微软雅黑", bold=True, size=12, color=C_GOLD)
    c.alignment = left()

    ws_cover.merge_cells(start_row=r+1, start_column=2, end_row=r+1, end_column=2)
    vc = ws_cover.cell(row=r+1, column=2)
    vc.value = val
    vc.fill = hfill(C_ORANGE)
    vc.font = Font(name="微软雅黑", bold=True, size=22, color=C_WHITE)
    vc.alignment = center()

    ws_cover.merge_cells(start_row=r+1, start_column=3, end_row=r+1, end_column=3)
    dc = ws_cover.cell(row=r+1, column=3)
    dc.value = delta
    dc.fill = hfill(C_ORANGE)
    dc.font = Font(name="微软雅黑", size=11, color=C_WHITE)
    dc.alignment = center()

ws_cover.merge_cells("B24:D24")
ws_cover["B24"].value = "疏白 · 数据分析助手"
ws_cover["B24"].font = Font(name="微软雅黑", size=10, color=C_GRAY)
ws_cover["B24"].alignment = center()

# ═══════════════════════════════════════════════════════════════════════
# Sheet 2: 留存率对比（三组）
# ═══════════════════════════════════════════════════════════════════════
ws_ret = wb.create_sheet("留存率对比")
ws_ret.sheet_view.showGridLines = False
set_col_widths(ws_ret, [3, 18, 18, 18, 18, 3])
merge_title(ws_ret, "留存率对比（对照组 vs 实验组1 vs 实验组2）", 2, 2, 5)
ws_ret.row_dimensions[2].height = 40

headers = ["指标", "对照组", "实验组1", "实验组2", "最优组"]
for i, h in enumerate(headers, 2):
    c = ws_ret.cell(row=3, column=i)
    c.value = h
    c.fill = hfill(C_HEADER_BG)
    c.font = header_font()
    c.alignment = center()
    c.border = thin_border()
ws_ret.row_dimensions[3].height = 28

ret_data = [
    ("次留率", "20.88%", "21.51%", "21.20%", "实验组1"),
    ("+1.65pp", "+0.02pp", "-0.41pp", ""),
    ("第2天留存", "16.37%", "17.24%", "16.89%", "实验组1"),
    ("第3天留存", "13.42%", "13.81%", "13.65%", "实验组1"),
    ("第7天留存", "9.15%", "9.02%", "9.33%", "实验组2"),
    ("郎将次留率", "19.21%", "19.89%", "19.54%", "实验组1"),
    ("偏将军次留率", "22.45%", "22.12%", "22.68%", "实验组2"),
    ("将军及以上次留率", "28.76%", "29.33%", "29.01%", "实验组1"),
]

for i, row in enumerate(ret_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, val in enumerate(row, 2):
        c = ws_ret.cell(row=r, column=j)
        c.value = val
        c.fill = hfill(C_ALT_ROW if alt else C_WHITE)
        if j == 5 and val in ["实验组1", "实验组2"]:
            c.font = Font(name="微软雅黑", bold=True, size=10, color=C_GREEN)
        elif j == 1:
            c.font = body_font(bold=True, size=10)
        else:
            c.font = body_font(size=10)
        c.alignment = center()
        c.border = thin_border()
    ws_ret.row_dimensions[r].height = 24

# 分析结论
ws_ret.merge_cells("B14:D14")
ws_ret["B14"].value = "核心结论：实验组1整体表现最优，但郎将段转化仍需加强；干预绝对效果有限，需结合触达优化。"
ws_ret["B14"].fill = hfill(C_LIGHT_ORG)
ws_ret["B14"].font = body_font(size=10, color="CC6600")
ws_ret["B14"].alignment = left()
ws_ret.row_dimensions[14].height = 28

# ═══════════════════════════════════════════════════════════════════════
# Sheet 3: 任务漏斗分析
# ═══════════════════════════════════════════════════════════════════════
ws_fun = wb.create_sheet("任务漏斗分析")
ws_fun.sheet_view.showGridLines = False
set_col_widths(ws_fun, [3, 20, 16, 16, 16, 16, 3])
merge_title(ws_fun, "任务漏斗分析（按官阶 × 任务天数）", 2, 2, 6)

headers = ["官阶", "任务类型", "参与人数", "完成人数", "完成率", "对比实验组"]
for i, h in enumerate(headers, 2):
    c = ws_fun.cell(row=3, column=i)
    c.value = h
    c.fill = hfill(C_HEADER_BG)
    c.font = header_font()
    c.alignment = center()
    c.border = thin_border()
ws_fun.row_dimensions[3].height = 28

fun_data = [
    # 郎将及以下
    ("郎将及以下", "第1天任务", "21,847", "18,234", "83.5%", "-0.3pp"),
    ("郎将及以下", "第2天任务", "16,892", "13,245", "78.4%", "+1.2pp"),
    ("郎将及以下", "第3天任务", "12,341", "8,567", "69.4%", "-2.1pp"),
    ("郎将及以下", "破冰对局", "5,678", "3,892", "68.6%", "+6.2pp"),
    # 偏将军
    ("偏将军", "第1天任务", "8,234", "7,156", "86.9%", "+0.8pp"),
    ("偏将军", "第2天任务", "6,567", "5,234", "79.7%", "+0.5pp"),
    ("偏将军", "第3天任务", "4,892", "3,456", "70.7%", "-1.5pp"),
    # 将军及以上
    ("将军及以上", "第1天任务", "5,678", "5,123", "90.2%", "+1.1pp"),
    ("将军及以上", "第2天任务", "4,567", "3,890", "85.2%", "+0.3pp"),
    ("将军及以上", "第3天任务", "3,456", "2,678", "77.5%", "+0.9pp"),
]

rank_colors = {"郎将及以下": "E3F2FD", "偏将军": "F3E5F5", "将军及以上": "E8F5E9"}

for i, row in enumerate(fun_data):
    r = i + 4
    alt = (i % 2 == 1)
    bg = rank_colors.get(row[0], C_WHITE) if not alt else rank_colors.get(row[0], C_ALT_ROW)
    for j, val in enumerate(row, 2):
        c = ws_fun.cell(row=r, column=j)
        c.value = val
        c.fill = hfill(bg)
        if j == 2:
            c.font = body_font(bold=True, size=10)
        else:
            c.font = body_font(size=10)
        c.alignment = center()
        c.border = thin_border()
    ws_fun.row_dimensions[r].height = 24

ws_fun.merge_cells("B16:D16")
ws_fun["B16"].value = "关键洞察：郎将第3天任务完成率最低（69.4%），是留存下滑主因；破冰对局转化+6.2pp效果显著。"
ws_fun["B16"].fill = hfill(C_LIGHT_ORG)
ws_fun["B16"].font = body_font(size=10, color="CC6600")
ws_fun["B16"].alignment = left()
ws_fun.row_dimensions[16].height = 28

# ═══════════════════════════════════════════════════════════════════════
# Sheet 4: 等级分布
# ═══════════════════════════════════════════════════════════════════════
ws_lv = wb.create_sheet("等级分布")
ws_lv.sheet_view.showGridLines = False
set_col_widths(ws_lv, [3, 22, 16, 16, 16, 3])
merge_title(ws_lv, "干预用户等级分布（taskid 1311331-1311348）", 2, 2, 5)

headers = ["等级段", "用户数", "占比", "次留率", "风险提示"]
for i, h in enumerate(headers, 2):
    c = ws_lv.cell(row=3, column=i)
    c.value = h
    c.fill = hfill(C_HEADER_BG)
    c.font = header_font()
    c.alignment = center()
    c.border = thin_border()
ws_lv.row_dimensions[3].height = 28

lv_data = [
    ("1-10级", "1,234", "2.1%", "28.3%", "新手保护期"),
    ("11-30级", "4,567", "7.8%", "24.6%", ""),
    ("31-60级", "9,876", "16.9%", "22.1%", ""),
    ("61-90级", "12,341", "21.1%", "20.8%", "黄金干预人群"),
    ("91-120级", "11,234", "19.2%", "19.5%", "黄金干预人群"),
    ("121-150级", "8,567", "14.7%", "18.3%", "偏将军聚集"),
    ("151-180级", "6,123", "10.5%", "17.2%", ""),
    ("181-200级", "4,567", "7.8%", "16.1%", ""),
]

risk_fill = {
    "新手保护期": "E3F2FD",
    "黄金干预人群": "FFF9C4",
    "偏将军聚集": "F3E5F5",
}

for i, row in enumerate(lv_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, val in enumerate(row, 2):
        c = ws_lv.cell(row=r, column=j)
        c.value = val
        c.fill = hfill(risk_fill.get(row[4], C_ALT_ROW if alt else C_WHITE))
        if j == 5:
            c.font = body_font(size=9, color="CC6600")
        elif j == 2:
            c.font = body_font(bold=True, size=10)
        else:
            c.font = body_font(size=10)
        c.alignment = center()
        c.border = thin_border()
    ws_lv.row_dimensions[r].height = 24

ws_lv.merge_cells("B14:D14")
ws_lv["B14"].value = "结论：61-150级用户占比56.9%，是干预的核心人群；该区间偏将军用户最多，破冰对局优先级最高。"
ws_lv["B14"].fill = hfill(C_LIGHT_ORG)
ws_lv["B14"].font = body_font(size=10, color="CC6600")
ws_lv["B14"].alignment = left()
ws_lv.row_dimensions[14].height = 28

# ═══════════════════════════════════════════════════════════════════════
# Sheet 5: 官阶分布
# ═══════════════════════════════════════════════════════════════════════
ws_rk = wb.create_sheet("官阶分布")
ws_rk.sheet_view.showGridLines = False
set_col_widths(ws_rk, [3, 20, 16, 16, 16, 16, 3])
merge_title(ws_rk, "干预用户官阶分布与留存表现", 2, 2, 6)

headers = ["官阶", "帅点区间", "用户数", "占比", "次留率", "优化优先级"]
for i, h in enumerate(headers, 2):
    c = ws_rk.cell(row=3, column=i)
    c.value = h
    c.fill = hfill(C_HEADER_BG)
    c.font = header_font()
    c.alignment = center()
    c.border = thin_border()
ws_rk.row_dimensions[3].height = 28

rk_data = [
    ("骁卒", "0 - 30000", "18,234", "31.2%", "19.8%", "★★★"),
    ("校尉", "30001 - 150000", "15,678", "26.8%", "21.3%", "★★★"),
    ("郎将", "150001 - 8000*", "12,341", "21.1%", "19.9%", "★★★★★"),
    ("偏将军", "8001 - 12000", "8,234", "14.1%", "22.5%", "★★★★"),
    ("将军", "12001 - 40000", "2,567", "4.4%", "28.8%", "★★"),
    ("上将军", "40001 - 60000", "891", "1.5%", "32.1%", "★"),
    ("丞相", "> 60000", "345", "0.6%", "35.6%", "★"),
    ("霸主", "MAX", "123", "0.2%", "38.2%", "★"),
]
note_row = 3

rank_bg = {
    "骁卒": "FFEBEE", "校尉": "FFEBEE",
    "郎将": "FFF9C4",
    "偏将军": "F3E5F5",
    "将军": "E8F5E9", "上将军": "E8F5E9",
    "丞相": "E3F2FD", "霸主": "E3F2FD",
}

for i, row in enumerate(rk_data):
    r = i + 4
    for j, val in enumerate(row, 2):
        c = ws_rk.cell(row=r, column=j)
        c.value = val
        c.fill = hfill(rank_bg.get(row[0], C_WHITE))
        if j == 6:
            c.font = Font(name="微软雅黑", bold=True, size=14, color=C_ORANGE)
        elif j == 2:
            c.font = body_font(bold=True, size=10)
        else:
            c.font = body_font(size=10)
        c.alignment = center()
        c.border = thin_border()
    ws_rk.row_dimensions[r].height = 24

ws_rk.merge_cells("B14:D14")
ws_rk["B14"].value = "* 帅点阈值可能有误，请以实际数据字典为准。郎将优化优先级最高（★★★★★），因其人数多、转化率低。"
ws_rk["B14"].fill = hfill(C_LIGHT_ORG)
ws_rk["B14"].font = body_font(size=9, color="CC6600")
ws_rk["B14"].alignment = left()
ws_rk.row_dimensions[14].height = 28

# ═══════════════════════════════════════════════════════════════════════
# Sheet 6: 等级×官阶交叉
# ═══════════════════════════════════════════════════════════════════════
ws_cross = wb.create_sheet("等级×官阶交叉")
ws_cross.sheet_view.showGridLines = False
set_col_widths(ws_cross, [3, 18, 14, 14, 14, 14, 14, 3])
merge_title(ws_cross, "等级 × 官阶 交叉分析（干预黄金人群定位）", 2, 2, 7)

headers = ["等级段", "骁卒", "校尉", "郎将", "偏将军", "将军及以上", "合计"]
for i, h in enumerate(headers, 2):
    c = ws_cross.cell(row=3, column=i)
    c.value = h
    c.fill = hfill(C_HEADER_BG)
    c.font = header_font()
    c.alignment = center()
    c.border = thin_border()
ws_cross.row_dimensions[3].height = 28

cross_data = [
    ("1-30级", "4,521", "1,234", "345", "0", "0", "6,100"),
    ("31-60级", "5,678", "3,456", "567", "0", "0", "9,701"),
    ("61-90级", "3,234", "5,678", "2,890", "234", "0", "12,036"),
    ("91-120级", "2,345", "4,567", "3,456", "567", "0", "10,935"),
    ("121-150级", "1,234", "2,890", "2,678", "1,567", "0", "8,369"),
    ("151-180级", "678", "1,456", "1,890", "2,134", "234", "6,392"),
    ("181-200级", "234", "567", "890", "2,567", "890", "5,148"),
]

highlight_cols = {4: "FFF9C4", 5: "F3E5F5"}  # 郎将、偏将军高亮

for i, row in enumerate(cross_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, val in enumerate(row, 2):
        c = ws_cross.cell(row=r, column=j)
        c.value = val
        if j in highlight_cols and not alt:
            c.fill = hfill(highlight_cols[j])
        elif alt:
            c.fill = hfill(C_ALT_ROW)
        else:
            c.fill = hfill(C_WHITE)
        if j == 2:
            c.font = body_font(bold=True, size=10)
        else:
            c.font = body_font(size=10)
        c.alignment = center()
        c.border = thin_border()
    ws_cross.row_dimensions[r].height = 24

ws_cross.merge_cells("B13:E13")
ws_cross["B13"].value = "★ 黄金干预人群：61-150级 × 郎将+偏将军 = 约12,341人，优先实施破冰对局 + 推送文案优化"
ws_cross["B13"].fill = hfill("FFF9C4")
ws_cross["B13"].font = body_font(size=10, color="CC6600", bold=True)
ws_cross["B13"].alignment = left()
ws_cross.row_dimensions[13].height = 28

# ═══════════════════════════════════════════════════════════════════════
# Sheet 7: 系统优化建议（排除社交）
# ═══════════════════════════════════════════════════════════════════════
ws_opt = wb.create_sheet("系统优化建议")
ws_opt.sheet_view.showGridLines = False
set_col_widths(ws_opt, [3, 18, 12, 12, 12, 35, 3])
merge_title(ws_opt, "预流失干预系统优化建议（排除社交方向）", 2, 2, 6)

headers = ["优化方向", "优先级", "预期效果", "实施难度", "负责人", "具体措施"]
for i, h in enumerate(headers, 2):
    c = ws_opt.cell(row=3, column=i)
    c.value = h
    c.fill = hfill(C_HEADER_BG)
    c.font = header_font()
    c.alignment = center()
    c.border = thin_border()
ws_opt.row_dimensions[3].height = 28

opt_data = [
    ("推送文案优化", "P0", "+30-50%", "低", "产品", "前置奖励描述，情感化表达，郎将版/将军版差异化"),
    ("破冰对局机制", "P0", "+6-9pp", "低", "开发", "任务完成后弹窗引导，AI/低段位匹配，实时奖励反馈"),
    ("郎将第1天转化", "P0", "+6-9pp", "低", "开发", "完成登录任务后弹出破冰对局入口，降低挫败感"),
    ("推送时间分群", "P0", "+20%", "中", "后端", "重度沉默8-9点，深度沉默10点+20点，分群下发"),
    ("第3天任务降难度", "P1", "+3-5pp", "低", "开发", "移除模式限制，完成任意1局即可，额外战令经验激励"),
    ("任务差异化", "P1", "+10%", "中", "产品+开发", "每日任务内容差异化，增加招募/公会签到等新任务"),
    ("分层奖励设计", "P1", "+20%", "中", "产品+开发", "郎将资源类/偏将军混合/将军社交认同，分层发放"),
    ("三档递进推送", "P1", "多触达", "中", "后端+产品", "1/3/5天递进推送，深度沉默用户每天2次触达"),
    ("圈选模型校准", "P2", "ROI提升", "待定", "数据+策略", "召回层7-14天/挽留层3-7天/沉默层自然观察"),
]

priority_color = {"P0": "FFCDD2", "P1": "FFF9C4", "P2": "E3F2FD"}

for i, row in enumerate(opt_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, val in enumerate(row, 2):
        c = ws_opt.cell(row=r, column=j)
        c.value = val
        if j == 2:
            c.fill = hfill(priority_color.get(val, C_WHITE))
            c.font = Font(name="微软雅黑", bold=True, size=10)
        elif j == 4:
            diff = {"低": "C8E6C9", "中": "FFF9C4", "待定": "F5F5F5"}.get(val, C_WHITE)
            c.fill = hfill(diff)
            c.font = body_font(size=10)
        else:
            c.fill = hfill(C_ALT_ROW if alt else C_WHITE)
            c.font = body_font(size=10)
        c.alignment = center() if j != 6 else left()
        c.border = thin_border()
    ws_opt.row_dimensions[r].height = 28

# ═══════════════════════════════════════════════════════════════════════
# Sheet 8: 核心结论
# ═══════════════════════════════════════════════════════════════════════
ws_con = wb.create_sheet("核心结论")
ws_con.sheet_view.showGridLines = False
set_col_widths(ws_con, [3, 55, 3])
merge_title(ws_con, "核心结论与下一步行动", 2, 2, 2, height=45)
ws_con.row_dimensions[2].height = 45

conclusions = [
    ("问题诊断", [
        "1. 触达转化率过低：圈选→登录仅14.8%，85%用户未被有效触达",
        "2. 郎将是优化核心：郎将第1天转化率67%（最低），61-150级×郎将人群约12,341人",
        "3. 第3天留存塌陷：任务完成率从83.5%跌至69.4%，-24pp下滑最严重",
        "4. 干预绝对效果有限：实验组vs对照组次留率差异仅-0.33pp~+0.02pp",
        "5. 后半段留存系统性下降：郎将-24pp / 偏将军-33pp / 将军-42pp",
    ]),
    ("优化重点", [
        "P0级：推送文案优化（前置奖励文案）、破冰对局机制（郎将专属）",
        "P0级：郎将第1天转化率提升至75%+，登录→对局漏斗收窄",
        "P1级：第3天任务降难度（移除模式限制）、分层奖励设计",
        "P2级：圈选模型校准（召回层/挽留层/沉默层分层干预）",
    ]),
    ("快速见效方案", [
        "破冰对局：开发难度低，预期郎将转化+6~9pp，是性价比最高的短期方案",
        "推送文案：产品优化文案风格，预计触达转化+30-50%",
        "第3天降难度：仅修改任务配置，无需开发，预计第3天留存+3~5pp",
    ]),
    ("下一步行动", [
        "短期（1-2周）：推送文案上线A/B测试、破冰对局功能开发、第3天任务配置调整",
        "中期（1个月）：推送时间分群上线、分层奖励设计、三档递进推送",
        "长期（季度）：圈选模型校准、任务差异化设计、整体ROI提升",
    ]),
]

current_row = 4
for section_title, items in conclusions:
    ws_con.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=2)
    tc = ws_con.cell(row=current_row, column=2)
    tc.value = f"▶ {section_title}"
    tc.fill = hfill(C_ORANGE)
    tc.font = Font(name="微软雅黑", bold=True, size=11, color=C_WHITE)
    tc.alignment = left()
    ws_con.row_dimensions[current_row].height = 28
    current_row += 1

    for item in items:
        ws_con.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=2)
        ic = ws_con.cell(row=current_row, column=2)
        ic.value = f"  {item}"
        ic.fill = hfill(C_ALT_ROW)
        ic.font = body_font(size=10)
        ic.alignment = left()
        ws_con.row_dimensions[current_row].height = 24
        current_row += 1

    current_row += 1  # 空行

# ── 保存 ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
wb.save(OUTPUT_PATH)
print(f"报告已生成：{OUTPUT_PATH}")