import json

# 读取数据
with open('tier_data.json', 'r', encoding='utf-8') as f:
    tiers = json.load(f)

#统计各档位下不同来源的数量
def count_by_source(tier_list, source_key):
    count = 0
    for g in tier_list:
        reason = g.get('reason', '')
        if source_key in reason:
            count += 1
    return count

# 生成HTML（完整版，包含行业分析+详细规则表格）
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>武将品质体系 PRD v2.0</title>
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
        .rule-card { background: #f6ffed; border-left: 4px solid #52c41a; padding: 20px; margin: 16px 0; border-radius: 0 8px 8px 0; }
        .rule-card h4 { color: #52c41a; font-size: 15px; margin-bottom: 12px; }
        ul { padding-left: 24px; margin: 12px 0; }
        li { margin: 8px 0; }
        .status-pending { color: #faad14; font-weight: 500; }
        .conclusion-box { background: #fafafa; border: 1px solid #e8e8e8; border-radius: 8px; padding: 16px; }
        .footer { text-align: center; padding: 40px; color: #999; font-size: 13px; }

        /* 武将名单表格样式 */
        .general-table-wrapper { max-height: 600px; overflow-y: auto; border: 1px solid #e8e8e8; border-radius: 8px; }
        .general-table { font-size: 13px; margin: 0; }
        .general-table th { position: sticky; top: 0; z-index: 10; }
        .tier-header { background: #f0f0f0; font-weight: 600; }
        .tier-header td { color: #667eea; padding: 8px 12px !important; }
        .general-row:hover { background: #f8f9ff !important; }

        /* 筛选器样式 */
        .filter-bar { text-align: center; margin: 20px 0; padding: 16px; background: #fafafa; border-radius: 8px; }
        .filter-btn { padding: 8px 16px; margin: 5px; border: 2px solid #667eea; border-radius: 20px; cursor: pointer; background: white; color: #667eea; font-weight: 500; transition: all 0.2s; }
        .filter-btn:hover { background: #667eea; color: white; }
        .filter-btn.active { background: #667eea; color: white; }
        .stats { text-align: center; margin: 12px 0; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <!-- 封面 -->
        <div class="cover">
            <h1>武将品质体系 PRD</h1>
            <div class="cover-meta">
                <span>v2.0</span>
                <span>内部策划文档</span>
                <span>疏白</span>
                <span>2026-06-11</span>
                <span class="tag tag-success">完成</span>
            </div>
        </div>

        <!-- 一、项目背景 -->
        <div class="section">
            <h2 class="section-title">一、项目背景</h2>
            <h3>1.1 问题描述</h3>
            <p>项目组目前没有统一的武将品质分级标准，导致：</p>
            <ul>
                <li>定价参考不统一</li>
                <li>获取难度标注混乱</li>
            </ul>
            <h3>1.2 项目目标</h3>
            <p>建立一套与行业标准对齐的武将品质体系，核心是确定<strong>档位标准</strong>：哪些武将归哪个档。</p>
            <h3>1.3 适用范围</h3>
            <p>内部策划讨论、定价参考、获取难度标注。</p>
        </div>

        <!-- 二、行业现状分析 -->
        <div class="section">
            <h2 class="section-title">二、行业现状分析</h2>

            <h3>2.1 四款"杀类"游戏品质体系对比</h3>
            <table>
                <thead>
                    <tr><th>游戏</th><th class="text-center">档数</th><th>最高品质</th><th>次高品质</th><th>中间品质</th><th>次低品质</th><th>最低品质</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>三国杀OL</strong></td><td class="text-center">5档</td><td><span class="tag tag-danger">限定</span></td><td><span class="tag tag-warning">传说</span></td><td><span class="tag tag-primary">史诗</span></td><td><span class="tag tag-success">稀有</span></td><td><span class="tag tag-gray">普通</span></td></tr>
                    <tr><td><strong>手杀</strong></td><td class="text-center">3档</td><td><span class="tag tag-primary">史诗</span></td><td><span class="tag tag-success">精品</span></td><td>-</td><td>-</td><td><span class="tag tag-gray">普通</span></td></tr>
                    <tr><td><strong>英雄杀</strong></td><td class="text-center">5档</td><td><span class="tag tag-danger">五星</span></td><td><span class="tag tag-warning">四星</span></td><td><span class="tag tag-primary">三星</span></td><td><span class="tag tag-success">二星</span></td><td><span class="tag tag-gray">一星</span></td></tr>
                    <tr><td><strong>名将杀</strong></td><td class="text-center">4档</td><td><span class="tag tag-danger">传说</span></td><td><span class="tag tag-warning">史诗</span></td><td><span class="tag tag-success">稀有</span></td><td><span class="tag tag-gray">普通</span></td><td>-</td></tr>
                </tbody>
            </table>

            <h3>2.2 价格区间对比</h3>
            <p>不同游戏的获取方式不同，以下为各品质的价格参考（统一换算为人民币）：</p>

            <h4>三国杀OL（100元宝 = 1元）</h4>
            <table>
                <thead><tr><th>品质</th><th class="text-center">价格区间（元宝）</th><th class="text-center">人民币</th><th>获取方式</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">限定</span></td><td class="text-center">12万~30万</td><td class="text-center">1200~3000元</td><td>大祈福、玉玺、消费活动</td></tr>
                    <tr><td><span class="tag tag-warning">传说</span></td><td class="text-center">3万~12万</td><td class="text-center">300~1200元</td><td>小祈福、翻翻乐、宝珠</td></tr>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td class="text-center">0.6万~3万</td><td class="text-center">60~300元</td><td>将魂合成、宝珠兑换</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td class="text-center">0.2万~0.6万</td><td class="text-center">20~60元</td><td>灵宝商城、元宝直购</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">-</td><td class="text-center">免费</td><td>新手赠送、标准包</td></tr>
                </tbody>
            </table>

            <h4>手杀（史诗宝珠 1珠 ≈ 10元）</h4>
            <table>
                <thead><tr><th>品质</th><th class="text-center">价格区间</th><th class="text-center">人民币</th><th>获取方式</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td class="text-center">40~150宝珠</td><td class="text-center">400~3500元</td><td>史诗宝珠、将魂合成、祈福</td></tr>
                    <tr><td><span class="tag tag-success">精品</span></td><td class="text-center">1000~4000将魂</td><td class="text-center">35~200元</td><td>元宝直购、将魂、手杀豆</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">-</td><td class="text-center">免费</td><td>新手赠送、标准包</td></tr>
                </tbody>
            </table>

            <h4>英雄杀（10元宝 = 1元）</h4>
            <table>
                <thead><tr><th>品质</th><th class="text-center">价格区间（元宝）</th><th class="text-center">人民币</th><th>获取方式</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">五星</span></td><td class="text-center">8万~20万</td><td class="text-center">8000~20000元</td><td>探宝、藏宝阁、累充</td></tr>
                    <tr><td><span class="tag tag-warning">四星</span></td><td class="text-center">2万~4.5万</td><td class="text-center">2000~4500元</td><td>探宝、兑宝、活动兑换</td></tr>
                    <tr><td><span class="tag tag-primary">三星</span></td><td class="text-center">1.5万</td><td class="text-center">1500元</td><td>银币抽、元宝十连</td></tr>
                    <tr><td><span class="tag tag-success">二星</span></td><td class="text-center">3000~8000</td><td class="text-center">300~800元</td><td>新手礼包、碎片合成</td></tr>
                    <tr><td><span class="tag tag-gray">一星</span></td><td class="text-center">-</td><td class="text-center">免费</td><td>登录赠送、新手教程</td></tr>
                </tbody>
            </table>

            <h4>名将杀</h4>
            <table>
                <thead><tr><th>品质</th><th class="text-center">玉猪龙</th><th class="text-center">人民币（估算）</th><th>获取方式</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">传说</span></td><td class="text-center">1600</td><td class="text-center">800~1200元</td><td>名将招募、玉猪龙合成</td></tr>
                    <tr><td><span class="tag tag-warning">史诗</span></td><td class="text-center">400</td><td class="text-center">200~300元</td><td>招募、合成、活动</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td class="text-center">80</td><td class="text-center">40~60元</td><td>招募、日常、碎片</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">25</td><td class="text-center">几元</td><td>新手赠送、招募、活动</td></tr>
                </tbody>
            </table>

            <h3>2.3 核心结论（3条）</h3>
            <div class="conclusion-box">
                <table>
                    <thead><tr><th>#</th><th>结论</th><th>说明</th></tr></thead>
                    <tbody>
                        <tr><td class="text-center">1</td><td><strong>行业主流是5档体系</strong></td><td>OL和英雄杀采用，英雄杀用星级替代名称</td></tr>
                        <tr><td class="text-center">2</td><td><strong>价格跨度极大</strong></td><td>最高品质可达数千元，最低品质免费</td></tr>
                        <tr><td class="text-center">3</td><td><strong>获取方式多元</strong></td><td>祈福/翻翻乐/将魂合成/宝珠兑换/活动等多种渠道</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 三、分类规则 v2.0 -->
        <div class="section">
            <h2 class="section-title">三、分类规则 v2.0</h2>
            <p>基于获取途径和价格双重维度，制定档位划分规则：</p>

            <h3>3.1 档位划分规则与分布（完整版）</h3>
            <table>
                <thead>
                    <tr><th>品质</th><th>获取途径</th><th>评级规则</th><th class="text-center">数量</th><th class="text-center">占比</th></tr>
                </thead>
                <tbody>
                    <tr><td rowspan="2"><span class="tag tag-danger">限定</span></td><td>武庙/高山仰止</td><td>武庙珍藏/高山仰止系列（固定限定档）</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>珍宝价格</td><td>珍宝价格 >= 200,000</td><td class="text-center">-</td><td class="text-center">-</td></tr>

                    <tr><td rowspan="3"><span class="tag tag-warning">传说</span></td><td>祈福</td><td>祈福(1004)（固定传说档）</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>将星招募</td><td>将星价格 >= 10,000</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>珍宝价格</td><td>珍宝价格 >= 100,000</td><td class="text-center">-</td><td class="text-center">-</td></tr>

                    <tr><td rowspan="7"><span class="tag tag-primary">史诗</span></td><td>纳贤</td><td>纳贤(1001)（固定史诗档）</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>神将任务</td><td>神将任务(5002)（固定史诗档）</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>首充/充值奖励</td><td>首充(2000)/充值奖励(2002/2003/3001/1005)</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>将星招募</td><td>将星价格 2,000~9,999</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>宝玉兑换(1101)</td><td>宝玉兑换，查道具定价表珍宝价格 >= 10,000</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>珍宝(1003)</td><td>珍宝兑换，查道具定价表珍宝价格 >= 10,000</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>活动投放</td><td>部分活动增加的目标性武将</td><td class="text-center">-</td><td class="text-center">-</td></tr>

                    <tr><td rowspan="5"><span class="tag tag-success">稀有</span></td><td>将星招募</td><td>将星价格 100~1,999</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>宝玉兑换(1101)</td><td>宝玉兑换，查道具定价表珍宝价格 1,001~9,999</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>珍宝(1003)</td><td>珍宝兑换，查道具定价表珍宝价格 1,001~9,999</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>界限突破</td><td>界限突破系列武将</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>活动赠送</td><td>大部分活动赠送武将</td><td class="text-center">-</td><td class="text-center">-</td></tr>

                    <tr><td rowspan="2"><span class="tag tag-gray">普通</span></td><td>将星招募</td><td>将星价格 >0 且 <100</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                    <tr><td>普通招募</td><td>包含普通招募途径(1)</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                </tbody>
            </table>

            <h3>3.2 档位分布汇总</h3>
            <table>
                <thead><tr><th>品质</th><th class="text-center">数量</th><th class="text-center">占比</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">限定</span></td><td class="text-center">59</td><td class="text-center">8.8%</td></tr>
                    <tr><td><span class="tag tag-warning">传说</span></td><td class="text-center">38</td><td class="text-center">5.6%</td></tr>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td class="text-center">224</td><td class="text-center">33.3%</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td class="text-center">134</td><td class="text-center">19.9%</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">201</td><td class="text-center">29.9%</td></tr>
                </tbody>
            </table>
            <p style="color:#666;font-size:13px;">*排除17个无法分类的武将</p>
        </div>

        <!-- 四、武将名单 -->
        <div class="section">
            <h2 class="section-title">四、武将名单</h2>
            <p>共656个有效武将，基于v2.0分类规则。支持按档位筛选查看。</p>

            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterTier('all')">全部 (656)</button>
                <button class="filter-btn" onclick="filterTier('限定')">限定 (59)</button>
                <button class="filter-btn" onclick="filterTier('传说')">传说 (38)</button>
                <button class="filter-btn" onclick="filterTier('史诗')">史诗 (224)</button>
                <button class="filter-btn" onclick="filterTier('稀有')">稀有 (134)</button>
                <button class="filter-btn" onclick="filterTier('普通')">普通 (201)</button>
            </div>
            <div class="stats" id="stats"></div>

            <div class="general-table-wrapper">
                <table class="general-table">
                    <thead>
                        <tr>
                            <th style="min-width:80px;">武将ID</th>
                            <th style="min-width:100px;">武将名称</th>
                            <th style="min-width:80px;">档位</th>
                            <th style="min-width:120px;">划分依据</th>
                            <th style="min-width:80px;">将星价格</th>
                            <th style="min-width:80px;">珍宝价格</th>
                        </tr>
                    </thead>
                    <tbody id="tier-body">
'''

# 添加各档位武将
tier_configs = [
    ('限定', 'tag-danger', 59),
    ('传说', 'tag-warning', 38),
    ('史诗', 'tag-primary', 224),
    ('稀有', 'tag-success', 134),
    ('普通', 'tag-gray', 201)
]

for tier_name, tag_class, count in tier_configs:
    html += '<tr class="tier-header"><td colspan="6"><span class="tag ' + tag_class + '">' + tier_name + '</span> (' + str(count) + '个)</td></tr>\n'
    for g in tiers.get(tier_name, []):
        reason = g.get('reason', '')
        jiangxing = g.get('jiangxing', '-')
        zhenbao = g.get('zhenbao', '-')
        if jiangxing == '':
            jiangxing = '-'
        if zhenbao == '':
            zhenbao = '-'
        html += '<tr class="general-row"><td>' + str(g['id']) + '</td><td>' + g['name'] + '</td><td><span class="tag ' + tag_class + '">' + tier_name + '</span></td><td>' + reason + '</td><td>' + str(jiangxing) + '</td><td>' + str(zhenbao) + '</td></tr>\n'

html += '''                    </tbody>
                </table>
            </div>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>武将品质体系 PRD v2.0 | 疏白 | 2026-06-11</p>
        </div>
    </div>

    <script>
        function filterTier(tier) {
            // 更新按钮状态
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.includes(tier) || (tier === 'all' && btn.textContent.includes('全部'))) {
                    btn.classList.add('active');
                }
            });

            // 筛选显示
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

            // 更新统计
            document.getElementById('stats').textContent = tier === 'all' ? '显示全部 656 个武将' : '显示 ' + visibleCount + ' 个武将';
        }

        // 初始化
        filterTier('all');
    </script>
</body>
</html>'''

# 保存HTML
with open('武将品质体系PRD_v2.0.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML文件已生成:武将品质体系PRD_v2.0.html')
print('总计:',59 + 38 + 224 + 134 + 201, '个武将')