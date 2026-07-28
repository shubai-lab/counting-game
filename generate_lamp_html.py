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
    '普通': 100,
    '稀有': 150,
    '史诗': 200,
    '传说': 500,
    '限定': 800,
}

# 按将灯分组
lamp_groups = {}
for g in generals:
    lamp = g.get('lamp_type', '未知')
    if lamp not in lamp_groups:
        lamp_groups[lamp] = []
    lamp_groups[lamp].append(g)

# 计算每个将灯的系统需补
lamp_summary = []
total_system_need = 0
total_old_points = 0
total_new_points = 0
total_lamp_points = 0

for lamp in sorted(lamp_groups.keys(), key=lambda x: -len(lamp_groups[x])):
    generals_list = lamp_groups[lamp]
    lamp_points = lamp_points_config.get(lamp, 0)
    old_sum = sum(g.get('old_points', 0) for g in generals_list)
    new_sum = sum(tier_new_points.get(g.get('tier', '普通'), 100) for g in generals_list)
    count = len(generals_list)

    system_need = new_sum - (old_sum + lamp_points)

    total_system_need += system_need
    total_old_points += old_sum
    total_new_points += new_sum
    total_lamp_points += lamp_points

    lamp_summary.append({
        'lamp': lamp,
        'count': count,
        'old_sum': old_sum,
        'new_sum': new_sum,
        'lamp_points': lamp_points,
        'system_need': system_need,
    })

# 系统需补为正数的将灯
need补充 = [l for l in lamp_summary if l['system_need'] > 0]

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>武将品质体系PRD - 帅点汇总</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #ffd700; text-align: center; }}
        h2 {{ color: #87ceeb; border-bottom: 2px solid #87ceeb; padding-bottom: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #444; padding: 10px; text-align: center; }}
        th {{ background: #333; color: #ffd700; }}
        tr:nth-child(even) {{ background: #2a2a4a; }}
        tr:hover {{ background: #3a3a5a; }}
        .positive {{ color: #ff6b6b; font-weight: bold; }}
        .negative {{ color: #4ecdc4; }}
        .summary {{ background: #2a2a4a; padding: 15px; border-radius: 10px; margin: 20px 0; }}
        .highlight {{ background: #4a3a6a; padding: 15px; border-radius: 10px; margin: 20px 0; border: 2px solid #ffd700; }}
    </style>
</head>
<body>
    <h1>🔥 武将品质体系 PRD v5 - 帅点汇总</h1>

    <div class="summary">
        <h2>📊 总体帅点统计</h2>
        <table>
            <tr>
                <th>指标</th>
                <th>数值</th>
            </tr>
            <tr>
                <td>将灯总数</td>
                <td>{len(lamp_groups)}</td>
            </tr>
            <tr>
                <td>武将总数</td>
                <td>{len(generals)}</td>
            </tr>
            <tr>
                <td>原武将帅点总和</td>
                <td>{total_old_points:,}</td>
            </tr>
            <tr>
                <td>新武将帅点总和</td>
                <td>{total_new_points:,}</td>
            </tr>
            <tr>
                <td>将灯帅点总和</td>
                <td>{total_lamp_points:,}</td>
            </tr>
            <tr>
                <td>系统需补充总帅点</td>
                <td class="{'positive' if total_system_need > 0 else 'negative'}">{total_system_need:,}</td>
            </tr>
        </table>
    </div>

    <div class="highlight">
        <h2>⚠️ 需要系统补充帅点的将灯</h2>
        <table>
            <tr>
                <th>将灯名</th>
                <th>武将数</th>
                <th>原帅点总和</th>
                <th>新帅点总和</th>
                <th>将灯帅点</th>
                <th>系统需补</th>
            </tr>'''

for l in sorted(need补充, key=lambda x: -x['system_need']):
    html_content += f'''
            <tr>
                <td>{l['lamp']}</td>
                <td>{l['count']}</td>
                <td>{l['old_sum']:,}</td>
                <td>{l['new_sum']:,}</td>
                <td>{l['lamp_points']:,}</td>
                <td class="positive">{l['system_need']:,}</td>
            </tr>'''

total_need = sum(l['system_need'] for l in need补充)
html_content += f'''
            <tr style="background: #4a3a6a; font-weight: bold;">
                <td>合计</td>
                <td>{sum(l['count'] for l in need补充)}</td>
                <td>{sum(l['old_sum'] for l in need补充):,}</td>
                <td>{sum(l['new_sum'] for l in need补充):,}</td>
                <td>{sum(l['lamp_points'] for l in need补充):,}</td>
                <td class="positive">{total_need:,}</td>
            </tr>
        </table>
    </div>

    <h2>📋 所有将灯帅点明细</h2>
    <table>
        <tr>
            <th>将灯名</th>
            <th>武将数</th>
            <th>原帅点总和</th>
            <th>新帅点总和</th>
            <th>将灯帅点</th>
            <th>系统需补</th>
            <th>状态</th>
        </tr>'''

for l in lamp_summary:
    status = "⚠️ 需补" if l['system_need'] > 0 else "✅ 盈余"
    css_class = "positive" if l['system_need'] > 0 else "negative"
    html_content += f'''
        <tr>
            <td>{l['lamp']}</td>
            <td>{l['count']}</td>
            <td>{l['old_sum']:,}</td>
            <td>{l['new_sum']:,}</td>
            <td>{l['lamp_points']:,}</td>
            <td class="{css_class}">{l['system_need']:,}</td>
            <td>{status}</td>
        </tr>'''

html_content += '''
    </table>

    <h2>📐 计算公式说明</h2>
    <div class="summary">
        <p><strong>公式：系统需补 = 新武将帅点总和 - (原武将帅点总和 + 真实将灯帅点)</strong></p>
        <ul>
            <li><strong>新武将帅点总和</strong>：所有武将新帅点之和（根据档位：普通100/稀有150/史诗200/传说500/限定800）</li>
            <li><strong>原武将帅点总和</strong>：所有武将原帅点之和</li>
            <li><strong>真实将灯帅点</strong>：来自sgs_general_lamp_conf表的OfficialScore+NewOfficialScore</li>
            <li><strong>系统需补 > 0</strong>：表示系统需要额外产出帅点</li>
            <li><strong>系统需补 < 0</strong>：表示将灯有盈余帅点</li>
        </ul>
    </div>

    <h2>📈 档位帅点对照</h2>
    <table>
        <tr>
            <th>档位</th>
            <th>新帅点</th>
            <th>武将数量</th>
        </tr>'''

tier_counts = {'普通': 0, '稀有': 0, '史诗': 0, '传说': 0, '限定': 0}
for g in generals:
    tier = g.get('tier', '普通')
    if tier in tier_counts:
        tier_counts[tier] += 1

for tier, points in tier_new_points.items():
    html_content += f'''
        <tr>
            <td>{tier}</td>
            <td>{points}</td>
            <td>{tier_counts.get(tier, 0)}</td>
        </tr>'''

html_content += '''
    </table>

    <footer style="text-align: center; margin-top: 50px; color: #888;">
        <p>武将品质体系 PRD v5 - 帅点汇总分析</p>
    </footer>
</body>
</html>'''

# 输出到文件
output_path = '武将评级划分/data/武将品质体系PRD_v5.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'HTML已生成: {output_path}')
print(f'系统需补充总帅点: {total_system_need:,}')
print(f'需要系统补的将灯数: {len(need补充)}')
print(f'需要系统补的帅点总数: {total_need:,}')