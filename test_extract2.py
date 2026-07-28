#!/usr/bin/env python3
"""测试提取采访内容 - 改进版"""
import re
import urllib.request

url = "https://yinzhengfans.com/interviews/written-2017-10-17-64bf8e5a"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode('utf-8')

# 方法1: 提取HTML中的article标签内容
print("=== 方法1: article标签 ===")
article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if article_match:
    text = re.sub(r'<[^>]+>', '', article_match.group(1))
    print(text.strip()[:1000])

# 方法2: 提取Next.js的__NEXT_DATA__
print("\n\n=== 方法2: __NEXT_DATA__ ===")
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
if next_data_match:
    import json
    data = json.loads(next_data_match.group(1))
    body = data.get('props', {}).get('pageProps', {}).get('interview', {}).get('body', '')
    print(body[:1000])

# 方法3: 直接搜索正文关键词
print("\n\n=== 方法3: 搜索正文 ===")
if '尹正' in html:
    idx = html.find('尹正')
    print(html[idx:idx+500])
