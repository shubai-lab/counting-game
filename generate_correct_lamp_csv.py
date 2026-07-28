# -*- coding: utf-8 -*-
import json
import csv
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取分类结果
with open('武将评级划分/data/classification_final_v5_result.json', 'r', encoding='utf-8') as f:
    generals = json.load(f)

print(f'武将总数: {len(generals)}')

# 将灯帅点配置（从sgs_general_lamp_conf.xlsx读取的真实数据）
# 格式：将灯名 -> 将灯帅点
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
    '限定': 800,  # 武庙/高山仰止
}

# 按将灯分组
lamp_groups = {}
for g in generals:
    lamp = g.get('lamp_type', '未知')
    if lamp not in lamp_groups:
        lamp_groups[lamp] = []
    lamp_groups[lamp].append(g)

# 计算每个将灯的系统需补
results = []
total_system_need = 0

for lamp, generals_list in sorted(lamp_groups.items(), key=lambda x: -len(x[1])):
    lamp_points = lamp_points_config.get(lamp, 0)
    old_sum = sum(g.get('old_points', 0) for g in generals_list)
    new_sum = sum(tier_new_points.get(g.get('tier', '普通'), 100) for g in generals_list)
    count = len(generals_list)

    # 公式：系统需补 = 新武将帅点总和 - (原武将帅点总和 + 真实将灯帅点)
    system_need = new_sum - (old_sum + lamp_points)

    total_system_need += system_need

    print(f'{lamp}: {count}个武将, 原帅点={old_sum}, 新帅点={new_sum}, 将灯帅点={lamp_points}, 系统需补={system_need}')

    for g in generals_list:
        tier = g.get('tier', '普通')
        new_points = tier_new_points.get(tier, 100)
        old_points = g.get('old_points', 0)
        results.append({
            'lamp': lamp,
            'name': g.get('name', ''),
            'old_points': old_points,
            'lamp_points': lamp_points,
            'new_points': new_points,
            'tier': tier,
        })

print(f'\n系统需补充总帅点: {total_system_need}')

# 生成CSV
with open('将灯帅点明细_修正版.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['lamp', 'name', 'old_points', 'lamp_points', 'new_points', 'tier'])
    writer.writeheader()
    writer.writerows(results)

print('\nCSV已生成: 将灯帅点明细_修正版.csv')