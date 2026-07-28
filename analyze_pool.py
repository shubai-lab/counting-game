# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 加载Excel数据
with open('excel_content_utf8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取武将名单
generals = data['content']['武将名单']['data'][2:]  # 跳过标题行

# 按品质分类
by_quality = {}
for row in generals:
    if row[0] and row[2]:  # ID和品质存在
        quality = row[2]
        name = row[1]
        lamp2 = row[6]  # 二级将灯
        price = row[7]  # 将星价格
        if quality not in by_quality:
            by_quality[quality] = []
        by_quality[quality].append({
            'name': name,
            'lamp2': lamp2,
            'price': price
        })

# 网页中的将池武将
web_pools = {
    '祈福SSS': ['司马徽', '兀突骨', '庞德公', '王烈', '沙摩柯', '陆郁生'],
    '限定SSS': ['关索', '赵襄', '鲍三娘', '徐荣', '曹婴', '张琪瑛', '曹纯', '花鬘'],
    '限定(高级)': ['刘宏', '刘永', '张勋', '麴义', '祢衡', '胡金定'],
    '限定(普通)': ['皇甫嵩', '赵昂', '何进', '严夫人', '陆凯', '管辂', '王昶'],
    '活动': ['张让', '王桃', '陈珪', '辛宪英', '黄祖', '韩馥', '王悦', '胡班', '蒲元', '杨仪', '孙鲁育', '邓芝', '田畴', '王荣', '南华老仙', '华歆', '冯熙', '轲比能', '雷铜', '吕玲绮', '陶谦', '朱灵', '雷薄', '王双', '张嫙', '张邈', '吉平', '尹夫人', '刘琦', '潘淑', '曹安民', '刘巴', '王威', '董承', '滕公主', '何晏', '冯方', '穆顺', '张虎', '管亥', '唐姬', '滕胤', '吕旷吕翔', '留赞', '诸葛尚', '杜夫人', '羊祜', '刘辩', '杨婉', '荀谌', '卞喜'],
    'SS': ['黄忠', '邓艾', '郝昭', '虞翻', '步骘', '戏志才', '蒋琬费祎', '魏延', '姜维', '曹植', '伏皇后', '曹昂', 'SP孙尚香', '李傕郭汜', '曹仁', '刘禅', '陈宫', '李儒', '刘协', 'SP蔡文姬', '董白', '小乔', '孙策', '关兴张苞', '张松', '曹节', '李严', '赵忠', '周泰', '张昭张纮', '步练师', '沮授', '董允', '糜竺', '崔琰毛玠', '张角', '蔡文姬', '荀攸', '曹叡', '诸葛瑾', '关银屏', '朱儁', '荀彧', '陆绩', '王异', '钟繇', '李典', '徐氏', '曹丕', '王基', '钟会', '夏侯氏', '刘焉', '吕虔', '贾诩', '许攸', '曹冲', '朱治', '张鲁', '马腾', '鲁肃', '诸葛瞻', '满宠', '郭图逢纪', '秦宓', '孔融', '张郃', '周妃', '刘封', '吴苋', '薛综', '田丰'],
    'S': ['于吉', '王平', '凌统', '陈群', '诸葛诞', 'SP黄月英', '臧霸', '庞统', '孙亮', '徐盛', '吴懿', '严畯', '周鲂', '糜夫人', '卧龙诸葛', '蒯良蒯越', '张春华', '周仓', '司马朗', '贺齐', '陈武董袭', '太史慈', '陈到', '高顺', '孙鲁班', '杜畿', '文聘', '张任', '庞德', '陆抗', '马岱', '朱桓', '孙乾', '吕岱', '曹洪', '颜良文丑', '毌丘俭', '程普', '顾雍', '潘濬', '刘繇', '蒋钦', '袁绍', '袁术', '韩当', '蔡夫人', '郭皇后', '马云騄', '卞夫人', '徐晃', '张绣', '刘表', '曹休', '王粲', '祖茂', '孙坚', '法正', '关平', '刘谌', '蔡邕', '蹋顿', '董卓', '马谡', '简雍', '孙休', 'SP徐庶', '乐进', '祝融', '徐庶', '潘璋马忠', '公孙渊', 'SP庞统', '纪灵', '孟获', '吴国太', '韩浩史涣', '孙登', 'SP姜维', '何太后']
}

# 合并所有网页将池武将
all_web_generals = set()
for pool, names in web_pools.items():
    all_web_generals.update(names)

print("=" * 60)
print("将池武将与品质划分匹配性分析")
print("=" * 60)

# 统计匹配情况
matched = 0
unmatched = []
in_pool_but_wrong_quality = []

for pool_name, pool_generals in web_pools.items():
    print(f"\n【{pool_name}】({len(pool_generals)}人)")
    pool_matched = 0
    pool_unmatched = []

    for name in pool_generals:
        found = False
        for quality, generals_list in by_quality.items():
            for g in generals_list:
                if g['name'] == name:
                    if quality in ['限定', '传说', '史诗', '稀有', '普通']:
                        pool_matched += 1
                        matched += 1
                        found = True
                    else:
                        pool_unmatched.append((name, quality))
                        in_pool_but_wrong_quality.append((name, quality, pool_name))
                    break
            if found:
                break
        if not found:
            unmatched.append(name)

    if pool_unmatched:
        print(f"  匹配异常: {pool_unmatched}")
    print(f"  匹配数: {pool_matched}/{len(pool_generals)}")

print("\n" + "=" * 60)
print("汇总统计")
print("=" * 60)

# 计算总匹配率
total_in_pool = sum(len(v) for v in web_pools.values())
print(f"网页将池总武将数: {total_in_pool}")
print(f"Excel匹配数: {matched}")
print(f"匹配率: {matched/total_in_pool*100:.1f}%")

print(f"\n未匹配武将(Excel中不存在): {unmatched}")
print(f"品质异常武将: {in_pool_but_wrong_quality}")

# 分析各品质在将池中的分布
print("\n" + "=" * 60)
print("各品质在将池中的分布")
print("=" * 60)

quality_in_pool = {'限定': 0, '传说': 0, '史诗': 0, '稀有': 0, '普通': 0}
for pool_name, pool_generals in web_pools.items():
    for name in pool_generals:
        for quality, generals_list in by_quality.items():
            if quality in quality_in_pool:
                for g in generals_list:
                    if g['name'] == name:
                        quality_in_pool[quality] += 1
                        break

for q, count in quality_in_pool.items():
    pct = count / total_in_pool * 100
    print(f"{q}: {count}人 ({pct:.1f}%)")
