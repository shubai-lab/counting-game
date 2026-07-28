# -*- coding: utf-8 -*-
import json
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取Star帅点
df = pd.read_excel('武将评级划分/data/sgs_general_conf.xlsx', header=None, skiprows=4)
df_star = df[[0, 25]].copy()
df_star.columns = ['GeneralID', 'Star']
df_star['GeneralID'] = pd.to_numeric(df_star['GeneralID'], errors='coerce')
df_star['Star'] = pd.to_numeric(df_star['Star'], errors='coerce')
df_star = df_star.dropna()

star_to_points = {1: 80, 2: 100, 3: 120, 4: 500}
df_star['帅点'] = df_star['Star'].map(star_to_points)

# 读取当前分类
with open('武将评级划分/data/classification_final_v4_result.json', 'r', encoding='utf-8') as f:
    generals = json.load(f)

# 合并帅点数据
id_to_points = dict(zip(df_star['GeneralID'].astype(int), df_star['帅点'].astype(int)))
for g in generals:
    g['old_points'] = id_to_points.get(g['general_id'])

# 统计1: 原帅点 -> 当前品质
pts_to_tiers = {}
for pts in [500, 120, 100, 80]:
    gens = [g for g in generals if g.get('old_points') == pts]
    tiers = {}
    for g in gens:
        t = g['tier']
        tiers[t] = tiers.get(t, 0) + 1
    pts_to_tiers[pts] = tiers

# 统计2: 当前品质 -> 原帅点
tier_to_pts = {}
tiers_order = ['限定', '传说', '史诗', '稀有', '普通']
for tier in tiers_order:
    gens = [g for g in generals if g['tier'] == tier]
    pts_dist = {}
    for g in gens:
        p = g.get('old_points', '-')
        pts_dist[p] = pts_dist.get(p, 0) + 1
    tier_to_pts[tier] = pts_dist

# 档位颜色
tier_colors = {
    '限定': '#ff4d4f',
    '传说': '#fa8c16',
    '史诗': '#722ed1',
    '稀有': '#52c41a',
    '普通': '#8c8c8c'
}

tier_tag_classes = {
    '限定': 'tag-danger',
    '传说': 'tag-warning',
    '史诗': 'tag-purple',
    '稀有': 'tag-success',
    '普通': 'tag-gray'
}

# 统计总档位
tiers = {}
for g in generals:
    t = g['tier']
    tiers[t] = tiers.get(t, 0) + 1

tiers_sorted = [(t, tiers[t]) for t in tiers_order if t in tiers]

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>武将品质体系 PRD v5.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.8; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .cover { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 40px; border-radius: 16px; margin-bottom: 40px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); }
        .cover h1 { font-size: 32px; font-weight: 600; margin-bottom: 20px; }
        .cover-meta { display: flex; flex-wrap: wrap; gap: 20px; font-size: 14px; opacity: 0.9; }
        .cover-meta span { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; }
        .tag { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .tag-primary { background: #667eea; color: white; }
        .tag-success { background: #52c41a; color: white; }
        .tag-warning { background: #faad14; color: white; }
        .tag-danger { background: #ff4d4f; color: white; }
        .tag-gray { background: #8c8c8c; color: white; }
        .tag-purple { background: #722ed1; color: white; }
        .section { background: white; border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-title { font-size: 20px; font-weight: 600; color: #667eea; padding-bottom: 16px; margin-bottom: 20px; border-bottom: 2px solid #f0f0f0; }
        table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
        th { background: #667eea; color: white; padding: 12px 16px; text-align: left; }
        td { padding: 12px 16px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9ff; }
        .text-center { text-align: center; }
        .general-table-wrapper { max-height: 500px; overflow-y: auto; border: 1px solid #e8e8e8; border-radius: 8px; }
        .general-table th { position: sticky; top: 0; z-index: 10; }
        .tier-header { background: #f0f0f0; font-weight: 600; }
        .tier-header td { color: #667eea; padding: 8px 12px !important; }
        .filter-bar { text-align: center; margin: 20px 0; padding: 16px; background: #fafafa; border-radius: 8px; }
        .filter-btn { padding: 8px 16px; margin: 5px; border: 2px solid #667eea; border-radius: 20px; cursor: pointer; background: white; color: #667eea; font-weight: 500; transition: all 0.2s; }
        .filter-btn:hover { background: #667eea; color: white; }
        .filter-btn.active { background: #667eea; color: white; }
        .stats { text-align: center; margin: 12px 0; color: #666; font-size: 14px; }
        .footer { text-align: center; padding: 40px; color: #999; font-size: 13px; }
        .summary-cards { display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }
        .summary-card { flex: 1; min-width: 120px; padding: 20px; border-radius: 12px; text-align: center; color: white; }
        .cross-table { margin-top: 16px; }
        .cross-table th { background: #52c41a; }
        .cross-table td { text-align: center; }
        .points-tag { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; color: white; }
        .pts-500 { background: #722ed1; }
        .pts-120 { background: #1890ff; }
        .pts-100 { background: #fa8c16; }
        .pts-80 { background: #8c8c8c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="cover">
            <h1>武将品质体系 PRD v5.0</h1>
            <div class="cover-meta">
                <span>v5.0</span>
                <span>内部策划文档</span>
                <span>疏白</span>
                <span>2026-06-12</span>
                <span class="tag" style="background:#52c41a">已完成</span>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">一、档位分布</h2>
            <div class="summary-cards">
'''

for tier, count in tiers_sorted:
    color = tier_colors.get(tier, '#667eea')
    pct = round(count / len(generals) * 100, 1)
    html += f'''
                <div class="summary-card" style="background:{color}">
                    <div style="font-size:32px;font-weight:bold">{count}</div>
                    <div>{tier}</div>
                    <div style="font-size:12px;opacity:0.8">{pct}%</div>
                </div>'''

html += '''
            </div>
            <table>
                <thead><tr><th>品质</th><th class="text-center">数量</th><th class="text-center">占比</th></tr></thead>
                <tbody>
'''

for tier, count in tiers_sorted:
    pct = round(count / len(generals) * 100, 1)
    tag_class = tier_tag_classes.get(tier, 'tag-primary')
    html += f'''
                    <tr><td><span class="tag {tag_class}">{tier}</span></td><td class="text-center">{count}</td><td class="text-center">{pct}%</td></tr>'''

html += f'''
                </tbody>
            </table>
            <p style="color:#666;margin-top:16px">共 {len(generals)} 个有效武将，基于v5.0分类规则。</p>
        </div>

        <div class="section">
            <h2 class="section-title">二、原帅点对比分析</h2>
            <p style="color:#666;margin-bottom:16px">原Star评级：1=80帅点，2=100帅点，3=120帅点，4=500帅点</p>

            <h3 style="font-size:16px;color:#333;margin:16px 0 8px">2.1 原帅点 → 当前品质分布</h3>
            <table class="cross-table">
                <thead>
                    <tr>
                        <th>原帅点</th>
                        <th>限定</th>
                        <th>传说</th>
                        <th>史诗</th>
                        <th>稀有</th>
                        <th>普通</th>
                        <th>合计</th>
                    </tr>
                </thead>
                <tbody>
'''

# 表1: 原帅点 -> 当前品质
pts_order = [500, 120, 100, 80]
pts_labels = {500: '500帅点', 120: '120帅点', 100: '100帅点', 80: '80帅点'}
pts_class = {500: 'pts-500', 120: 'pts-120', 100: 'pts-100', 80: 'pts-80'}
tier_name_to_key = {'限定': '限定', '传说': '传说', '史诗': '史诗', '稀有': '稀有', '普通': '普通'}

for pts in pts_order:
    data_row = pts_to_tiers.get(pts, {})
    total = sum(data_row.values())
    if total == 0:
        continue
    pts_label = pts_labels.get(pts, str(pts))
    pts_cls = pts_class.get(pts, '')
    row = f'<tr><td><span class="points-tag {pts_cls}">{pts_label}</span></td>'
    for tier in tiers_order:
        count = data_row.get(tier, 0)
        row += f'<td>{count if count > 0 else "-"}</td>'
    row += f'<td><strong>{total}</strong></td></tr>'
    html += row

html += '''
                </tbody>
            </table>

            <h3 style="font-size:16px;color:#333;margin:24px 0 8px">2.2 当前品质 → 原帅点分布</h3>
            <table class="cross-table">
                <thead>
                    <tr>
                        <th>当前品质</th>
                        <th>500帅</th>
                        <th>120帅</th>
                        <th>100帅</th>
                        <th>80帅</th>
                        <th>合计</th>
                    </tr>
                </thead>
                <tbody>
'''

# 表2: 当前品质 -> 原帅点
for tier in tiers_order:
    pts_data = tier_to_pts.get(tier, {})
    total = sum(pts_data.values())
    if total == 0:
        continue
    tag_class = tier_tag_classes.get(tier, 'tag-primary')
    row = f'<tr><td><span class="tag {tag_class}">{tier}</span></td>'
    for pts in [500, 120, 100, 80]:
        count = pts_data.get(pts, 0)
        row += f'<td>{count if count > 0 else "-"}</td>'
    row += f'<td><strong>{total}</strong></td></tr>'
    html += row

html += '''
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2 class="section-title">三、武将名单</h2>

            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterTier('all')">全部 (''' + str(len(generals)) + ''')</button>
'''

for tier, count in tiers_sorted:
    html += f'''                <button class="filter-btn" onclick="filterTier('{tier}')">{tier} ({count})</button>
'''

html += '''            </div>
            <div class="stats" id="stats"></div>

            <div class="general-table-wrapper">
                <table class="general-table">
                    <thead>
                        <tr><th>武将ID</th><th>武将名称</th><th>档位</th><th>原帅点</th><th>分类依据</th></tr>
                    </thead>
                    <tbody id="tier-body">
'''

# 按档位分组输出
for tier in tiers_order:
    generals_in_tier = [g for g in generals if g['tier'] == tier]
    if not generals_in_tier:
        continue
    generals_in_tier.sort(key=lambda x: x['general_id'])
    tag_class = tier_tag_classes.get(tier, 'tag-primary')
    html += f'<tr class="tier-header"><td colspan="5"><span class="tag {tag_class}">{tier}</span> ({len(generals_in_tier)}个)</td></tr>\n'
    for g in generals_in_tier:
        pts = g.get('old_points', '-')
        pts_str = f'{pts}帅' if pts != '-' else '-'
        html += f'<tr class="general-row"><td>{g["general_id"]}</td><td>{g["name"]}</td><td><span class="tag {tag_class}">{g["tier"]}</span></td><td>{pts_str}</td><td>{g["reason"]}</td></tr>\n'

html += '''                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>武将品质体系 PRD v5.0 | 疏白 | 2026-06-12</p>
        </div>
    </div>

    <script>
        function filterTier(tier) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.includes(tier) || (tier === 'all' && btn.textContent.includes('全部'))) {
                    btn.classList.add('active');
                }
            });
            const rows = document.querySelectorAll('.tier-header, .general-row');
            let visibleCount = 0;
            rows.forEach(row => {
                if (tier === 'all') {
                    row.style.display = '';
                    if (!row.classList.contains('tier-header')) visibleCount++;
                } else {
                    const isHeader = row.classList.contains('tier-header');
                    const containsTier = row.innerHTML.includes('>' + tier + '<');
                    if (isHeader && containsTier) {
                        row.style.display = '';
                    } else if (isHeader) {
                        row.style.display = 'none';
                    } else {
                        row.style.display = containsTier ? '' : 'none';
                        if (containsTier) visibleCount++;
                    }
                }
            });
            document.getElementById('stats').textContent = tier === 'all' ? '显示全部 ''' + str(len(generals)) + ''' 个武将' : '显示 ' + visibleCount + ' 个武将';
        }
        filterTier('all');
    </script>
</body>
</html>'''

with open('武将评级划分/data/武将品质体系PRD_v5.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'已生成: 武将评级划分/data/武将品质体系PRD_v5.html')
print(f'共 {len(generals)} 个武将')

# 保存带帅点的JSON
with open('武将评级划分/data/classification_final_v5_result.json', 'w', encoding='utf-8') as f:
    json.dump(generals, f, ensure_ascii=False, indent=2)
print('已保存: classification_final_v5_result.json (含帅点)')