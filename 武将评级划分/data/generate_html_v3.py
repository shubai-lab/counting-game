# -*- coding: utf-8 -*-
"""
武将品质体系 HTML文档生成脚本 v3
基于 classification_final5_result.json 生成
"""

import json

# 读取数据
with open('c:/Users/zhangfan/my-openspec-project/武将评级划分/data/classification_final5_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 按档位分组
tiers = {'限定': [], '传说': [], '史诗': [], '稀有': [], '普通': [], '待手动确认': []}
for g in data:
    t = g.get('tier', '待手动确认')
    if t in tiers:
        tiers[t].append(g)

# 统计
tier_counts = {t: len(tiers[t]) for t in tiers}
total = len(data)

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>武将品质体系 PRD v3.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; line-height: 1.8; color: #333; background: #f5f5f5; }
        .container { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
        .cover { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 40px; border-radius: 16px; margin-bottom: 40px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); }
        .cover h1 { font-size: 32px; font-weight: 600; margin-bottom: 20px; }
        .cover-meta { display: flex; flex-wrap: wrap; gap: 20px; font-size: 14px; opacity: 0.9; }
        .cover-meta span { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; }
        .section { background: white; border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-title { font-size: 20px; font-weight: 600; color: #667eea; padding-bottom: 16px; margin-bottom: 20px; border-bottom: 2px solid #f0f0f0; }
        .section h3 { font-size: 16px; font-weight: 600; color: #444; margin: 24px 0 12px 0; }
        .section h4 { font-size: 14px; font-weight: 600; color: #666; margin: 16px 0 8px 0; }
        table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
        th { background: #667eea; color: white; padding: 12px 16px; text-align: left; font-weight: 500; }
        td { padding: 12px 16px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9ff; }
        .text-center { text-align: center; }
        .tag { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .tag-primary { background: #667eea; color: white; }
        .tag-success { background: #52c41a; color: white; }
        .tag-warning { background: #faad14; color: white; }
        .tag-danger { background: #ff4d4f; color: white; }
        .tag-gray { background: #8c8c8c; color: white; }
        .tag-purple { background: #722ed1; color: white; }
        .rule-card { background: #f6ffed; border-left: 4px solid #52c41a; padding: 20px; margin: 16px 0; border-radius: 0 8px 8px 0; }
        .rule-card h4 { color: #52c41a; font-size: 15px; margin-bottom: 12px; }
        ul { padding-left: 24px; margin: 12px 0; }
        li { margin: 8px 0; }
        .status-pending { color: #faad14; font-weight: 500; }
        .conclusion-box { background: #fafafa; border: 1px solid #e8e8e8; border-radius: 8px; padding: 16px; }
        .footer { text-align: center; padding: 40px; color: #999; font-size: 13px; }
        .general-table-wrapper { max-height: 600px; overflow-y: auto; border: 1px solid #e8e8e8; border-radius: 8px; }
        .general-table { font-size: 13px; margin: 0; }
        .general-table th { position: sticky; top: 0; z-index: 10; }
        .tier-header { background: #f0f0f0; font-weight: 600; }
        .tier-header td { color: #667eea; padding: 8px 12px !important; }
        .general-row:hover { background: #f8f9ff !important; }
        .filter-bar { text-align: center; margin: 20px 0; padding: 16px; background: #fafafa; border-radius: 8px; }
        .filter-btn { padding: 8px 16px; margin: 5px; border: 2px solid #667eea; border-radius: 20px; cursor: pointer; background: white; color: #667eea; font-weight: 500; transition: all 0.2s; }
        .filter-btn:hover { background: #667eea; color: white; }
        .filter-btn.active { background: #667eea; color: white; }
        .stats { text-align: center; margin: 12px 0; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="cover">
            <h1>武将品质体系 PRD v3.0</h1>
            <div class="cover-meta">
                <span>v3.0</span>
                <span>内部策划文档</span>
                <span>疏白</span>
                <span>2026-06-12</span>
                <span class="tag tag-success">完成</span>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">一、项目背景</h2>
            <p>项目组需要对武将进行统一的品质分级，用于：定价参考、获取难度标注、玩家资源规划。</p>
            <h3>1.1 行业现状</h3>
            <p>三国杀OL采用<strong>限定/传说/史诗/稀有/普通</strong>5档体系，价格跨度从免费到数千元。</p>
           <h3>1.2 项目目标</h3>
            <p>建立一套与行业标准对齐的武将品质体系，输出673个武将的完整分级。</p>
        </div>

        <div class="section">
            <h2 class="section-title">二、分类规则 v3.0</h2>
            <h3>2.1 档位划分规则</h3>
            <table>
                <thead>
                    <tr><th>品质</th><th>获取途径</th><th>评级规则</th></tr>
                </thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">限定</span></td><td>武庙/高山仰止/威前缀</td><td>武庙珍藏/高山仰止；威前缀；珍宝>200,000</td></tr>
                    <tr><td><span class="tag tag-warning">传说</span></td><td>祈福/将星高价</td><td>祈福(1004)固定；将星≥9,999；珍宝>150,000且≤200,000</td></tr>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td>纳贤/神将任务/无双上将</td><td>纳贤(1001)/神将任务(5002)；将星2,000~9,998；珍宝>100,000且≤150,000</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td>界限突破/活动</td><td>界限突破(12)；将星100~1,999；珍宝>1,000且≤100,000</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td>普通招募</td><td>普通招募(1)；珍宝≤1,000</td></tr>
                </tbody>
            </table>

            <h3>2.2 档位分布汇总 v3.0</h3>
            <table>
                <thead><tr><th>品质</th><th class="text-center">数量</th><th class="text-center">占比</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">限定</span></td><td class="text-center">''' + str(tier_counts['限定']) + '''</td><td class="text-center">''' + f"{tier_counts['限定']/total*100:.1f}%" + '''</td></tr>
                    <tr><td><span class="tag tag-warning">传说</span></td><td class="text-center">''' + str(tier_counts['传说']) + '''</td><td class="text-center">''' + f"{tier_counts['传说']/total*100:.1f}%" + '''</td></tr>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td class="text-center">''' + str(tier_counts['史诗']) + '''</td><td class="text-center">''' + f"{tier_counts['史诗']/total*100:.1f}%" + '''</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td class="text-center">''' + str(tier_counts['稀有']) + '''</td><td class="text-center">''' + f"{tier_counts['稀有']/total*100:.1f}%" + '''</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">''' + str(tier_counts['普通']) + '''</td><td class="text-center">''' + f"{tier_counts['普通']/total*100:.1f}%" + '''</td></tr>
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2 class="section-title">三、武将名单</h2>
            <p>共''' + str(total) + '''个有效武将，基于v3.0分类规则。</p>

            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterTier('all')">全部 (''' + str(total) + ''')</button>
                <button class="filter-btn" onclick="filterTier('限定')">限定 (''' + str(tier_counts['限定']) + ''')</button>
                <button class="filter-btn" onclick="filterTier('传说')">传说 (''' + str(tier_counts['传说']) + ''')</button>
                <button class="filter-btn" onclick="filterTier('史诗')">史诗 (''' + str(tier_counts['史诗']) + ''')</button>
                <button class="filter-btn" onclick="filterTier('稀有')">稀有 (''' + str(tier_counts['稀有']) + ''')</button>
                <button class="filter-btn" onclick="filterTier('普通')">普通 (''' + str(tier_counts['普通']) + ''')</button>
            </div>
            <div class="stats" id="stats"></div>

            <div class="general-table-wrapper">
                <table class="general-table">
                    <thead>
                        <tr>
                            <th style="min-width:80px;">武将ID</th>
                            <th style="min-width:100px;">武将名称</th>
                            <th style="min-width:80px;">档位</th>
                            <th style="min-width:200px;">划分依据</th>
                        </tr>
                    </thead>
                    <tbody id="tier-body">
'''

# 添加各档位武将
tier_configs = [
    ('限定', 'tag-danger', tier_counts['限定']),
    ('传说', 'tag-warning', tier_counts['传说']),
    ('史诗', 'tag-primary', tier_counts['史诗']),
    ('稀有', 'tag-success', tier_counts['稀有']),
    ('普通', 'tag-gray', tier_counts['普通'])
]

for tier_name, tag_class, count in tier_configs:
    html += '<tr class="tier-header"><td colspan="4"><span class="tag ' + tag_class + '">' + tier_name + '</span> (' + str(count) + '个)</td></tr>\n'
    for g in tiers[tier_name]:
        reason = g.get('reason', '')
        html += '<tr class="general-row"><td>' + str(g['general_id']) + '</td><td>' + g.get('name', '') + '</td><td><span class="tag ' + tag_class + '">' + tier_name + '</span></td><td>' + reason + '</td></tr>\n'

html += '''                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>武将品质体系 PRD v3.0 | 疏白 | 2026-06-12</p>
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

            document.getElementById('stats').textContent = tier === 'all' ? '显示全部 ''' + str(total) + ''' 个武将' : '显示 ' + visibleCount + ' 个武将';
        }
        filterTier('all');
    </script>
</body>
</html>'''

# 保存HTML
output_path = 'c:/Users/zhangfan/my-openspec-project/武将评级划分/data/武将品质体系PRD_v3.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'HTML文件已生成: {output_path}')
print(f'总计: {total} 个武将')
print(f'档位分布: 限定={tier_counts["限定"]}, 传说={tier_counts["传说"]}, 史诗={tier_counts["史诗"]}, 稀有={tier_counts["稀有"]}, 普通={tier_counts["普通"]}')