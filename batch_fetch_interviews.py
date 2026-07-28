#!/usr/bin/env python3
"""
批量获取尹正采访文本
"""
import re
import time
import urllib.request
import json
import sys

# 修复Windows控制台编码问题
sys.stdout.reconfigure(encoding='utf-8')

# 待采集的采访列表 (排除已采集的)
interviews = [
    # 2017年
    ("2017", "written-2017-10-17-64bf8e5a"),
    ("2017", "written-2017-10-11-e83f53d0"),
    ("2017", "written-2017-10-6f7b062a"),
    ("2017", "written-2017-10-9e2990a5"),
    ("2017", "written-2017-09-26-e629aa9e"),
    ("2017", "written-2017-06-07-a1c56db8"),
    ("2017", "written-2017-05-07c26bf5"),
    ("2017", "written-2017-05-f0c30ca1"),
    ("2017", "written-2017-02-e9fa15b1"),
    ("2017", "written-2017-01-213f10e6"),
    # 2016年
    ("2016", "written-2016-12-20-15eb6227"),
    ("2016", "written-2016-12-07-d7c49f68"),
    ("2016", "written-2016-12-2ac21670"),
    ("2016", "written-2016-10-28-0e46c9e8"),
    ("2016", "written-2016-10-25-7ee270ff"),
    ("2016", "written-2016-10-24-563a6eea"),
    ("2016", "written-2016-10-23-1d29bdb4"),
    ("2016", "written-2016-09-20-1e2bfc47"),
    ("2016", "written-2016-09-a8fe8516"),
    ("2016", "written-2016-09-44e741be"),
    ("2016", "written-2016-06-6953e0db"),
    ("2016", "written-2016-05-64c17b92"),
    ("2016", "written-2016-05-5dac268b"),
    ("2016", "written-2016-04-22-c9e2dbfb"),
    ("2016", "written-2016-01-a10443fd"),
    # 2015年
    ("2015", "written-2015-12-18-61ab0b20"),
    ("2015", "written-2015-12-d4b51b0e"),
    ("2015", "written-2015-12-ecc8cbb0"),
    ("2015", "written-2015-10-23-cdf1521e"),
    ("2015", "written-2015-10-23-11fac5eb"),
    # 2021年
    ("2021", "written-2021-11-18-778f1447"),
    ("2021", "2021-11-11-5e9e5e64"),
    ("2021", "video-2021-11-13-c244a291"),
    # 2020年
    ("2020", "written-2020-12-30-79f021c9"),
    ("2020", "written-2020-10-18-e909416b"),
    ("2020", "written-2020-08-02-473bdba1"),
    ("2020", "written-2020-06-04-344ee049"),
    ("2020", "written-2020-06-02-1b7a5f8b"),
    ("2020", "written-2020-06-01-7b457057"),
    ("2020", "written-2020-05-20-cefe9e52"),
    ("2020", "written-2020-05-09-f7672153"),
    ("2020", "written-2020-04-30-89036a7a"),
    # 2019年
    ("2019", "written-2019-05-25-7193e2d0"),
    ("2019", "written-2019-05-09-d9214982"),
    ("2019", "written-2019-02-20-f7dd049a"),
    ("2019", "written-2019-02-16-e672bee0"),
    ("2019", "written-2019-01-22-4890a83c"),
    # 2018年
    ("2018", "written-2018-12-09-2e1dfad4"),
    ("2018", "written-2018-10-cdb7f984"),
    ("2018", "written-2018-09-7fabbd5a"),
    ("2018", "written-2018-06-27-ba997c1d"),
    ("2018", "written-2018-01-4c06a936"),
]

def extract_interview(html, year, interview_id):
    """从HTML中提取采访内容"""
    result = {"year": year, "id": interview_id, "content": "", "title": "", "date": "", "source": ""}

    # 提取标题
    title_match = re.search(r'<h1[^>]*class="[^"]*text-2xl[^"]*"[^>]*>([^<]+)</h1>', html)
    if not title_match:
        title_match = re.search(r'"children":"([^"]+)"' , html)

    # 提取body内容 - 从Next.js JSON数据中提取
    body_match = re.search(r'"body":"((?:[^"\\]|\\.)*)"', html)
    if body_match:
        body = body_match.group(1)
        # 处理转义字符
        body = body.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        result["content"] = body

    # 提取日期和来源
    date_match = re.search(r'"(\d{4}-\d{2}-\d{2})"[^,]*"·"[^,]*"([^"]+)"', html)
    if date_match:
        result["date"] = date_match.group(1)
        result["source"] = date_match.group(2)

    return result

def fetch_interview(year, interview_id):
    """获取单个采访"""
    url = f"https://yinzhengfans.com/interviews/{interview_id}"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            return extract_interview(html, year, interview_id)
    except Exception as e:
        print(f"Error fetching {interview_id}: {e}")
        return None

def main():
    results = []
    total = len(interviews)
    current = 0

    print(f"开始采集 {total} 个采访...")

    for year, interview_id in interviews:
        current += 1
        print(f"[{current}/{total}] 获取: {year}/{interview_id}")

        result = fetch_interview(year, interview_id)
        if result and result["content"]:
            results.append(result)
            print(f"  ✓ 成功 (内容长度: {len(result['content'])}字符)")
        else:
            print(f"  ✗ 失败")

        # 避免请求过快
        time.sleep(0.5)

    # 保存结果
    output_file = "yinzheng_interviews_batch2.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 尹正采访文本汇总（第二批）\n\n")
        f.write("> 数据来源：https://yinzhengfans.com/interviews\n")
        f.write("> 采集时间：2026-07-27\n")
        f.write(f"> 本批采集：{len(results)}/{total} 个采访\n\n")
        f.write("---\n\n")

        for r in results:
            f.write(f"## {r['year']}年\n\n")
            f.write(f"### {r['id']}\n")
            f.write(f"- 日期：{r['date']}\n")
            f.write(f"- 来源：{r['source']}\n")
            f.write(f"- URL：https://yinzhengfans.com/interviews/{r['id']}\n\n")
            f.write(r['content'])
            f.write("\n\n---\n\n")

    print(f"\n采集完成！结果保存到: {output_file}")
    print(f"成功: {len(results)}/{total}")

if __name__ == "__main__":
    main()
