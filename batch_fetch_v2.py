#!/usr/bin/env python3
"""
批量获取尹正采访文本 - v2
"""
import re
import time
import urllib.request
import json
import sys

# 待采集的采访列表
interviews = [
    # 2017年
    ("2017", "written-2017-10-17-64bf8e5a", "尹正专访：特想演农民、东厂大太监还有爸爸"),
    ("2017", "written-2017-10-11-e83f53d0", "专访 | 一剪梅boy变身话痨唐僧后，还想演东厂大太监……"),
    ("2017", "written-2017-10-6f7b062a", "尹正 在角色中看自己"),
    ("2017", "written-2017-10-9e2990a5", "尹正 戏中人"),
    ("2017", "written-2017-09-26-e629aa9e", "大话西游之爱你一万年 唐僧饰演者尹正采访提问"),
    ("2017", "written-2017-06-07-a1c56db8", "COVER STORY-HOMMES | 尹正：一个宅男的自我修养"),
    ("2017", "written-2017-05-07c26bf5", "尹正 永葆初心的成长与蜕变"),
    ("2017", "written-2017-05-f0c30ca1", "尹正 演戏就像谈恋爱"),
    ("2017", "written-2017-02-e9fa15b1", "情人节别册：认真踏实的二次元宅男"),
    ("2017", "written-2017-01-213f10e6", "尹人注目 正在当红"),
    # 2016年
    ("2016", "written-2016-12-20-15eb6227", "专访尹正：没有刻意要演喜剧 演员是儿时梦想"),
    ("2016", "written-2016-12-07-d7c49f68", "专访尹正：真诚的反面角色不怕遭人恨"),
    ("2016", "written-2016-12-2ac21670", "尹正 自带BGM的演员"),
    ("2016", "written-2016-10-28-0e46c9e8", "专访尹正:我演反派太多 是反派版吴彦祖"),
    ("2016", "written-2016-10-25-7ee270ff", "尹正：有张鲁一、王劲松在，我算不上演技担当"),
    ("2016", "written-2016-10-24-563a6eea", "尹正 会唱歌的苏三省是个机车控"),
    ("2016", "written-2016-10-23-1d29bdb4", "尹正：有人原谅他，我就及格了"),
    ("2016", "written-2016-09-20-1e2bfc47", "独家【先生】尹正 | 痞子少侠"),
    ("2016", "written-2016-09-a8fe8516", "尹正 唱而优则演 演而优则精"),
    ("2016", "written-2016-09-44e741be", "演员尹正 追求生活的另一种可能"),
    ("2016", "written-2016-06-6953e0db", "尹正 爱嘻哈的耿直Boy"),
    ("2016", "written-2016-05-64c17b92", "尹正 酷与逗切换无违和"),
    ("2016", "written-2016-05-5dac268b", "想遇到一个高情商女孩，好好相爱"),
    ("2016", "written-2016-04-22-c9e2dbfb", "专访尹正：我是一个单性思维的动物"),
    ("2016", "written-2016-01-a10443fd", "麻雀 主创论剧"),
    # 2015年
    ("2015", "written-2015-12-18-61ab0b20", "我很闷骚天天想着上电视"),
    ("2015", "written-2015-12-d4b51b0e", "独家专访尹正：曾经拿着一张试香纸跑遍所有香水柜台"),
    ("2015", "written-2015-12-ecc8cbb0", "我不是男神，只是一个热爱演戏的演员"),
    ("2015", "written-2015-10-23-cdf1521e", "尹正：傅子遇和薄靳言是海尔兄弟"),
    ("2015", "written-2015-10-23-11fac5eb", "尹正：现在听到《一剪梅》还是发怵"),
    # 2021年
    ("2021", "written-2021-11-18-778f1447", "独家专访尹正：在那个年代，想扬名立万的这帮人应该是存在的"),
    ("2021", "2021-11-11-5e9e5e64", "昨天我们围堵尹正，就为了扬名立万"),
    # 2020年
    ("2020", "written-2020-12-30-79f021c9", "正在通话中 4.0"),
    ("2020", "written-2020-10-18-e909416b", "爱过、做过、才算真正活过"),
    ("2020", "written-2020-08-02-473bdba1", "尹正：我的快乐从没变过"),
    ("2020", "written-2020-06-04-344ee049", "100个有品位的人"),
    ("2020", "written-2020-06-02-1b7a5f8b", "EMO派x尹正 | 等一场等待"),
    ("2020", "written-2020-06-01-7b457057", "尹正 | 每一个角色都自有其命"),
    ("2020", "written-2020-05-20-cefe9e52", "封面故事 | 尹正：七步成戏"),
    ("2020", "written-2020-05-09-f7672153", "戏痴尹正专访"),
    ("2020", "written-2020-04-30-89036a7a", "尹正 我亦痴心人"),
    # 2019年
    ("2019", "written-2019-05-25-7193e2d0", "画框外的人生 | 被演戏耽误的赛车手尹正"),
    ("2019", "written-2019-05-09-d9214982", "尹正 演员加赛车手已经是我的人生巅峰了"),
    ("2019", "written-2019-02-20-f7dd049a", "正在通话中 2.0"),
    ("2019", "written-2019-02-16-e672bee0", "热血少年尹正：我的忍道就是永不放弃"),
    ("2019", "written-2019-01-22-4890a83c", "尹正：沈腾爱漂移 韩寒脾气好"),
    # 2018年
    ("2018", "written-2018-12-09-2e1dfad4", "正在通话中 1.0"),
    ("2018", "written-2018-10-cdb7f984", "尹正 「非科班」演员的春天"),
    ("2018", "written-2018-09-7fabbd5a", "尹正 演戏，每天都是上班第一天"),
    ("2018", "written-2018-06-27-ba997c1d", "尹正 | 天生的戏疯子"),
    ("2018", "written-2018-01-4c06a936", "尹正：慢下来，享受极速前进"),
]

def fetch_and_extract(year, interview_id, title):
    """获取并提取采访内容"""
    url = f"https://yinzhengfans.com/interviews/{interview_id}"

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')

        # 提取article标签内容
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if article_match:
            text = re.sub(r'<[^>]+>', '', article_match.group(1))
            # 清理多余空白
            text = re.sub(r'\n\s*\n', '\n\n', text.strip())
            return {
                'year': year,
                'id': interview_id,
                'title': title,
                'content': text,
                'url': url
            }
        return None

    except Exception as e:
        return None

def main():
    results = []
    total = len(interviews)
    current = 0

    print(f"开始采集 {total} 个采访...")

    for year, interview_id, title in interviews:
        current += 1
        result = fetch_and_extract(year, interview_id, title)
        if result and result['content']:
            results.append(result)
            print(f"[{current}/{total}] OK: {interview_id} ({len(result['content'])}字符)")
        else:
            print(f"[{current}/{total}] FAIL: {interview_id}")

        time.sleep(0.5)

    # 写入文件
    output_file = "yinzheng_interviews_batch2.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 尹正采访文本汇总（第二批）\n\n")
        f.write("> 数据来源：https://yinzhengfans.com/interviews\n")
        f.write("> 采集时间：2026-07-27\n")
        f.write(f"> 本批采集：{len(results)}/{total} 个采访\n\n")
        f.write("---\n\n")

        for r in results:
            f.write(f"## {r['year']}年\n\n")
            f.write(f"### {r['title']}\n")
            f.write(f"- URL：{r['url']}\n\n")
            f.write(r['content'])
            f.write("\n\n---\n\n")

    print(f"\n完成！结果: {output_file}")
    print(f"成功: {len(results)}/{total}")

if __name__ == "__main__":
    main()
