#!/bin/bash
# 批量获取尹正采访文本

# 待采集的采访列表
declare -a interviews=(
  # 2017年
  "written-2017-10-17-64bf8e5a"
  "written-2017-10-11-e83f53d0"
  "written-2017-10-6f7b062a"
  "written-2017-10-9e2990a5"
  "written-2017-09-26-e629aa9e"
  "written-2017-06-07-a1c56db8"
  "written-2017-05-07c26bf5"
  "written-2017-05-f0c30ca1"
  "written-2017-02-e9fa15b1"
  "written-2017-01-213f10e6"
  # 2016年
  "written-2016-12-20-15eb6227"
  "written-2016-12-07-d7c49f68"
  "written-2016-12-2ac21670"
  "written-2016-10-28-0e46c9e8"
  "written-2016-10-25-7ee270ff"
  "written-2016-10-24-563a6eea"
  "written-2016-10-23-1d29bdb4"
  "written-2016-09-20-1e2bfc47"
  "written-2016-09-a8fe8516"
  "written-2016-09-44e741be"
  "written-2016-06-6953e0db"
  "written-2016-05-64c17b92"
  "written-2016-05-5dac268b"
  "written-2016-04-22-c9e2dbfb"
  "written-2016-01-a10443fd"
  # 2015年
  "written-2015-12-18-61ab0b20"
  "written-2015-12-d4b51b0e"
  "written-2015-12-ecc8cbb0"
  "written-2015-10-23-cdf1521e"
  "written-2015-10-23-11fac5eb"
  # 2021年
  "written-2021-11-18-778f1447"
  "2021-11-11-5e9e5e64"
  "video-2021-11-13-c244a291"
  # 2020年
  "written-2020-12-30-79f021c9"
  "written-2020-10-18-e909416b"
  "written-2020-08-02-473bdba1"
  "written-2020-06-04-344ee049"
  "written-2020-06-02-1b7a5f8b"
  "written-2020-06-01-7b457057"
  "written-2020-05-20-cefe9e52"
  "written-2020-05-09-f7672153"
  "written-2020-04-30-89036a7a"
  # 2019年
  "written-2019-05-25-7193e2d0"
  "written-2019-05-09-d9214982"
  "written-2019-02-20-f7dd049a"
  "written-2019-02-16-e672bee0"
  "written-2019-01-22-4890a83c"
  # 2018年
  "written-2018-12-09-2e1dfad4"
  "written-2018-10-cdb7f984"
  "written-2018-09-7fabbd5a"
  "written-2018-06-27-ba997c1d"
  "written-2018-01-4c06a936"
)

echo "开始采集 ${#interviews[@]} 个采访..."

for id in "${interviews[@]}"; do
  echo "获取: $id"
  url="https://yinzhengfans.com/interviews/$id"

  # 获取页面并提取body内容
  content=$(curl -s "$url" | grep -o '"body":"[^"]*"' | head -1 | sed 's/"body":"//;s/\\n/\n/g;s/\\"/"/g;s/"$//')

  if [ -n "$content" ]; then
    echo "$content"
    echo "---"
  else
    echo "无法获取: $id"
  fi

  # 避免请求过快
  sleep 1
done
