# -*- coding: utf-8 -*-
import pandas as pd

# 读取数据
df = pd.read_excel('武将评级合并_v32.xlsx', sheet_name='武将名单')
DELETE_NAMES = {'威马腾', '威曹彰', '谋诸葛亮'}
df = df[~df['武将名称'].isin(DELETE_NAMES)]
tier_order = {'限定': 1, '传说': 2, '史诗': 3, '稀有': 4, '普通': 5}
df['sort_key'] = df['品质'].map(tier_order)
df = df.sort_values(['sort_key', '武将名称'])
df = df.drop('sort_key', axis=1)

# 生成行
rows_html = []
current_tier = None
for _, row in df.iterrows():
    tier = row['品质']
    if tier != current_tier:
        if current_tier is not None:
            rows_html.append('</tbody>')
        tc = 'danger' if tier == '限定' else 'warning' if tier == '传说' else 'primary' if tier == '史诗' else 'success' if tier == '稀有' else 'gray'
        count = len(df[df['品质'] == tier])
        rows_html.append(f'<tbody id="tier-{tier}" class="tier-section">')
        rows_html.append(f'<tr class="tier-header"><td colspan="5"><span class="tag tag-{tc}">{tier}</span> ({count}个)</td></tr>')
        current_tier = tier

    name = row['武将名称']
    tier = row['品质']
    reason = row['划分依据']
    jx = row['正确将星价格']
    by = row['宝玉数量']
    jx_str = str(int(float(jx))) if pd.notna(jx) and jx != '-' else '-'
    by_str = str(int(float(by))) if pd.notna(by) and by != '-' else '-'
    tc = 'danger' if tier == '限定' else 'warning' if tier == '传说' else 'primary' if tier == '史诗' else 'success' if tier == '稀有' else 'gray'
    rows_html.append(f'<tr class="general-row"><td>{name}</td><td><span class="tag tag-{tc}">{tier}</span></td><td>{reason}</td><td>{jx_str}</td><td>{by_str}</td></tr>')

rows_html.append('</tbody>')

rows_content = '\n'.join(rows_html)

# 更新后的数据统计
tier_counts = df.groupby('品质').size().to_dict()
total = len(df)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>武将品质体系 PRD v1.0</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; line-height: 1.8; color: #333; background: #f5f5f5; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 40px 20px; }}
        .cover {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 40px; border-radius: 16px; margin-bottom: 40px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); }}
        .cover h1 {{ font-size: 32px; font-weight: 600; margin-bottom: 20px; }}
        .cover-meta {{ display: flex; flex-wrap: wrap; gap: 20px; font-size: 14px; opacity: 0.9; }}
        .cover-meta span {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; }}
        .section {{ background: white; border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .section-title {{ font-size: 20px; font-weight: 600; color: #667eea; padding-bottom: 16px; margin-bottom: 20px; border-bottom: 2px solid #f0f0f0; }}
        .section h3 {{ font-size: 16px; font-weight: 600; color: #444; margin: 24px 0 12px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }}
        th {{ background: #667eea; color: white; padding: 12px 16px; text-align: left; font-weight: 500; }}
        td {{ padding: 12px 16px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9ff; }}
        .text-center {{ text-align: center; }}
        .tag {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }}
        .tag-primary {{ background: #667eea; color: white; }}
        .tag-success {{ background: #52c41a; color: white; }}
        .tag-warning {{ background: #faad14; color: white; }}
        .tag-danger {{ background: #ff4d4f; color: white; }}
        .tag-gray {{ background: #8c8c8c; color: white; }}
        .rule-card {{ background: #f6ffed; border-left: 4px solid #52c41a; padding: 20px; margin: 16px 0; border-radius: 0 8px 8px 0; }}
        .rule-card h4 {{ color: #52c41a; font-size: 15px; margin-bottom: 12px; }}
        ul {{ padding-left: 24px; margin: 12px 0; }}
        li {{ margin: 8px 0; }}
        .status-pending {{ color: #faad14; font-weight: 500; }}
        .conclusion-box {{ background: #fafafa; border: 1px solid #e8e8e8; border-radius: 8px; padding: 16px; }}
        .review-section {{ background: #fafafa; border: 1px dashed #ddd; border-radius: 8px; padding: 20px; }}
        .review-item {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #eee; }}
        .review-item:last-child {{ border-bottom: none; }}
        .footer {{ text-align: center; padding: 40px; color: #999; font-size: 13px; }}

        /* 武将名单表格样式 */
        .general-table-wrapper {{ max-height: 600px; overflow-y: auto; border: 1px solid #e8e8e8; border-radius: 8px; }}
        .general-table {{ font-size: 13px; margin: 0; }}
        .general-table th {{ position: sticky; top: 0; z-index: 10; }}
        .tier-header {{ background: #f0f0f0; font-weight: 600; }}
        .tier-header td {{ color: #667eea; padding: 8px 12px !important; }}
        .general-row:hover {{ background: #f8f9ff !important; }}

        /* 筛选器样式 */
        .filter-bar {{ text-align: center; margin: 20px 0; padding: 16px; background: #fafafa; border-radius: 8px; }}
        .filter-btn {{ padding: 8px 16px; margin: 5px; border: 2px solid #667eea; border-radius: 20px; cursor: pointer; background: white; color: #667eea; font-weight: 500; transition: all 0.2s; }}
        .filter-btn:hover {{ background: #667eea; color: white; }}
        .filter-btn.active {{ background: #667eea; color: white; }}
        .stats {{ text-align: center; margin: 12px 0; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 封面 -->
        <div class="cover">
            <h1>武将品质体系 PRD</h1>
            <div class="cover-meta">
                <span>v1.0</span>
                <span>内部策划文档</span>
                <span>疏白</span>
                <span>2026-05-27</span>
                <span class="tag tag-warning">待评审</span>
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

        <!-- 三、当前数据现状 -->
        <div class="section">
            <h2 class="section-title">三、当前数据现状</h2>
            <h3>3.1 档位分布（v32，共{total}个武将）</h3>
            <table>
                <thead><tr><th>品质</th><th class="text-center">数量</th><th class="text-center">占比</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">限定</span></td><td class="text-center">{tier_counts.get('限定', 0)}</td><td class="text-center">{tier_counts.get('限定', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-warning">传说</span></td><td class="text-center">{tier_counts.get('传说', 0)}</td><td class="text-center">{tier_counts.get('传说', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td class="text-center">{tier_counts.get('史诗', 0)}</td><td class="text-center">{tier_counts.get('史诗', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td class="text-center">{tier_counts.get('稀有', 0)}</td><td class="text-center">{tier_counts.get('稀有', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">{tier_counts.get('普通', 0)}</td><td class="text-center">{tier_counts.get('普通', 0)/total*100:.1f}%</td></tr>
                </tbody>
            </table>
        </div>

        <!-- 四、我们的档位规则 -->
        <div class="section">
            <h2 class="section-title">四、我们的档位规则</h2>
            <p>基于获取途径和价格双重维度，制定档位划分规则：</p>

            <h3>4.1 档位划分规则与分布（完整版）</h3>
            <table>
                <thead><tr><th>品质</th><th>获取途径</th><th>评级规则</th><th class="text-center">数量</th><th class="text-center">占比</th></tr></thead>
                <tbody>
                    <tr><td rowspan="2"><span class="tag tag-danger">限定</span></td><td>珍宝</td><td>宝玉 ≥ 20个</td><td class="text-center">25</td><td class="text-center">3.7%</td></tr>
                    <tr><td>武庙+高山仰止</td><td>高山仰止系列（固定限定档）</td><td class="text-center">2</td><td class="text-center">0.3%</td></tr>
                    <tr><td rowspan="3"><span class="tag tag-warning">传说</span></td><td>祈福</td><td>祈福（固定传说档）</td><td class="text-center">8</td><td class="text-center">1.2%</td></tr>
                    <tr><td>将星招募</td><td>将星价格 ≥ 1万</td><td class="text-center">19</td><td class="text-center">2.8%</td></tr>
                    <tr><td>珍宝</td><td>宝玉 < 5个</td><td class="text-center">4</td><td class="text-center">0.6%</td></tr>
                    <tr><td rowspan="4"><span class="tag tag-primary">史诗</span></td><td>纳贤</td><td>纳贤（固定史诗档）</td><td class="text-center">13</td><td class="text-center">1.9%</td></tr>
                    <tr><td>神将任务</td><td>神将任务（固定史诗档）</td><td class="text-center">10</td><td class="text-center">1.5%</td></tr>
                    <tr><td>将星招募</td><td>将星价格 2000~9999</td><td class="text-center">127</td><td class="text-center">18.9%</td></tr>
                    <tr><td>珍宝</td><td>宝玉 10~20个</td><td class="text-center">10</td><td class="text-center">1.5%</td></tr>
                    <tr><td rowspan="3"><span class="tag tag-success">稀有</span></td><td>珍宝</td><td>宝玉 5~10个 或 <5个</td><td class="text-center">11</td><td class="text-center">1.6%</td></tr>
                    <tr><td>将星招募</td><td>将星价格 100~2000</td><td class="text-center">76</td><td class="text-center">11.3%</td></tr>
                    <tr><td colspan="2">珍宝<5个归稀有</td><td class="text-center">2</td><td class="text-center">0.3%</td></tr>
                    <tr><td rowspan="2"><span class="tag tag-gray">普通</span></td><td>将星招募</td><td>将星价格 < 100</td><td class="text-center">368</td><td class="text-center">54.7%</td></tr>
                    <tr><td>新手等活动</td><td>新手等活动赠送武将</td><td class="text-center">-</td><td class="text-center">-</td></tr>
                </tbody>
            </table>

            <h3>4.2 品质分布汇总</h3>
            <table>
                <thead><tr><th>品质</th><th class="text-center">数量</th><th class="text-center">占比</th></tr></thead>
                <tbody>
                    <tr><td><span class="tag tag-danger">限定</span></td><td class="text-center">{tier_counts.get('限定', 0)}</td><td class="text-center">{tier_counts.get('限定', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-warning">传说</span></td><td class="text-center">{tier_counts.get('传说', 0)}</td><td class="text-center">{tier_counts.get('传说', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-primary">史诗</span></td><td class="text-center">{tier_counts.get('史诗', 0)}</td><td class="text-center">{tier_counts.get('史诗', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-success">稀有</span></td><td class="text-center">{tier_counts.get('稀有', 0)}</td><td class="text-center">{tier_counts.get('稀有', 0)/total*100:.1f}%</td></tr>
                    <tr><td><span class="tag tag-gray">普通</span></td><td class="text-center">{tier_counts.get('普通', 0)}</td><td class="text-center">{tier_counts.get('普通', 0)/total*100:.1f}%</td></tr>
                </tbody>
            </table>

            <h3>4.3 获取途径分类</h3>

            <div class="rule-card">
                <h4>珍宝</h4>
                <ul>
                    <li>珍宝价格 ≥ 20万 → <span class="tag tag-danger">限定</span></li>
                    <li>珍宝价格 10~20万 → <span class="tag tag-primary">史诗</span></li>
                    <li>珍宝价格 5~10万 → <span class="tag tag-success">稀有</span></li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>祈福</h4>
                <ul>
                    <li>祈福武将 → <span class="tag tag-warning">传说</span>（固定传说档）</li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>武庙+高山仰止</h4>
                <ul>
                    <li>高山仰止系列 → <span class="tag tag-danger">限定</span>（固定限定档）</li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>纳贤</h4>
                <ul>
                    <li>纳贤武将 → <span class="tag tag-primary">史诗</span>（固定史诗档）</li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>神将任务</h4>
                <ul>
                    <li>神将任务武将 → <span class="tag tag-primary">史诗</span>（固定史诗档）</li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>将星招募</h4>
                <ul>
                    <li>将星价格 ≥ 1万 → <span class="tag tag-warning">传说</span></li>
                    <li>将星价格 2000~9999 → <span class="tag tag-primary">史诗</span></li>
                    <li>将星价格 100~2000 → <span class="tag tag-success">稀有</span></li>
                    <li>将星价格 < 100 → <span class="tag tag-gray">普通</span></li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>运营活动 / 更多方式</h4>
                <ul>
                    <li>运营活动价格 ≥ 20万 → <span class="tag tag-warning">传说</span></li>
                    <li>运营活动价格 10~20万 → <span class="tag tag-primary">史诗</span></li>
                    <li>运营活动价格 1001~10万 → <span class="tag tag-success">稀有</span></li>
                    <li>运营活动价格 ≤ 1000 → <span class="tag tag-gray">普通</span></li>
                </ul>
            </div>

            <div class="rule-card">
                <h4>目标投放</h4>
                <ul>
                    <li>高官阶投放/新手关键节点投放 → <span class="tag tag-warning">传说</span></li>
                    <li>无双上将/新手运营活动/高强度武将/官阶武将 → <span class="tag tag-primary">史诗</span></li>
                    <li>部分活动投放低强度武将 → <span class="tag tag-success">稀有</span></li>
                </ul>
            </div>
        </div>

        <!-- 六、武将名单 -->
        <div class="section">
            <h2 class="section-title">六、武将名单</h2>
            <p>共{total}个武将，基于v32数据分类。支持按档位筛选查看。</p>

            <!-- 筛选器 -->
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterTier('all')">全部</button>
                <button class="filter-btn" onclick="filterTier('限定')">限定 ({tier_counts.get('限定', 0)})</button>
                <button class="filter-btn" onclick="filterTier('传说')">传说 ({tier_counts.get('传说', 0)})</button>
                <button class="filter-btn" onclick="filterTier('史诗')">史诗 ({tier_counts.get('史诗', 0)})</button>
                <button class="filter-btn" onclick="filterTier('稀有')">稀有 ({tier_counts.get('稀有', 0)})</button>
                <button class="filter-btn" onclick="filterTier('普通')">普通 ({tier_counts.get('普通', 0)})</button>
            </div>
            <div class="stats" id="stats"></div>

            <!-- 武将表格 -->
            <div class="general-table-wrapper">
                <table class="general-table">
                    <thead>
                        <tr>
                            <th style="min-width:80px;">武将名称</th>
                            <th style="min-width:60px;">档位</th>
                            <th style="min-width:100px;">划分依据</th>
                            <th style="min-width:80px;">将星价格</th>
                            <th style="min-width:60px;">宝玉</th>
                        </tr>
                    </thead>
                    {rows_content}
                </table>
            </div>
            <p style="margin-top:16px; color:#666; font-size:13px;">* 完整数据请查看附件：武将评级划分/data/武将评级合并_v32.xlsx</p>
        </div>

        <!-- 七、附件 -->
        <div class="section">
            <h2 class="section-title">七、附件</h2>
            <table>
                <thead><tr><th>附件</th><th>文件名</th><th>说明</th></tr></thead>
                <tbody>
                    <tr><td>A</td><td>武将评级划分/data/武将评级合并_v32.xlsx</td><td>673个武将完整列表（含品质、划分依据、将星价格、宝玉数量）</td></tr>
                    <tr><td>B</td><td>武将评级划分/data/武将评级完整名单_v22.xlsx</td><td>原始武将名单</td></tr>
                    <tr><td>C</td><td>四款杀类游戏武将品质价格对照表.xlsx</td><td>行业横向对比</td></tr>
                </tbody>
            </table>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>武将品质体系 PRD v1.0 | 内部策划文档</p>
            <p style="margin-top:8px;">最后更新：2026-05-27</p>
        </div>
    </div>

    <script>
        function filterTier(tier) {{
            // 更新按钮状态
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // 筛选表格
            const sections = document.querySelectorAll('.tier-section');
            let count = 0;
            sections.forEach(section => {{
                if (tier === 'all' || section.id === 'tier-' + tier) {{
                    section.style.display = '';
                    count += section.querySelectorAll('.general-row').length;
                }} else {{
                    section.style.display = 'none';
                }}
            }});

            // 更新统计
            document.getElementById('stats').textContent = tier === 'all' ? '共{total}个武将' : tier + '：' + count + '个武将';
        }}
    </script>
</body>
</html>'''

with open('../../requirements/武将品质体系PRD_v1.0.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("合并完成！")
print(f"总武将数: {total}")
print(f"限定: {tier_counts.get('限定', 0)}")
print(f"传说: {tier_counts.get('传说', 0)}")
print(f"史诗: {tier_counts.get('史诗', 0)}")
print(f"稀有: {tier_counts.get('稀有', 0)}")
print(f"普通: {tier_counts.get('普通', 0)}")
