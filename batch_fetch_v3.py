#!/usr/bin/env python3
"""
批量获取尹正采访文本 - v3 (剩余采访)
"""
import re
import time
import urllib.request

# 剩余待采集的采访
interviews = [
    # 2018年
    ("2018", "written-2018-01-4c06a936", "尹正：慢下来，享受极速前进"),
    # 2021年
    ("2021", "video-2021-11-13-52248cfd", "现实中是社恐本恐？韩寒最天马行空？"),
    ("2021", "written-2021-10-47d5009c", "披荆斩棘的哥哥 x 时尚芭莎"),
    # 2020年
    ("2020", "video-2020-09-02-48b7ec6a", "最美表演 采访"),
    ("2020", "video-2020-06-03-8abae486", "EMO派 幕后采访"),
    ("2020", "video-2020-05-25-ce33f188", "精美JSTYLE x 尹正 戏里·戏外"),
    ("2020", "video-2020-05-24-aee924d5", "俊仕5月刊 快问快答"),
    ("2020", "video-2020-05-21-2ad4e763", "搜狐时尚采访"),
    ("2020", "written-2020-05-21-4cbe5b45", "尹正 | 享受多样"),
    ("2020", "written-2020-05-04-cd967c31", "专访演员尹正—演戏这件事，多好玩儿啊"),
    ("2020", "written-2020-05-2cdc994a", "尹正 演员的自我修养"),
    # 2019年
    ("2019", "video-2019-06-20-4f68a01f", "头条故事会 | 当旦角儿商细蕊遇上唱生戏"),
    ("2019", "video-2019-05-25-5de0b921", "专访城市应援官尹正：赛车和篮球一样不是一个人的荣耀"),
    ("2019", "video-2019-02-07-bbc967bb", "尹正：内蒙是像根一样的存在"),
    ("2019", "video-2019-02-05-125c6fcd", "Style We x 飞驰人生"),
    ("2019", "video-2019-02-02-d052b31e", "尹正无奈回应撞脸海王"),
    ("2019", "written-2019-02-01-bca9b5cb", "登封Style We 大年初一开启飞驰人生模式"),
    ("2019", "video-2019-02-fdd13d96", "凤凰网idol电话局 | 春节专访"),
    # 2016年
    ("2016", "written-2016-10-23-1d29bdb4", "尹正：有人原谅他，我就及格了"),
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

    print(f"开始采集第三批 {total} 个采访...")

    for year, interview_id, title in interviews:
        current += 1
        result = fetch_and_extract(year, interview_id, title)
        if result and result['content']:
            results.append(result)
            print(f"[{current}/{total}] OK: {interview_id}")
        else:
            print(f"[{current}/{total}] FAIL: {interview_id}")

        time.sleep(0.5)

    # 追加到文件
    if results:
        with open("yinzheng_interviews_batch3.md", 'w', encoding='utf-8') as f:
            f.write("# 尹正采访文本汇总（第三批）\n\n")
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

        print(f"\n完成！结果: yinzheng_interviews_batch3.md")
        print(f"成功: {len(results)}/{total}")

if __name__ == "__main__":
    main()
