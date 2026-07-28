#!/usr/bin/env python3
"""测试提取采访内容"""
import re
import urllib.request

url = "https://yinzhengfans.com/interviews/written-2017-10-17-64bf8e5a"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode('utf-8')

# 提取所有self.__next_f.push内容
matches = re.findall(r'self\.__next_f\.push\(\[1,"([^"]+)"', html)
if matches:
    for m in matches[:3]:
        print("=" * 50)
        # 解码转义
        text = m.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        print(text[:2000])

# 也尝试提取HTML中的正文
print("\n\n=== HTML正文 ===")
body_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if body_match:
    text = re.sub(r'<[^>]+>', '', body_match.group(1))
    print(text.strip()[:2000])
