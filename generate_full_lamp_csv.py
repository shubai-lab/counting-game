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

# 按将灯分组计算系统需补
lamp_groups = {}
for g in generals:
    lamp = g.get('lamp_type', '未知')
    if lamp not in lamp_groups:
        lamp_groups[lamp] = []
    lamp_groups[lamp].append(g)

# 计算每个将灯的系统需补（总额）
lamp_system_need = {}
for lamp, generals_list in lamp_groups.items():
    lamp_points = lamp_points_config.get(lamp, 0)
    old_sum = sum(g.get('old_points', 0) for g in generals_list)
    new_sum = sum(tier_new_points.get(g.get('tier', '普通'), 100) for g in generals_list)
    count = len(generals_list)
    system_need = new_sum - (old_sum + lamp_points)
    lamp_system_need[lamp] = {
        'system_need': system_need,
        'count': count,
        'lamp_points': lamp_points,
    }

# 生成CSV
results = []
total_system_need = 0

for g in generals:
    lamp = g.get('lamp_type', '未知')
    name = g.get('name', '')
    tier = g.get('tier', '普通')
    old_general_points = g.get('old_points', 0)  # 武将原来帅点
    old_lamp_points = lamp_points_config.get(lamp, 0)  # 将灯原来的帅点
    new_general_points = tier_new_points.get(tier, 100)  # 武将新的帅点

    lamp_info = lamp_system_need.get(lamp, {'system_need': 0, 'count': 1, 'lamp_points': 0})
    system_need_total = lamp_info['system_need']
    count = lamp_info['count']

    # 将灯新的帅点 = 原武将帅点 + 原将灯帅点 - 新武将帅点
    new_lamp_points = old_general_points + old_lamp_points - new_general_points

    # 系统需要补充的帅点（按人头分摊）
    if count > 0:
        system_need_per = round(system_need_total / count, 2)
    else:
        system_need_per = 0

    total_system_need += system_need_per

    results.append({
        '将灯名': lamp,
        '武将名': name,
        '武将原来帅点': old_general_points,
        '将灯原来的帅点': old_lamp_points,
        '武将新的帅点': new_general_points,
        '将灯新的帅点': new_lamp_points,
        '系统需要补充的帅点': system_need_per,
    })

# 按将灯名排序
results.sort(key=lambda x: (x['将灯名'], x['武将名']))

# 输出CSV
output_path = '将灯帅点明细_完整版.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        '将灯名', '武将名', '武将原来帅点', '将灯原来的帅点',
        '武将新的帅点', '将灯新的帅点', '系统需要补充的帅点'
    ])
    writer.writeheader()
    writer.writerows(results)

print(f'CSV已生成: {output_path}')
print(f'武将总数: {len(results)}')
print(f'系统需补充总帅点: {total_system_need:.2f}')

# 显示需要系统补充的将灯汇总
print('\n=== 需要系统补充帅点的将灯 ===')
need补充_lamps = set()
for r in results:
    if r['系统需要补充的帅点'] > 0:
        need补充_lamps.add(r['将灯名'])

for lamp in sorted(need补充_lamps):
    lamp_results = [r for r in results if r['将灯名'] == lamp]
    total = sum(r['系统需要补充的帅点'] for r in lamp_results)
    print(f'{lamp}: {len(lamp_results)}个武将, 系统需补={total:.2f}')