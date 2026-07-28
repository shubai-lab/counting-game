# -*- coding: utf-8 -*-
"""三组等级分布 + 官阶分布对比 → 更新到预流失干预现状分析_v1"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

OUTPUT_PATH = r"C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预\预流失干预现状分析_v1.xlsx"

wb = openpyxl.load_workbook(OUTPUT_PATH)

C_DARK="1A1A2E"; C_GOLD="D4AF37"; C_ORANGE="FF9800"; C_WHITE="FFFFFF"
C_HEADER="2D2D44"; C_ALT="F5F5F5"; C_GREEN="4CAF50"; C_RED="F44336"

def fill(h): return PatternFill("solid", fgColor=h)
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
    c.value = text; c.fill = fill(C_DARK)
    c.font = Font(name="微软雅黑", bold=True, size=sz, color=C_GOLD)
    c.alignment = center()
    ws.row_dimensions[row].height = h

def hdr(ws, row, c1, c2, texts, bg=C_HEADER):
    for i, t in enumerate(texts):
        cell = ws.cell(row=row, column=c1+i)
        cell.value = t; cell.fill = fill(bg)
        cell.font = Font(name="微软雅黑", bold=True, size=10, color=C_WHITE)
        cell.alignment = center(); cell.border = thin_border()
    ws.row_dimensions[row].height = 26

def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

# ── 原始数据（等级1.xlsx 解析）────────────────────────────────────────
# 等级分布
level_data = [
    ("1-30级",      6279,  1452, 11528),
    ("31-60级",     7850,  1875, 12982),
    ("61-100级",    9543,  2196,  8887),
    ("101-150级",   5818,  1385,  4576),
    ("151级以上",  16796,  3981,  5929),
]
# 官阶分布
rank_data = [
    ("骁卒",      7452,  1710, 14654),
    ("校尉",      6386,  1476, 10361),
    ("郎将",      7727,  1796,  7607),
    ("偏将军",   12472,  2942,  8570),
    ("将军",       3882,   935,  1466),
    ("上将军",    2448,   588,   523),
    ("国都护",    3360,   796,   529),
    ("卫将军",    1050,   256,   107),
    ("车骑将军",   744,   193,    51),
    ("骠骑将军",   444,   107,    26),
    ("大将军",     256,    77,     8),
    ("国护军",      65,    13,     0),
]

# ── 删除旧 sheet，重新创建 ──────────────────────────────────────────
for sn in ["三组等级分布", "三组官阶分布"]:
    if sn in wb.sheetnames:
        del wb[sn]

# ════════════════════════════════════════════════════════════════════════
# 三组等级分布
# ════════════════════════════════════════════════════════════════════════
ws_lv = wb.create_sheet("三组等级分布")
ws_lv.sheet_view.showGridLines = False
set_widths(ws_lv, [3, 16, 14, 12, 14, 12, 14, 12, 3])

merge_title(ws_lv, "三组圈选用户等级分布对比（tag data_day±7天匹配logout表）", 2, 2, 8, sz=13, h=40)
hdr(ws_lv, 3, 2, 9, ["等级段", "数据部实验组", "占比", "对照组", "占比", "算法实验组", "占比", "合计"])

lv_total = [sum(r[i] for r in level_data) for i in range(1, 4)]
lv_bgs = ["FFCDD2","FFCDD2","FFF9C4","E8F5E9","E8F5E9"]
for i, (label, dw, ct, cx) in enumerate(level_data):
    r = i + 4
    row_total = dw + ct + cx
    bg = lv_bgs[i]
    vals = [label, f"{dw:,}", f"{dw/lv_total[0]*100:.1f}%",
            f"{ct:,}", f"{ct/lv_total[1]*100:.1f}%",
            f"{cx:,}", f"{cx/lv_total[2]*100:.1f}%", f"{row_total:,}"]
    for j, v in enumerate(vals, 2):
        cell = ws_lv.cell(r, j)
        cell.value = v; cell.fill = fill(bg)
        cell.font = bfont(10, bold=(j==2))
        cell.alignment = center(); cell.border = thin_border()
    ws_lv.row_dimensions[r].height = 24

# 合计行
r = 9
total_all = sum(dw+ct+cx for dw,ct,cx in [(r[1],r[2],r[3]) for r in level_data])
vals = ["合计", f"{lv_total[0]:,}", "100%", f"{lv_total[1]:,}", "100%", f"{lv_total[2]:,}", "100%", f"{lv_total[0]+lv_total[1]+lv_total[2]:,}"]
for j, v in enumerate(vals, 2):
    cell = ws_lv.cell(r, j)
    cell.value = v; cell.fill = fill(C_HEADER)
    cell.font = Font(name="微软雅黑", bold=True, size=10, color=C_WHITE)
    cell.alignment = center(); cell.border = thin_border()
ws_lv.row_dimensions[r].height = 26

ws_lv.merge_cells("B11:H11")
c = ws_lv.cell(11, 2)
c.value = f"★ 匹配率：数据部 {lv_total[0]:,}人 / 对照组 {lv_total[1]:,}人 / 算法实验组 {lv_total[2]:,}人（tag data_day±7天范围内有logout记录的用户）"
c.fill = fill("FFF9C4"); c.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
c.alignment = left(); ws_lv.row_dimensions[11].height = 28

# ════════════════════════════════════════════════════════════════════════
# 三组官阶分布
# ════════════════════════════════════════════════════════════════════════
ws_rk = wb.create_sheet("三组官阶分布")
ws_rk.sheet_view.showGridLines = False
set_widths(ws_rk, [3, 16, 14, 12, 14, 12, 14, 12, 3])

merge_title(ws_rk, "三组圈选用户官阶分布对比（tag data_day±7天匹配logout表）", 2, 2, 8, sz=13, h=40)
hdr(ws_rk, 3, 2, 9, ["官阶", "数据部实验组", "占比", "对照组", "占比", "算法实验组", "占比", "合计"])

rk_total = [sum(r[i] for r in rank_data) for i in range(1, 4)]
rk_bgs = ["FFCDD2","FFCDD2","FFF9C4","FFF9C4","E8F5E9","E8F5E9","E8F5E9","E3F2FD","E3F2FD","E3F2FD","E3F2FD","E3F2FD"]
for i, (label, dw, ct, cx) in enumerate(rank_data):
    r = i + 4
    row_total = dw + ct + cx
    bg = rk_bgs[i]
    vals = [label, f"{dw:,}", f"{dw/rk_total[0]*100:.1f}%",
            f"{ct:,}", f"{ct/rk_total[1]*100:.1f}%",
            f"{cx:,}", f"{cx/rk_total[2]*100:.1f}%", f"{row_total:,}"]
    for j, v in enumerate(vals, 2):
        cell = ws_rk.cell(r, j)
        cell.value = v; cell.fill = fill(bg)
        cell.font = bfont(10, bold=(j==2))
        cell.alignment = center(); cell.border = thin_border()
    ws_rk.row_dimensions[r].height = 24

# 合计行
r = 16
for j, v in enumerate(["合计", f"{rk_total[0]:,}", "100%", f"{rk_total[1]:,}", "100%", f"{rk_total[2]:,}", "100%", f"{rk_total[0]+rk_total[1]+rk_total[2]:,}"], 2):
    cell = ws_rk.cell(r, j)
    cell.value = v; cell.fill = fill(C_HEADER)
    cell.font = Font(name="微软雅黑", bold=True, size=10, color=C_WHITE)
    cell.alignment = center(); cell.border = thin_border()
ws_rk.row_dimensions[r].height = 26

# 结论
ws_rk.merge_cells("B18:H18")
c = ws_rk.cell(18, 2)
c.value = "★ 算法实验组骁卒+校尉+郎将合计32,622人(79%)，远高于数据部21,565人(49%)。cxb圈选的确实是低官阶玩家为主"
c.fill = fill("FFF9C4"); c.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
c.alignment = left(); ws_rk.row_dimensions[18].height = 28

wb.save(OUTPUT_PATH)
print(f"已更新：{OUTPUT_PATH}")
print(f"共 {len(wb.sheetnames)} 个Sheet：{wb.sheetnames}")
