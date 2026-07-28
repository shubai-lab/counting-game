# -*- coding: utf-8 -*-
"""
生成武将品质划分依据Excel模板
- Sheet1: 划分规则说明
- Sheet2: 武将名单（可手动输入划分依据）
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def create_excel():
    wb = openpyxl.Workbook()

    # ===== Sheet1: 划分规则说明 =====
    ws_rules = wb.active
    ws_rules.title = "划分规则说明"

    # 样式
    header_fill = PatternFill(start_color="667eea", end_color="667eea", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    tier_colors = {
        "限定": "FF4D4F",
        "传说": "FAAD14",
        "史诗": "667EEA",
        "稀有": "52C41A",
        "普通": "8C8C8C"
    }

    # 标题
    ws_rules.merge_cells('A1:D1')
    ws_rules['A1'] = "武将品质体系 - 划分规则说明 v5.0"
    ws_rules['A1'].font = Font(bold=True, size=16, color="667eea")
    ws_rules['A1'].alignment = Alignment(horizontal='center')

    # 规则表头
    headers = ["品质", "获取途径", "评级规则", "珍宝价格区间"]
    for col, header in enumerate(headers, 1):
        cell = ws_rules.cell(row=3, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # 划分规则数据
    rules = [
        ("限定", "武庙/高山仰止", "武庙珍藏/高山仰止系列（固定限定档）", ">200,000"),
        ("限定", "珍宝价格", "珍宝价格 > 200,000", ">200,000"),
        ("传说", "祈福", "祈福(1004)（固定传说档）", "150,000~200,000"),
        ("传说", "将星招募", "将星价格 >= 10,000", "150,000~200,000"),
        ("传说", "珍宝价格", "珍宝价格 > 150,000 且 <= 200,000", "150,000~200,000"),
        ("史诗", "纳贤", "纳贤(1001)（固定史诗档）", "100,000~150,000"),
        ("史诗", "神将任务", "神将任务(5002)（固定史诗档）", "100,000~150,000"),
        ("史诗", "首充/充值奖励", "首充(2000)/充值奖励(2002/2003/3001/1005)", "100,000~150,000"),
        ("史诗", "将星招募", "将星价格 2,000~9,999", "100,000~150,000"),
        ("史诗", "宝玉兑换(1101)", "宝玉兑换，查道具定价表珍宝价格 > 100,000 且 <= 150,000", "100,000~150,000"),
        ("史诗", "珍宝(1003)", "珍宝兑换，查道具定价表珍宝价格 > 100,000 且 <= 150,000", "100,000~150,000"),
        ("史诗", "活动投放", "部分活动增加的目标性武将", "100,000~150,000"),
        ("稀有", "将星招募", "将星价格 100~1,999", "1,000~100,000"),
        ("稀有", "宝玉兑换(1101)", "宝玉兑换，查道具定价表珍宝价格 > 1,000 且 <= 100,000", "1,000~100,000"),
        ("稀有", "珍宝(1003)", "珍宝兑换，查道具定价表珍宝价格 > 1,000 且 <= 100,000", "1,000~100,000"),
        ("稀有", "界限突破", "界限突破系列武将", "1,000~100,000"),
        ("稀有", "活动赠送", "大部分活动赠送武将", "1,000~100,000"),
        ("普通", "将星招募", "将星价格 >0 且 <100", "免费/极低"),
        ("普通", "普通招募", "包含普通招募途径(1)", "免费/极低"),
    ]

    for row_idx, rule in enumerate(rules, 4):
        tier = rule[0]
        tier_fill = PatternFill(start_color=tier_colors.get(tier, "FFFFFF"),
                               end_color=tier_colors.get(tier, "FFFFFF"),
                               fill_type="solid")
        tier_font = Font(color="FFFFFF", bold=True)

        for col, value in enumerate(rule, 1):
            cell = ws_rules.cell(row=row_idx, column=col, value=value)
            if col == 1:
                cell.fill = tier_fill
                cell.font = tier_font
                cell.alignment = Alignment(horizontal='center')
            else:
                cell.alignment = Alignment(wrap_text=True)

    # 设置列宽
    ws_rules.column_dimensions['A'].width = 12
    ws_rules.column_dimensions['B'].width = 18
    ws_rules.column_dimensions['C'].width = 50
    ws_rules.column_dimensions['D'].width = 18

    # ===== Sheet2: 武将名单 =====
    ws_data = wb.create_sheet("武将名单")

    # 标题
    ws_data.merge_cells('A1:G1')
    ws_data['A1'] = "武将品质划分表（可手动输入划分依据）"
    ws_data['A1'].font = Font(bold=True, size=16, color="667eea")
    ws_data['A1'].alignment = Alignment(horizontal='center')

    # 说明
    ws_data['A2'] = "说明："
    ws_data['A2'].font = Font(bold=True)
    ws_data['B2'] = "手动确认列：填写具体划分依据（如：纳贤价格、将星价格、LampType等）"
    ws_data.merge_cells('B2:G2')

    # 表头
    data_headers = ["武将ID", "武将名称", "品质", "帅点", "原划分依据", "手动确认划分依据", "备注"]
    for col, header in enumerate(data_headers, 1):
        cell = ws_data.cell(row=4, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # 下拉列表 - 品质选择
    tier_dv = DataValidation(type="list", formula1='"限定,传说,史诗,稀有,普通"', allow_blank=True)
    tier_dv.error = "请选择：限定,传说,史诗,稀有,普通"
    tier_dv.errorTitle = "无效品质"
    ws_data.add_data_validation(tier_dv)

    # 从HTML中读取武将数据
    generals = []
    try:
        with open("武将品质体系PRD_v5.html", "r", encoding="utf-8") as f:
            content = f.read()

        import re
        # 解析武将行
        pattern = r'<tr class="general-row"><td>(\d+)</td><td>([^<]+)</td><td><span class="tag [^"]+">([^<]+)</span></td><td[^>]*>(\d+)</td><td>([^<]+)</td></tr>'
        matches = re.findall(pattern, content)

        for match in matches:
            generals.append({
                "id": match[0],
                "name": match[1],
                "tier": match[2],
                "points": match[3],
                "reason": match[4]
            })
    except Exception as e:
        print(f"读取HTML失败: {e}")
        # 使用示例数据
        generals = [
            {"id": "230", "name": "武诸葛亮", "tier": "限定", "points": "500", "reason": "LampType:武庙/高山仰止"},
            {"id": "500", "name": "关索", "tier": "传说", "points": "500", "reason": "将星价格:9999"},
        ]

    # 写入武将数据
    for row_idx, g in enumerate(generals, 5):
        # 武将ID
        ws_data.cell(row=row_idx, column=1, value=int(g["id"]))
        # 武将名称
        ws_data.cell(row=row_idx, column=2, value=g["name"])
        # 品质（带下拉）
        tier_cell = ws_data.cell(row=row_idx, column=3, value=g["tier"])
        tier_dv.add(tier_cell)
        # 根据品质设置颜色
        if g["tier"] in tier_colors:
            tier_cell.fill = PatternFill(start_color=tier_colors[g["tier"]],
                                        end_color=tier_colors[g["tier"]],
                                        fill_type="solid")
            tier_cell.font = Font(color="FFFFFF", bold=True)
        # 帅点
        ws_data.cell(row=row_idx, column=4, value=int(g["points"]))
        # 原划分依据
        ws_data.cell(row=row_idx, column=5, value=g["reason"])
        # 手动确认划分依据（空，供用户填写）
        manual_cell = ws_data.cell(row=row_idx, column=6, value="")
        manual_cell.fill = PatternFill(start_color="FFFDE7", end_color="FFFDE7", fill_type="solid")
        # 备注
        ws_data.cell(row=row_idx, column=7, value="")

    # 设置列宽
    ws_data.column_dimensions['A'].width = 10
    ws_data.column_dimensions['B'].width = 20
    ws_data.column_dimensions['C'].width = 12
    ws_data.column_dimensions['D'].width = 8
    ws_data.column_dimensions['E'].width = 30
    ws_data.column_dimensions['F'].width = 30
    ws_data.column_dimensions['G'].width = 15

    # 冻结首行
    ws_data.freeze_panes = 'A5'

    # 添加统计行
    last_row = len(generals) + 6
    ws_data.cell(row=last_row, column=1, value="统计：")
    ws_data.cell(row=last_row, column=1).font = Font(bold=True)

    tier_count = {}
    for g in generals:
        tier_count[g["tier"]] = tier_count.get(g["tier"], 0) + 1

    col = 2
    for tier in ["限定", "传说", "史诗", "稀有", "普通"]:
        count = tier_count.get(tier, 0)
        ws_data.cell(row=last_row, column=col, value=f"{tier}: {count}个")
        col += 1

    # 保存
    output_path = "武将品质划分_手动输入版.xlsx"
    wb.save(output_path)
    print(f"Excel已生成: {output_path}")
    print(f"共 {len(generals)} 个武将")

    return output_path

if __name__ == "__main__":
    create_excel()