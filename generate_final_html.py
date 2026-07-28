# -*- coding: utf-8 -*-
import json
import csv
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
all_general_data = []

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

    # 武将明细
    for g in generals_list:
        tier = g.get('tier', '普通')
        old_general = g.get('old_points', 0)
        new_general = tier_new_points.get(tier, 100)
        new_lamp = old_general + lamp_points - new_general
        system_need_per = round(system_need / count, 2) if count > 0 else 0

        all_general_data.append({
            'lamp': lamp,
            'name': g.get('name', ''),
            'tier': tier,
            'old_general': old_general,
            'lamp_points': lamp_points,
            'new_general': new_general,
            'new_lamp': new_lamp,
            'system_need_per': system_need_per,
        })

# 系统需补为正数的将灯
need补充 = [l for l in lamp_summary if l['system_need'] > 0]
total_need补充 = sum(l['system_need'] for l in need补充)

# 档位统计
tier_counts = {'普通': 0, '稀有': 0, '史诗': 0, '传说': 0, '限定': 0}
for g in generals:
    tier = g.get('tier', '普通')
    if tier in tier_counts:
        tier_counts[tier] += 1

# 生成HTML
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>武将品质体系PRD v5 - 帅点汇总</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; color: #eee; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #ffd700; text-align: center; font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
        h2 {{ color: #87ceeb; border-bottom: 2px solid #87ceeb; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ color: #ff6b6b; margin-top: 20px; }}
        .subtitle {{ text-align: center; color: #aaa; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; }}
        th, td {{ border: 1px solid #444; padding: 10px 12px; text-align: center; }}
        th {{ background: linear-gradient(180deg, #333 0%, #222 100%); color: #ffd700; font-weight: bold; }}
        tr:nth-child(even) {{ background: rgba(255,255,255,0.03); }}
        tr:hover {{ background: rgba(255,255,255,0.08); }}
        .positive {{ color: #ff6b6b; font-weight: bold; }}
        .negative {{ color: #4ecdc4; }}
        .zero {{ color: #888; }}
        .summary-box {{ background: linear-gradient(135deg, #2a2a4a 0%, #1a1a3e 100%); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
        .highlight-box {{ background: linear-gradient(135deg, #4a2a5a 0%, #3a1a4a 100%); padding: 20px; border-radius: 15px; margin: 20px 0; border: 2px solid #ffd700; box-shadow: 0 4px 15px rgba(255,215,0,0.2); }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #ffd700; }}
        .stat-label {{ color: #aaa; margin-top: 5px; }}
        .formula {{ background: #2a2a2a; padding: 15px; border-radius: 10px; font-family: 'Consolas', monospace; margin: 15px 0; }}
        .formula code {{ color: #ffd700; }}
        .tier-badge {{ display: inline-block; padding: 3px 10px; border-radius: 15px; font-size: 0.85em; }}
        .tier-普通 {{ background: #4a4a4a; }}
        .tier-稀有 {{ background: #4a6aaa; }}
        .tier-史诗 {{ background: #8a4aaa; }}
        .tier-传说 {{ background: #aa6a4a; }}
        .tier-限定 {{ background: #aa4a4a; }}
        .toc {{ background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .toc a {{ color: #87ceeb; text-decoration: none; display: block; padding: 5px 0; }}
        .toc a:hover {{ color: #ffd700; }}
        footer {{ text-align: center; margin-top: 50px; padding: 20px; color: #666; border-top: 1px solid #333; }}
        .page-break {{ page-break-after: always; }}
        @media print {{ body {{ background: white; color: black; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 武将品质体系 PRD v5</h1>
        <p class="subtitle">帅点汇总分析报告</p>

        <div class="toc">
            <h3 style="color: #ffd700; margin-top: 0;">📑 目录</h3>
            <a href="#summary">📊 总体帅点统计</a>
            <a href="#need-supplement">⚠️ 需要系统补充帅点的将灯</a>
            <a href="#all-lamps">📋 所有将灯帅点明细</a>
            <a href="#general-detail">👥 武将帅点明细表</a>
            <a href="#formula">📐 计算公式说明</a>
            <a href="#tier-info">🏷️ 档位帅点对照</a>
        </div>

        <div id="summary">
            <h2>📊 总体帅点统计</h2>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-value">{len(lamp_groups)}</div>
                    <div class="stat-label">将灯总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(generals)}</div>
                    <div class="stat-label">武将总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_old_points:,}</div>
                    <div class="stat-label">原武将帅点总和</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_new_points:,}</div>
                    <div class="stat-label">新武将帅点总和</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_lamp_points:,}</div>
                    <div class="stat-label">将灯帅点总和</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value {'positive' if total_need补充 > 0 else 'negative'}">{total_need补充:,.0f}</div>
                    <div class="stat-label">系统需补帅点（正数）</div>
                </div>
            </div>
        </div>

        <div id="need-supplement">
            <h2>⚠️ 需要系统补充帅点的将灯</h2>
            <div class="highlight-box">
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
    html += f'''
                    <tr>
                        <td>{l['lamp']}</td>
                        <td>{l['count']}</td>
                        <td>{l['old_sum']:,}</td>
                        <td>{l['new_sum']:,}</td>
                        <td>{l['lamp_points']:,}</td>
                        <td class="positive">{l['system_need']:,.0f}</td>
                    </tr>'''

html += f'''
                    <tr style="background: rgba(255,215,0,0.2); font-weight: bold;">
                        <td>合计</td>
                        <td>{sum(l['count'] for l in need补充)}</td>
                        <td>{sum(l['old_sum'] for l in need补充):,}</td>
                        <td>{sum(l['new_sum'] for l in need补充):,}</td>
                        <td>{sum(l['lamp_points'] for l in need补充):,}</td>
                        <td class="positive">{total_need补充:,.0f}</td>
                    </tr>
                </table>
            </div>
        </div>

        <div id="all-lamps">
            <h2>📋 所有将灯帅点明细</h2>
            <div class="summary-box">
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
    html += f'''
                    <tr>
                        <td>{l['lamp']}</td>
                        <td>{l['count']}</td>
                        <td>{l['old_sum']:,}</td>
                        <td>{l['new_sum']:,}</td>
                        <td>{l['lamp_points']:,}</td>
                        <td class="{css_class}">{l['system_need']:,.0f}</td>
                        <td>{status}</td>
                    </tr>'''

html += '''
                </table>
            </div>
        </div>

        <div id="general-detail">
            <h2>👥 武将帅点明细表</h2>
            <p style="color: #aaa;">（按将灯分组显示）</p>
'''

# 按将灯分组显示武将明细
for lamp_data in lamp_summary:
    lamp = lamp_data['lamp']
    lamp_generals = [g for g in all_general_data if g['lamp'] == lamp]

    system_need_total = lamp_data['system_need']

    html += f'''
            <h3>{lamp} <span style="color: #888; font-size: 0.7em;">({len(lamp_generals)}个武将 | 系统需补: {system_need_total:,.0f})</span></h3>
            <table>
                <tr>
                    <th>武将名</th>
                    <th>档位</th>
                    <th>武将原来帅点</th>
                    <th>将灯原来的帅点</th>
                    <th>武将新的帅点</th>
                    <th>将灯新的帅点</th>
                    <th>系统需要补充的帅点</th>
                </tr>'''

    for g in lamp_generals:
        lamp_new_class = "positive" if g['new_lamp'] < 0 else "negative" if g['new_lamp'] > 0 else "zero"
        need_class = "positive" if g['system_need_per'] > 0 else "negative" if g['system_need_per'] < 0 else "zero"
        html += f'''
                <tr>
                    <td>{g['name']}</td>
                    <td><span class="tier-badge tier-{g['tier']}">{g['tier']}</span></td>
                    <td>{g['old_general']}</td>
                    <td>{g['lamp_points']:,}</td>
                    <td>{g['new_general']}</td>
                    <td class="{lamp_new_class}">{g['new_lamp']:,.0f}</td>
                    <td class="{need_class}">{g['system_need_per']:,.2f}</td>
                </tr>'''

    html += '''
            </table>'''

html += '''
        </div>

        <div id="formula">
            <h2>📐 计算公式说明</h2>
            <div class="summary-box">
                <h3>核心公式</h3>
                <div class="formula">
                    <p><code>系统需补 = 新武将帅点总和 - (原武将帅点总和 + 真实将灯帅点)</code></p>
                </div>

                <h3>各字段说明</h3>
                <table>
                    <tr>
                        <th>字段</th>
                        <th>说明</th>
                    </tr>
                    <tr>
                        <td>新武将帅点总和</td>
                        <td>所有武将新帅点之和（根据档位：普通100/稀有150/史诗200/传说500/限定800）</td>
                    </tr>
                    <tr>
                        <td>原武将帅点总和</td>
                        <td>所有武将原帅点之和（来自sgs_general_conf表的Star字段）</td>
                    </tr>
                    <tr>
                        <td>真实将灯帅点</td>
                        <td>来自sgs_general_lamp_conf表的OfficialScore+NewOfficialScore</td>
                    </tr>
                    <tr>
                        <td>系统需补 > 0</td>
                        <td>表示系统需要额外产出帅点填补缺口</td>
                    </tr>
                    <tr>
                        <td>系统需补 < 0</td>
                        <td>表示将灯有盈余帅点</td>
                    </tr>
                </table>

                <h3>武将帅点计算</h3>
                <div class="formula">
                    <p><code>将灯新的帅点 = 武将原来帅点 + 将灯原来的帅点 - 武将新的帅点</code></p>
                </div>
            </div>
        </div>

        <div id="tier-info">
            <h2>🏷️ 档位帅点对照</h2>
            <div class="summary-box">
                <table>
                    <tr>
                        <th>档位</th>
                        <th>新帅点</th>
                        <th>武将数量</th>
                    </tr>'''

for tier, points in tier_new_points.items():
    html += f'''
                    <tr>
                        <td><span class="tier-badge tier-{tier}">{tier}</span></td>
                        <td>{points}</td>
                        <td>{tier_counts.get(tier, 0)}</td>
                    </tr>'''

html += '''
                </table>
            </div>
        </div>

        <footer>
            <p>武将品质体系 PRD v5 - 帅点汇总分析报告</p>
            <p style="color: #666;">生成日期：2026年6月12日</p>
        </footer>
    </div>
</body>
</html>'''

# 输出到文件
output_path = '武将评级划分/data/武将品质体系PRD_v5.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'HTML已生成: {output_path}')
print(f'将灯总数: {len(lamp_groups)}')
print(f'武将总数: {len(generals)}')
print(f'需要系统补的将灯数: {len(need补充)}')
print(f'系统需补总帅点: {total_need补充:,.0f}')