/**
 * 批量获取尹正采访内容
 * 使用Chrome CDP获取所有采访页面文本
 */

const https = require('https');
const http = require('http');

// 完整的采访URL列表
const interviews = [
  // 2026
  "written-2026-02-18-ace76fcb",
  "video-2026-01-07-7384b245",
  // 2025
  "video-2025-12-30-33e75859",
  "video-2025-12-30-5dab340a",
  "video-2025-12-30-b3710399",
  "written-2025-12-30-9f5e12df",
  "video-2025-12-27-7b79a7bd",
  "video-2025-12-b1d3723f",
  "video-2025-12-02d90de8",
  "video-2025-05-23-840981ad",
  "video-2025-01-11-f85eba8a",
  // 2024
  "written-2024-12-30-61a93c28",
  "written-2024-02-11-21e74838",
  // 2023
  "written-2023-12-30-68f40ba3",
  "2023-12-13-a8262571",
  // 2022
  "written-2022-12-30-90f5278d",
  "2022-01-31-8cee0940",
  // 2021
  "written-2021-12-30-2bad19f4",
  "written-2021-11-18-778f1447",
  "video-2021-11-13-52248cfd",
  "video-2021-11-13-c244a291",
  "2021-11-11-5e9e5e64",
  "written-2021-10-47d5009c",
  // 2020
  "written-2020-12-30-79f021c9",
  "written-2020-10-18-e909416b",
  "video-2020-09-02-48b7ec6a",
  "written-2020-08-02-473bdba1",
  "written-2020-06-04-344ee049",
  "video-2020-06-03-8abae486",
  "written-2020-06-02-1b7a5f8b",
  "written-2020-06-01-7b457057",
  "video-2020-05-25-ce33f188",
  "video-2020-05-24-aee924d5",
  "video-2020-05-21-2ad4e763",
  "written-2020-05-21-4cbe5b45",
  "written-2020-05-20-cefe9e52",
  "written-2020-05-09-f7672153",
  "written-2020-05-04-cd967c31",
  "written-2020-05-2cdc994a",
  "written-2020-04-30-89036a7a",
  // 2019
  "video-2019-06-20-4f68a01f",
  "video-2019-05-25-5de0b921",
  "written-2019-05-25-7193e2d0",
  "written-2019-05-09-d9214982",
  "written-2019-02-20-f7dd049a",
  "written-2019-02-16-e672bee0",
  "video-2019-02-07-bbc967bb",
  "video-2019-02-05-125c6fcd",
  "video-2019-02-02-d052b31e",
  "written-2019-02-01-bca9b5cb",
  "video-2019-02-fdd13d96",
  "written-2019-01-22-4890a83c",
  // 2018
  "written-2018-12-09-2e1dfad4",
  "written-2018-10-cdb7f984",
  "written-2018-09-7fabbd5a",
  "written-2018-06-27-ba997c1d",
  "written-2018-01-4c06b936",
  // 2017
  "written-2017-10-17-64bf8e5a",
  "written-2017-10-11-e83f53d0",
  "written-2017-10-6f7b062a",
  "written-2017-10-9e2990a5",
  "written-2017-09-26-e629aa9e",
  "written-2017-06-07-a1c56db8",
  "written-2017-05-07c26bf5",
  "written-2017-05-f0c30ca1",
  "written-2017-02-e9fa15b1",
  "written-2017-01-213f10e6",
  // 2016
  "written-2016-12-20-15eb6227",
  "written-2016-12-07-d7c49f68",
  "written-2016-12-2ac21670",
  "written-2016-10-28-0e46c9e8",
  "written-2016-10-25-7ee270ff",
  "written-2016-10-24-563a6eea",
  "written-2016-10-23-1d29bdb4",
  "written-2016-09-20-1e2bfc47",
  "written-2016-09-a8fe8516",
  "written-2016-09-44e741be",
  "written-2016-06-6953e0db",
  "written-2016-05-64c17b92",
  "written-2016-05-5dac268b",
  "written-2016-04-22-c9e2dbfb",
  "written-2016-01-a10443fd",
  // 2015
  "written-2015-12-18-61ab0b20",
  "written-2015-12-d4b51b0e",
  "written-2015-12-ecc8cbb0",
  "written-2015-10-23-cdf1521e",
  "written-2015-10-23-11fac5eb",
  "written-2015-10-09-10c35198",
];

console.log(`总共 ${interviews.length} 个采访URL`);
console.log(JSON.stringify(interviews.map(id => `https://yinzhengfans.com/interviews/${id}`)));
