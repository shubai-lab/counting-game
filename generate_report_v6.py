# -*- coding: utf-8 -*-
"""
预流失干预现状总览 + 优化方向
生成 Excel 报告
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

OUTPUT_PATH = r"C:\Users\zhangfan\Downloads\拉活功能分析-预流失干预\预流失干预现状分析_v1.xlsx"

wb = openpyxl.Workbook()
wb.remove(wb.active)

# ── 颜色常量 ──────────────────────────────────────────────────────────
C_DARK     = "1A1A2E"
C_GOLD     = "D4AF37"
C_ORANGE   = "FF9800"
C_WHITE    = "FFFFFF"
C_HEADER   = "2D2D44"
C_ALT      = "F5F5F5"
C_GREEN    = "4CAF50"
C_RED      = "F44336"
C_LIGHT_O  = "FFF3E0"

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

# ════════════════════════════════════════════════════════════════════════
# Sheet 1: 总览封面
# ════════════════════════════════════════════════════════════════════════
ws = wb.create_sheet("总览")
ws.sheet_view.showGridLines = False
set_widths(ws, [3, 28, 20, 20, 20, 3])

merge_title(ws, "预流失干预现状分析报告", 3, 2, 5, sz=16, h=50)
ws.merge_cells("B5:E5")
ws["B5"].value = "分析日期：2026-04-29  |  数据来源：Metabase sgsnew_user_tag + sgsnew_task_his"
ws["B5"].font = bfont(10, color="666666")
ws["B5"].alignment = left()

merge_title(ws, "三组圈选规模（tag表）", 8, 2, 5, sz=12, h=32)
hdr(ws, 9, 2, 6, ["组别", "tag表用户", "漏斗累计圈选", "tag覆盖率"])

tag_data = [
    ("数据部实验组(dweek tag2=0)", "152,916", "341,530", "44.8%", "E3F2FD"),
    ("对照组(dweek tag2=1)",         "37,965",  "102,930", "36.9%", "FFF3E0"),
    ("算法实验组(cxb tag2=0)",       "43,905",   "61,372", "71.5%", "E8F5E9"),
]
for i, (name, tag_u, funnel_u, rate, bg) in enumerate(tag_data):
    r = i + 10
    for j, v in enumerate([name, tag_u, funnel_u, rate], 2):
        cell = ws.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        cell.font = bfont(10, bold=(j==2))
        cell.alignment = center()
        cell.border = thin_border()
    ws.row_dimensions[r].height = 24

merge_title(ws, "漏斗转化率（累计 2026-04-08~04-27）", 15, 2, 5, sz=12, h=32)
hdr(ws, 16, 2, 6, ["组别", "圈选", "登录", "登录率", "完成任务"])

funnel_data = [
    ("数据部实验组", "341,530", "41,356", "12.1%", "23,087", "E3F2FD"),
    ("对照组",       "102,930", "12,131", "11.8%", "—",       "FFF3E0"),
    ("算法实验组",    "61,372", "19,905", "32.4%", "6,805",   "E8F5E9"),
]
for i, row in enumerate(funnel_data):
    r = i + 17
    name, sel, log, lgr, task, bg = row
    for j, v in enumerate([name, sel, log, lgr, task], 2):
        cell = ws.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if j == 5 and v == "32.4%":
            cell.font = Font(name="微软雅黑", bold=True, size=11, color=C_GREEN)
        elif j == 2:
            cell.font = bfont(10, bold=True)
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws.row_dimensions[r].height = 24

# ════════════════════════════════════════════════════════════════════════
# Sheet 2: 算法实验组用户结构
# ════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("算法实验组用户结构")
ws2.sheet_view.showGridLines = False
set_widths(ws2, [3, 16, 14, 12, 22, 3])

merge_title(ws2, "算法实验组(cxb tag2=0)用户结构分析", 2, 2, 5, sz=13, h=40)

hdr(ws2, 3, 2, 6, ["维度", "算法实验组(cxb)", "数据部/对照组(dweek)", "差异"])

compare_rows = [
    ("总圈选人数",    "43,905",      "494,460(dweek)",   "cxb仅为dweek的8.9%"),
    ("登录转化率",    "32.4%",        "~12%",             "cxb高出20pp+"),
    ("151+级占比",    "5.1%(318人)", "62%(主力)",         "cxb高等级用户极少"),
    ("31-60级占比",   "51.3%(3,174人)", "~5%",            "cxb低等级用户为主"),
    ("校尉+郎将",     "4,615人(78%)", "偏将军为主",       "cxb官阶偏低"),
    ("将军及以上",    "781人(13%)",   "占比高",           "cxb高端官阶极少"),
]
row_bgs = ["E3F2FD","FFF3E0","E8F5E9","E3F2FD","FFF3E0","E8F5E9"]
for i, row in enumerate(compare_rows):
    r = i + 4
    bg = row_bgs[i]
    for j, v in enumerate(row, 2):
        cell = ws2.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        cell.font = bfont(10, bold=(j==2))
        cell.alignment = center() if j != 5 else left()
        cell.border = thin_border()
    ws2.row_dimensions[r].height = 26

ws2.merge_cells("B11:E11")
c = ws2.cell(11, 2)
c.value = "★ 结论：算法实验组用户结构与数据部完全不同——以低等级(31-60级)校尉/郎将为主，而非高等级偏将军。32.4%的登录率或因圈选逻辑差异（cxb圈的是近期活跃下降用户，本身更易触达）。"
c.fill = fill("FFF9C4")
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
c.alignment = left()
ws2.row_dimensions[11].height = 32

# ════════════════════════════════════════════════════════════════════════
# Sheet 3: 等级×次留率
# ════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("等级×次留率")
ws3.sheet_view.showGridLines = False
set_widths(ws3, [3, 16, 14, 12, 22, 3])

merge_title(ws3, "等级分布 × 次留率（修正版 SQL：task_day 追踪）", 2, 2, 5, sz=13, h=40)
hdr(ws3, 3, 2, 6, ["等级段", "用户数", "占比", "次留率", "特征"])

lv_data = [
    ("1-30级",      1576, 2.97, 18.27, "★ 低留存风险", "FFCDD2"),
    ("31-60级",     2869, 5.41, 30.36, "★ 低留存风险", "FFCDD2"),
    ("61-100级",    6734, 12.70, 35.58, "★ 可提升段",  "FFF9C4"),
    ("101-150级",   9649, 18.19, 40.79, "★ 核心干预段", "F3E5F5"),
    ("151级以上",   33227, 62.64, 49.99, "主力人群",      "E8F5E9"),
]
for i, (label, cnt, pct, ret, note, bg) in enumerate(lv_data):
    r = i + 4
    vals = [label, f"{cnt:,}", f"{pct:.2f}%", f"{ret:.2f}%", note]
    for j, v in enumerate(vals, 2):
        cell = ws3.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if v.startswith("★"):
            cell.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
        elif j == 2:
            cell.font = bfont(10, bold=True)
        elif j == 5:
            ret_val = float(v.rstrip('%'))
            cell.font = Font(name="微软雅黑", bold=True, size=10,
                             color=C_GREEN if ret_val >= 45 else (C_RED if ret_val < 35 else "333333"))
        else:
            cell.font = bfont(10)
        cell.alignment = center() if j != 5 else left()
        cell.border = thin_border()
    ws3.row_dimensions[r].height = 24

note_row(ws3, 10, 2, 5,
    "总用户数 53,055 | 次留率=task_day次日是否登录（task_day+1） | 数据范围：2026-02-07~03-04")

ws3.merge_cells("B11:E11")
c = ws3.cell(11, 2)
c.value = "★ 低等级用户(1-60级)次留率仅18-30%，是优化重点；151+级次留50%仍有提升空间"
c.fill = fill("FFCDD2")
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC0000")
c.alignment = left()
ws3.row_dimensions[11].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 4: 官阶×次留率
# ════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("官阶×次留率")
ws4.sheet_view.showGridLines = False
set_widths(ws4, [3, 16, 18, 14, 12, 14, 3])

merge_title(ws4, "官阶分布 × 次留率（修正版 SQL）", 2, 2, 6, sz=13, h=40)
hdr(ws4, 3, 2, 7, ["官阶", "帅点区间", "用户数", "占比", "次留率", "优先级"])

rk_data = [
    ("国护军",   "80000~129999",  1424, 2.68, 19.52, "★★★ 需紧急干预", "FFCDD2"),
    ("骁卒",     "< 4000",         4447, 8.38, 35.96, "★★★ 高优先级",    "FFCDD2"),
    ("校尉",     "4000~7999",      2326, 4.38, 30.14, "★★★ 高优先级",    "FFCDD2"),
    ("郎将",     "8000~11999",     5337,10.06, 52.35, "★★ 可提升",       "FFF9C4"),
    ("偏将军",   "12000~39999",   23034,43.41, 43.64, "★★★★★ 最大人群","F3E5F5"),
    ("将军",     "40000~59999",    9240,17.41, 47.86, "★★",              "E8F5E9"),
    ("上将军",   "60000~79999",    4886, 9.21, 49.59, "★★",              "E8F5E9"),
    ("国都护",   "130000~159999",  1412, 2.66, 54.75, "★ 留存较好",       "E3F2FD"),
    ("卫将军",   "160000~199999",  1020, 1.92, 51.27, "★",               "E3F2FD"),
    ("车骑将军", "200000~249999",   525, 0.99, 56.57, "★ 留存较好",       "E3F2FD"),
    ("骠骑将军", "250000~349999",   256, 0.48, 55.47, "★",               "E3F2FD"),
    ("大将军",   "≥ 350000",         57, 0.11, 61.40, "★ 最高留存",       "E3F2FD"),
]

for i, row in enumerate(rk_data):
    r = i + 4
    label, srange, cnt, pct, ret, pri, bg = row
    vals = [label, srange, f"{cnt:,}", f"{pct:.2f}%", f"{ret:.2f}%", pri]
    for j, v in enumerate(vals, 2):
        cell = ws4.cell(r, j)
        cell.value = v
        cell.fill = fill(bg)
        if j == 7:
            cell.font = Font(name="微软雅黑", bold=True, size=10, color="CC0000")
        elif j == 2:
            cell.font = bfont(10, bold=True)
        elif j == 5:
            ret_val = float(v.rstrip('%'))
            cell.font = Font(name="微软雅黑", bold=True, size=10,
                             color=C_GREEN if ret_val >= 50 else (C_RED if ret_val < 40 else "333333"))
        else:
            cell.font = bfont(10)
        cell.alignment = center()
        cell.border = thin_border()
    ws4.row_dimensions[r].height = 24

note_row(ws4, 17, 2, 6,
    "总用户数 53,064 | 次留率=task_day次日是否登录 | 官阶取≤task_day最近logout")

ws4.merge_cells("B18:F18")
c = ws4.cell(18, 2)
c.value = "★ 低留存官阶：国护军19.52% / 校尉30.14% / 骁卒35.96%，合计8,197人(15.4%)需专项干预 | 偏将军23,034人(43.4%)优化空间最大"
c.fill = fill("FFF9C4")
c.font = Font(name="微软雅黑", bold=True, size=10, color="CC6600")
c.alignment = left()
ws4.row_dimensions[18].height = 26

# ════════════════════════════════════════════════════════════════════════
# Sheet 5: 优化方向
# ════════════════════════════════════════════════════════════════════════
ws5 = wb.create_sheet("优化方向")
ws5.sheet_view.showGridLines = False
set_widths(ws5, [3, 18, 10, 14, 12, 32, 3])

merge_title(ws5, "预流失干预优化方向（按优先级）", 2, 2, 6, sz=13, h=40)
hdr(ws5, 3, 2, 7, ["优化方向", "优先级", "涉及人数", "预期效果", "实施难度", "具体措施"])

opt_data = [
    ("国护军专项干预（次留19.52%）", "P0", "~1,424人", "+10-15pp", "中",
     "国护军次留率仅19.52%，是最低官阶组。需分析：是任务未完成还是完成但未留存？制定专属召回策略（前置奖励+任务降门槛）。"),
    ("低留存官阶定向干预（骁卒/校尉/国护军）", "P0", "~8,197人", "+8-12pp", "低",
     "骁卒(35.96%)、校尉(30.14%)、国护军(19.52%)次留率偏低。专属召回文案+移除模式限制+额外登录奖励（元宝×20/帅点×50）。"),
    ("偏将军23,034人优化（次留43.64%，优化空间~30pp）", "P1", "~23,034人", "+10-20pp", "中",
     "偏将军是最大干预人群。优化破冰对局机制+分层奖励设计（资源类奖励：元宝×50/帅点×100），重点关注61-100级×偏将军组合。"),
    ("郎将5,337人破冰对局落地", "P1", "~5,337人", "+5-8pp", "中",
     "郎将次留52.35%，专属破冰对局入口（任务完成后弹出AI对局+即时奖励）尚未实现，PRD方案尽快落地。"),
    ("第3天任务降难度", "P1", "全部用户", "+3-5pp", "低",
     "三个官阶任务内容完全相同。第3天移除模式限制，完成任意1局即可，额外发放战令经验×500激励。"),
    ("算法实验组用户结构分析", "P1", "~43,905人", "数据质量", "中",
     "为什么cxb圈到大量31-60级校尉/郎将？是否符合预期？需与算法团队对齐，确认圈选逻辑是否需要调整。"),
    ("对照组任务数据修复", "P0", "~37,965人", "数据完整", "低",
     "对照组task_done全为0，数据链路疑似断裂。需排查sgsnew_task_his是否关联了对应taskid。"),
    ("圈选模型分层校准", "P2", "全部用户", "ROI提升", "高",
     "召回层7-14天/挽留层3-7天/沉默层1-3天，低质量用户降低干预频次。与数据确认最优阈值。"),
]

pri_bg = {"P0":"FFCDD2","P1":"FFF9C4","P2":"E3F2FD"}
diff_bg = {"低":"C8E6C9","中":"FFF9C4","高":"FFCDD2"}

for i, row in enumerate(opt_data):
    r = i + 4
    alt = (i % 2 == 1)
    for j, v in enumerate(row, 2):
        cell = ws5.cell(r, j)
        cell.value = v
        if j == 2:
            cell.fill = fill(pri_bg.get(v, C_WHITE))
            cell.font = Font(name="微软雅黑", bold=True, size=10)
        elif j == 4:
            cell.fill = fill(diff_bg.get(v, C_WHITE))
            cell.font = bfont(10)
        else:
            cell.fill = fill(C_ALT if alt else C_WHITE)
            cell.font = bfont(10)
        cell.alignment = center() if j not in [2, 6] else (left() if j == 6 else center())
        cell.border = thin_border()
    ws5.row_dimensions[r].height = 36

# ════════════════════════════════════════════════════════════════════════
# Sheet 6: 核心结论
# ════════════════════════════════════════════════════════════════════════
ws6 = wb.create_sheet("核心结论")
ws6.sheet_view.showGridLines = False
set_widths(ws6, [3, 62, 3])
merge_title(ws6, "核心结论与下一步行动", 2, 2, 2, sz=14, h=48)
ws6.row_dimensions[2].height = 48

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

sections = [
    ("问题诊断", [
        "1. 国护军次留率仅19.52%，是所有官阶中最低的，合计1,424人需紧急专项干预",
        "2. 骁卒+校尉+国护军合计8,197人(15.4%)次留率低于36%，低留存官阶问题突出",
        "3. 算法实验组用户结构与数据部完全不同：以低等级(31-60级)为主，而非151+级",
        "4. 算法实验组登录率32.4%是其他组2.7倍，或因cxb圈选逻辑（近期活跃下降用户）差异",
        "5. 对照组task_done全为0，数据链路疑似断裂",
    ]),
    ("关键数据", [
        "数据部实验组：圈选341,530 / 登录41,356(12.1%) / 完成任务23,087(55.8%) / 次留40.3%",
        "算法实验组：圈选61,372 / 登录19,905(32.4%) / 完成任务6,805(34.2%) / 次留39.1%",
        "等级分布：151+级33,227人(62.6%)为主力，次留49.99%；1-30级1,576人(3%)次留仅18.27%",
        "官阶分布：偏将军23,034人(43.4%)最多，次留43.64%；国护军1,424人(2.7%)次留19.52%",
        "算法实验组用户等级集中在31-60级(51.3%)，与数据部/对照组结构差异巨大",
    ]),
    ("优化优先级", [
        "P0：国护军专项干预（1,424人/次留19.52%）——分析原因+专属召回方案",
        "P0：低留存官阶定向干预（骁卒/校尉/国护军合计8,197人）——召回文案+任务降门槛",
        "P0：修复对照组任务数据链路（task_done=0根因排查）",
        "P1：偏将军23,034人优化（次留43.64%，提升空间~30pp）——破冰对局+分层奖励",
        "P1：算法实验组结构分析（为什么cxb圈到大量31-60级？是否需要调整圈选逻辑）",
    ]),
    ("下一步行动", [
        "立即（1-2天）：分析国护军次留19.52%的原因（任务未完成 vs 完成但未留存）",
        "本周：输出骁卒/校尉/国护军专项召回方案（专属文案+任务降门槛评审）",
        "短期（1-2周）：与算法团队对齐cxb圈选逻辑，确认31-60级为主是否符合预期",
        "中期（1个月）：偏将军23,034人破冰对局+分层奖励落地；任务差异化PRD确认",
    ]),
]

r_cur = 4
for title, items in sections:
    section_head(ws6, r_cur, 2, 2, title)
    r_cur += 1
    for item in items:
        item_row(ws6, r_cur, 2, 2, item)
        r_cur += 1
    r_cur += 1

# ── 保存 ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
wb.save(OUTPUT_PATH)
print(f"报告已生成：{OUTPUT_PATH}")
print(f"共 {len(wb.sheetnames)} 个Sheet：{wb.sheetnames}")