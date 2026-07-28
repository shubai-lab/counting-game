# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('武将评级划分/data/classification_final_v4_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 筛选待手动确认的武将
pending = [item for item in data if item['tier'] == '待手动确认']
pending.sort(key=lambda x: x['general_id'])

# LampType分类建议
lamp_suggestions = {
    '逐鹿': '稀有',
    '上兵伐谋': '稀有',
    '黄巾之乱': '稀有',
    '锦瑟良缘': '稀有',
    '皇家贵胄': '稀有',
    '往者可谏': '稀有',
    '一将成名': '稀有',
    '豆蔻梢头': '稀有',
    '奇人异士': '稀有',
    '正音雅乐': '史诗',
    '百战虎贲': '稀有',
    '计将安出': '稀有',
    '天下归心': '稀有',
    '悬壶济世': '稀有',
    '兵临城下': '稀有',
    '中原狼烟': '稀有',
    '戚宦之争': '稀有',
    '虓虎悲歌': '稀有',
    '太平甲子': '稀有',
    '异军突起': '稀有',
    '绕庭之鸦': '稀有',
    '群雄伺动': '稀有',
    '代汉涂高': '稀有',
    '江湖之远': '稀有',
    '徐州风云': '稀有',
    '匡鼎炎汉': '稀有',
    '一将成名2023': '稀有',
    '一将成名2025': '稀有',
    '武侯定南': '稀有',
    '伯言绽火': '稀有',
    '幼麟绝战': '稀有',
    '奇佐论胜': '稀有',
    '周郎将计': '稀有',
    '子敬邀刀': '稀有',
    '凤雏溯攻': '稀有',
    '冢虎狼顾': '稀有',
    '毒士鸩计': '稀有',
    '王佐倡义': '稀有',
    '钟灵毓秀': '传说',
    '隐山之玉': '传说',
    '谋定天下': '传说',
    '谋': '传说',
}

def get_suggestion(lamp):
    for key, tier in lamp_suggestions.items():
        if key in lamp:
            return tier
    return '待确认'

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>待手动确认武将列表</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1300px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #ff9800 0%, #ff5722 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }
        .header h1 { font-size: 24px; margin-bottom: 10px; }
        .header .count { font-size: 14px; opacity: 0.9; }
        .filter-bar { text-align: center; margin: 20px 0; padding: 16px; background: white; border-radius: 8px; }
        .filter-btn { padding: 8px 16px; margin: 5px; border: 2px solid #ff9800; border-radius: 20px; cursor: pointer; background: white; color: #ff9800; font-weight: 500; transition: all 0.2s; }
        .filter-btn:hover { background: #ff9800; color: white; }
        .filter-btn.active { background: #ff9800; color: white; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        th { background: #ff9800; color: white; padding: 12px 16px; text-align: left; font-weight: 500; }
        td { padding: 10px 16px; border-bottom: 1px solid #eee; }
        tr:hover { background: #fff8f0; }
        .input-tier { padding: 6px 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 13px; width: 100px; }
        .row-index { color: #999; font-size: 12px; width: 50px; text-align: center; }
        .general-id { font-family: monospace; color: #666; }
        .reason { color: #888; font-size: 12px; }
        .checkbox { width: 40px; text-align: center; }
        input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
        .footer { text-align: center; padding: 20px; color: #999; font-size: 13px; }
        .action-bar { background: white; padding: 16px; border-radius: 8px; margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
        .action-btn { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; }
        .btn-primary { background: #ff9800; color: white; }
        .btn-success { background: #52c41a; color: white; }
        .btn-secondary { background: #666; color: white; }
        .suggestion-epic { color: #722ed1; font-weight: 500; }
        .suggestion-legend { color: #fa8c16; font-weight: 500; }
        .suggestion-rare { color: #52c41a; font-weight: 500; }
        .suggestion-pending { color: #999; }
        .price { font-family: monospace; color: #1890ff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>待手动确认武将列表</h1>
            <div class="count">共 ''' + str(len(pending)) + ''' 个武将需要确认档位</div>
        </div>

        <div class="filter-bar">
            <span style="margin-right: 20px;">快速定位：</span>
            <button class="filter-btn active" onclick="filterLamp('')">全部</button>
            <button class="filter-btn" onclick="filterLamp('逐鹿')">逐鹿</button>
            <button class="filter-btn" onclick="filterLamp('上兵伐谋')">上兵伐谋</button>
            <button class="filter-btn" onclick="filterLamp('黄巾之乱')">黄巾之乱</button>
            <button class="filter-btn" onclick="filterLamp('锦瑟良缘')">锦瑟良缘</button>
            <button class="filter-btn" onclick="filterLamp('皇家贵胄')">皇家贵胄</button>
            <button class="filter-btn" onclick="filterLamp('往者可谏')">往者可谏</button>
            <button class="filter-btn" onclick="filterLamp('正音雅乐')">正音雅乐</button>
            <button class="filter-btn" onclick="filterLamp('谋')">谋系列</button>
            <button class="filter-btn" onclick="filterLamp('其他')">其他</button>
        </div>

        <table>
            <thead>
                <tr>
                    <th class="row-index">#</th>
                    <th class="checkbox"><input type="checkbox" id="selectAll" onchange="toggleAll(this)"></th>
                    <th>武将ID</th>
                    <th>武将名称</th>
                    <th>LampType</th>
                    <th>原分类依据</th>
                    <th>定价(元)</th>
                    <th>建议档位</th>
                    <th>确认档位</th>
                </tr>
            </thead>
            <tbody>
'''

for i, item in enumerate(pending, 1):
    gid = item['general_id']
    name = item['name']
    lamp = item['lamp_type']
    reason = item['reason']
    price = item.get('item_price')

    suggestion = get_suggestion(lamp)
    suggestion_class = f'suggestion-{suggestion}'
    if suggestion == '传说':
        suggestion_class = 'suggestion-legend'
    elif suggestion == '史诗':
        suggestion_class = 'suggestion-epic'
    elif suggestion == '待确认':
        suggestion_class = 'suggestion-pending'

    price_str = f'{price:,}' if price else '-'

    html += f'''
                <tr data-lamp="{lamp}">
                    <td class="row-index">{i}</td>
                    <td class="checkbox"><input type="checkbox" class="row-checkbox"></td>
                    <td class="general-id">{gid}</td>
                    <td><strong>{name}</strong></td>
                    <td>{lamp}</td>
                    <td class="reason">{reason}</td>
                    <td class="price">{price_str}</td>
                    <td><span class="{suggestion_class}">{suggestion}</span></td>
                    <td><select class="input-tier" onchange="highlight(this)">
                        <option value="">--</option>
                        <option value="限定">限定</option>
                        <option value="传说">传说</option>
                        <option value="史诗">史诗</option>
                        <option value="稀有">稀有</option>
                        <option value="普通">普通</option>
                    </select></td>
                </tr>
'''

html += '''
            </tbody>
        </table>

        <div class="action-bar">
            <button class="action-btn btn-success" onclick="exportSelected()">导出已选择</button>
            <button class="action-btn btn-primary" onclick="exportAll()">导出全部</button>
            <button class="action-btn btn-secondary" onclick="clearAll()">清空选择</button>
            <span style="margin-left: auto; align-self: center; color: #666;">
                已选择 <span id="selectedCount">0</span> 个武将
            </span>
        </div>

        <div class="footer">
            <p>武将品质体系 v4.3 | 疏白 | 2026-06-12</p>
        </div>
    </div>

    <script>
        function filterLamp(lamp) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            const rows = document.querySelectorAll('tbody tr');
            const shownLamps = ['逐鹿', '上兵伐谋', '黄巾之乱', '锦瑟良缘', '皇家贵胄', '往者可谏', '正音雅乐'];
            rows.forEach(row => {
                if (!lamp) {
                    row.style.display = '';
                } else if (lamp === '其他') {
                    row.style.display = shownLamps.some(l => row.dataset.lamp.includes(l)) ? 'none' : '';
                } else if (lamp === '谋') {
                    row.style.display = row.dataset.lamp.includes('谋') ? '' : 'none';
                } else {
                    row.style.display = row.dataset.lamp.includes(lamp) ? '' : 'none';
                }
            });
        }

        function toggleAll(checkbox) {
            document.querySelectorAll('.row-checkbox').forEach(cb => cb.checked = checkbox.checked);
            updateCount();
        }

        function updateCount() {
            const count = document.querySelectorAll('.row-checkbox:checked').length;
            document.getElementById('selectedCount').textContent = count;
        }

        document.querySelectorAll('.row-checkbox').forEach(cb => cb.addEventListener('change', updateCount));

        function highlight(select) {
            if (select.value) {
                select.style.background = '#e8f5e9';
                select.style.borderColor = '#4caf50';
            } else {
                select.style.background = '';
                select.style.borderColor = '#ddd';
            }
        }

        function clearAll() {
            document.querySelectorAll('.row-checkbox').forEach(cb => cb.checked = false);
            document.querySelectorAll('.input-tier').forEach(sel => {
                sel.value = '';
                sel.style.background = '';
                sel.style.borderColor = '#ddd';
            });
            updateCount();
        }

        function exportSelected() {
            const rows = [];
            document.querySelectorAll('.row-checkbox:checked').forEach(cb => {
                const tr = cb.closest('tr');
                const cells = tr.querySelectorAll('td');
                const select = tr.querySelector('select');
                rows.push({
                    id: parseInt(cells[2].textContent.trim()),
                    name: cells[3].textContent.trim(),
                    lamp_type: tr.dataset.lamp,
                    item_price: cells[6].textContent.trim(),
                    tier: select.value || '待手动确认'
                });
            });
            if (rows.length === 0) { alert('请先选择武将'); return; }
            downloadJSON(rows, 'selected_generals.json');
        }

        function exportAll() {
            const rows = [];
            document.querySelectorAll('tbody tr').forEach(tr => {
                const cells = tr.querySelectorAll('td');
                const select = tr.querySelector('select');
                rows.push({
                    id: parseInt(cells[2].textContent.trim()),
                    name: cells[3].textContent.trim(),
                    lamp_type: tr.dataset.lamp,
                    item_price: cells[6].textContent.trim(),
                    tier: select.value || '待手动确认'
                });
            });
            downloadJSON(rows, 'all_pending_generals.json');
        }

        function downloadJSON(data, filename) {
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>'''

with open('武将评级划分/data/待手动确认武将列表.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'已生成: 武将评级划分/data/待手动确认武将列表.html')
print(f'共 {len(pending)} 个武将')