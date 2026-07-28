# -*- coding: utf-8 -*-
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取分类结果
with open('武将评级划分/data/classification_final_v5_result.json', 'r', encoding='utf-8') as f:
    generals = json.load(f)

# 将灯帅点配置
lamp_points_config = {
    '主': 20, '虎': 10, '慧': 10, '香': 10, '骁': 15,
    '风': 20, '火': 20, '林': 20, '山': 100, '阴': 20, '雷': 20,
    '神': 1000, '神武': 2800, '武庙': 3100,
    '将1': 25, '将2': 25, '将3': 25, '将4': 25, '将5': 25,
    '天府': 20, '天梁': 20, '天机': 20, '天同': 20, '天相': 20, '七杀': 20,
    '祈福': 4200, '豆蔻梢头': 2300, '皇家贵胄': 2700, '笔舌如椽': 1850,
    '计将安出': 1200, '高山仰止': 9600, '百战虎贲': 2700, '奇人异士': 3200,
    '往者可谏': 350, '千里单骑': 300, '戚宦之争': 250, '黄巾之乱': 150,
    '章台春望': 600, '才子佳人': 1180, '纵横捭阖': 250, '芝兰玉树': 1550,
    '天下归心': 1150, '隐山之玉': 1900, '烽火连天': 300, '锦瑟良缘': 2900,
    '悬壶济世': 600, '乱武': 450, '食禄尽忠': 250,
    '逐鹿': 20, '上兵伐谋': 100, '无双上将': 50,
    '绕庭之鸦': 450, '诸侯伐董': 100, '徐州风云': 150, '兵临城下': 350,
    '中原狼烟': 100, '虓虎悲歌': 100,
    '匡鼎炎汉': 1150, '一将成名2022': 650, '太平甲子': 650, '异军突起': 650,
    '钟灵毓秀': 2500, '正音雅乐': 1250, '代汉涂高': 550, '江湖之远': 1050,
    '群雄伺动': 400, '玉衡': 450, '一将成名2023': 550,
    '天枢': 400, '谋定天下': 2200, '天璇': 450, '冢虎狼顾': 450,
    '开阳': 150, '子敬邀刀': 300, '毒士鸩计': 450, '周郎将计': 150,
    '瑶光': 450, '奇佐论胜': 400,
    '威震天下': 1300, '君威盖世': 1450, '王佐倡义': 250,
    '一将成名2025': 350, '幼麟绝战': 100, '伯言绽火': 250,
    '片羽威凤': 200, '凤雏溯攻': 350, '武侯定南': 20,
}

# 档位对应的新帅点
tier_new_points = {
    '普通': 100, '稀有': 150, '史诗': 200, '传说': 500, '限定': 800,
}

# 按将灯分组
lamp_groups = {}
for g in generals:
    lamp = g.get('lamp_type', '未知')
    if lamp not in lamp_groups:
        lamp_groups[lamp] = []
    lamp_groups[lamp].append(g)

# 计算帅点汇总
lamp_summary = []
total_old_points = 0
total_new_points = 0
total_lamp_points = 0
all_general_data = []

for lamp in sorted(lamp_groups.keys(), key=lambda x: -len(lamp_groups[x])):
    generals_list = lamp_groups[lamp]
    lamp_points = lamp_points_config.get(lamp, 0)
    old_sum = sum(g.get('old_points', 0) for g in generals_list)
    new_sum = sum(tier_new_points.get(g.get('tier', '普通'), 100) for g in generals_list)
    count = len(generals_list)
    system_need = new_sum - (old_sum + lamp_points)

    total_old_points += old_sum
    total_new_points += new_sum
    total_lamp_points += lamp_points

    lamp_summary.append({
        'lamp': lamp, 'count': count, 'old_sum': old_sum,
        'new_sum': new_sum, 'lamp_points': lamp_points, 'system_need': system_need,
    })

    for g in generals_list:
        tier = g.get('tier', '普通')
        old_general = g.get('old_points', 0)
        new_general = tier_new_points.get(tier, 100)
        new_lamp = old_general + lamp_points - new_general
        system_need_per = round(system_need / count, 2) if count > 0 else 0
        all_general_data.append({
            'lamp': lamp, 'name': g.get('name', ''), 'tier': tier,
            'old_general': old_general, 'lamp_points': lamp_points,
            'new_general': new_general, 'new_lamp': new_lamp,
            'system_need_per': system_need_per,
        })

need补充 = [l for l in lamp_summary if l['system_need'] > 0]
total_need补充 = sum(l['system_need'] for l in need补充)

# 档位统计
tier_counts = {'普通': 0, '稀有': 0, '史诗': 0, '传说': 0, '限定': 0}
for g in generals:
    tier = g.get('tier', '普通')
    if tier in tier_counts:
        tier_counts[tier] += 1

# 生成帅点汇总HTML章节
lamp_section = '''
        <div class="section">
            <h2 class="section-title">四、帅点汇总分析</h2>

            <h3 style="color:#667eea;">4.1 总体帅点统计</h3>
            <table>
                <thead><tr><th>指标</th><th class="text-center">数值</th></tr></thead>
                <tbody>
                    <tr><td>将灯总数</td><td class="text-center">''' + str(len(lamp_groups)) + '''</td></tr>
                    <tr><td>武将总数</td><td class="text-center">''' + str(len(generals)) + '''</td></tr>
                    <tr><td>原武将帅点总和</td><td class="text-center">''' + f'{total_old_points:,}' + '''</td></tr>
                    <tr><td>新武将帅点总和</td><td class="text-center">''' + f'{total_new_points:,}' + '''</td></tr>
                    <tr><td>将灯帅点总和</td><td class="text-center">''' + f'{total_lamp_points:,}' + '''</td></tr>
                    <tr style="background:#fffbe6"><td><strong>系统需补帅点（正数）</strong></td><td class="text-center"><strong style="color:#ff4d4f;">''' + f'{total_need补充:,.0f}' + '''</strong></td></tr>
                </tbody>
            </table>

            <h3 style="color:#ff4d4f;">4.2 需要系统补充帅点的将灯</h3>
            <table>
                <thead><tr><th>将灯名</th><th class="text-center">武将数</th><th class="text-center">原帅点总和</th><th class="text-center">新帅点总和</th><th class="text-center">将灯帅点</th><th class="text-center">系统需补</th></tr></thead>
                <tbody>'''

for l in sorted(need补充, key=lambda x: -x['system_need']):
    lamp_section += f'''
                    <tr style="background:#fff2f0">
                        <td>{l['lamp']}</td>
                        <td class="text-center">{l['count']}</td>
                        <td class="text-center">{l['old_sum']:,}</td>
                        <td class="text-center">{l['new_sum']:,}</td>
                        <td class="text-center">{l['lamp_points']:,}</td>
                        <td class="text-center" style="color:#ff4d4f;font-weight:bold;">{l['system_need']:,.0f}</td>
                    </tr>'''

lamp_section += f'''
                    <tr style="background:#fffbe6;font-weight:bold;">
                        <td>合计</td>
                        <td class="text-center">{sum(l['count'] for l in need补充)}</td>
                        <td class="text-center">{sum(l['old_sum'] for l in need补充):,}</td>
                        <td class="text-center">{sum(l['new_sum'] for l in need补充):,}</td>
                        <td class="text-center">{sum(l['lamp_points'] for l in need补充):,}</td>
                        <td class="text-center" style="color:#ff4d4f;font-weight:bold;">{total_need补充:,.0f}</td>
                    </tr>
                </tbody>
            </table>

            <h3 style="color:#667eea;">4.3 所有将灯帅点明细</h3>
            <table>
                <thead><tr><th>将灯名</th><th class="text-center">武将数</th><th class="text-center">原帅点总和</th><th class="text-center">新帅点总和</th><th class="text-center">将灯帅点</th><th class="text-center">系统需补</th><th class="text-center">状态</th></tr></thead>
                <tbody>'''

for l in lamp_summary:
    status = '<span class="tag tag-warning">需补</span>' if l['system_need'] > 0 else '<span class="tag tag-success">盈余</span>'
    lamp_section += f'''
                    <tr>
                        <td>{l['lamp']}</td>
                        <td class="text-center">{l['count']}</td>
                        <td class="text-center">{l['old_sum']:,}</td>
                        <td class="text-center">{l['new_sum']:,}</td>
                        <td class="text-center">{l['lamp_points']:,}</td>
                        <td class="text-center" style="color:{"#ff4d4f" if l['system_need'] > 0 else "#52c41a"};">{l['system_need']:,.0f}</td>
                        <td class="text-center">{status}</td>
                    </tr>'''

lamp_section += '''
                </tbody>
            </table>

            <h3 style="color:#667eea;">4.4 武将帅点明细表</h3>
            <p style="color:#666;font-size:13px;">（按将灯分组显示，包含帅点变化和系统需补数据）</p>
'''

# 按将灯分组显示武将明细
for lamp_data in sorted(need补充, key=lambda x: -x['system_need']):
    lamp = lamp_data['lamp']
    lamp_generals = [g for g in all_general_data if g['lamp'] == lamp]
    system_need_total = lamp_data['system_need']

    lamp_section += f'''
            <h4 style="color:#8c8c8c;margin-top:15px;">{lamp} <span style="font-size:0.85em;">({len(lamp_generals)}个武将 | 系统需补: {system_need_total:,.0f})</span></h4>
            <table>
                <thead><tr>
                    <th>武将名</th>
                    <th>档位</th>
                    <th>武将原来帅点</th>
                    <th>将灯原来的帅点</th>
                    <th>武将新的帅点</th>
                    <th>将灯新的帅点</th>
                    <th>系统需要补充的帅点</th>
                </tr></thead>
                <tbody>'''

    for g in lamp_generals:
        lamp_new_class = "style='color:#ff4d4f;'" if g['new_lamp'] < 0 else "style='color:#52c41a;'"
        need_class = "style='color:#ff4d4f;font-weight:bold;'" if g['system_need_per'] > 0 else "style='color:#52c41a;'"
        lamp_section += f'''
                    <tr>
                        <td>{g['name']}</td>
                        <td><span class="tag tag-{'danger' if g['tier']=='限定' else 'warning' if g['tier']=='传说' else 'primary' if g['tier']=='史诗' else 'success' if g['tier']=='稀有' else 'gray'}">{g['tier']}</span></td>
                        <td class="text-center">{g['old_general']}</td>
                        <td class="text-center">{g['lamp_points']:,}</td>
                        <td class="text-center">{g['new_general']}</td>
                        <td class="text-center" {lamp_new_class}>{g['new_lamp']:,.0f}</td>
                        <td class="text-center" {need_class}>{g['system_need_per']:,.2f}</td>
                    </tr>'''

    lamp_section += '''
                </tbody>
            </table>'''

lamp_section += '''
            <h3 style="color:#667eea;">4.5 计算公式说明</h3>
            <div style="background:#fafafa;padding:16px;border-radius:8px;margin:10px 0;">
                <p><strong>核心公式：</strong></p>
                <p style="font-family:Consolas;background:#f0f0f0;padding:10px;border-radius:4px;margin:8px 0;">系统需补 = 新武将帅点总和 - (原武将帅点总和 + 真实将灯帅点)</p>
                <p><strong>武将帅点计算：</strong></p>
                <p style="font-family:Consolas;background:#f0f0f0;padding:10px;border-radius:4px;margin:8px 0;">将灯新的帅点 = 武将原来帅点 + 将灯原来的帅点 - 武将新的帅点</p>
                <ul style="font-size:13px;color:#666;">
                    <li><strong>新武将帅点</strong>：根据档位（普通100/稀有150/史诗200/传说500/限定800）</li>
                    <li><strong>原武将帅点</strong>：来自sgs_general_conf表的Star字段</li>
                    <li><strong>真实将灯帅点</strong>：来自sgs_general_lamp_conf表的OfficialScore+NewOfficialScore</li>
                    <li><strong>系统需补 > 0</strong>：表示系统需要额外产出帅点填补缺口</li>
                    <li><strong>系统需补 < 0</strong>：表示将灯有盈余帅点</li>
                </ul>
            </div>

            <h3 style="color:#667eea;">4.6 档位帅点对照</h3>
            <table>
                <thead><tr><th>档位</th><th class="text-center">新帅点</th><th class="text-center">武将数量</th></tr></thead>
                <tbody>'''

for tier, points in tier_new_points.items():
    tag_class = 'danger' if tier=='限定' else 'warning' if tier=='传说' else 'primary' if tier=='史诗' else 'success' if tier=='稀有' else 'gray'
    lamp_section += f'''
                    <tr>
                        <td><span class="tag tag-{tag_class}">{tier}</span></td>
                        <td class="text-center">{points}</td>
                        <td class="text-center">{tier_counts.get(tier, 0)}</td>
                    </tr>'''

lamp_section += '''
                </tbody>
            </table>
        </div>
'''

# 读取v4的HTML内容，插入帅点汇总章节
with open('武将评级划分/data/武将品质体系PRD_v4.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 在footer之前插入帅点汇总章节
insert_pos = html_content.find('<div class="footer">')
if insert_pos > 0:
    new_html = html_content[:insert_pos] + lamp_section + html_content[insert_pos:]
else:
    new_html = html_content + lamp_section

# 更新标题和版本信息
new_html = new_html.replace('武将品质体系 PRD v4.0', '武将品质体系 PRD v5.0')
new_html = new_html.replace('v4.0', 'v5.0')
new_html = new_html.replace('<span class="tag tag-warning">修订中</span>', '<span class="tag tag-success">完成</span>')
new_html = new_html.replace('2026-06-12</span>', '2026-06-12 | 帅点汇总已添加</span>')
new_html = new_html.replace('武将品质体系 PRD v5.0', '武将品质体系 PRD v5.0')

# 保存
output_path = '武将评级划分/data/武将品质体系PRD_v5.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'合并后的HTML已生成: {output_path}')
print(f'将灯总数: {len(lamp_groups)}')
print(f'武将总数: {len(generals)}')
print(f'需要系统补的将灯数: {len(need补充)}')
print(f'系统需补总帅点: {total_need补充:,.0f}')