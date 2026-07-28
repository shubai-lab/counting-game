// -*- coding: utf-8 -*-
const XLSX = require('xlsx');
const path = require('path');
const fs = require('fs');

const dataDir = path.join(__dirname);
const outputPath = path.join(dataDir, 'treasure_tier_result.json');

console.log('='.repeat(60));
console.log('读取Excel文件...');
console.log('='.repeat(60));

// 读取Excel文件
const generalConf = XLSX.readFile(path.join(dataDir, 'sgs_general_conf.xlsx'));
const itemGeneralConf = XLSX.readFile(path.join(dataDir, 'sgs_item_general_conf.xlsx'));
const priceTable = XLSX.readFile(path.join(dataDir, '新三国杀道具定价表.xlsx'));

// 转换为sheet数据
function sheetToJson(workbook) {
    const sheetName = workbook.SheetNames[0];
    return XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
}

const generals = sheetToJson(generalConf);
const items = sheetToJson(itemGeneralConf);
const prices = sheetToJson(priceTable);

console.log('\n=== sgs_general_conf.xlsx (武将配置表) ===');
console.log('列名:', Object.keys(generals[0] || {}));
console.log('数据量:', generals.length);
console.log('示例数据:', JSON.stringify(generals[0], null, 2));

console.log('\n=== sgs_item_general_conf.xlsx (武将道具表) ===');
console.log('列名:', Object.keys(items[0] || {}));
console.log('数据量:', items.length);
console.log('示例数据:', JSON.stringify(items[0], null, 2));

console.log('\n=== 新三国杀道具定价表.xlsx (道具定价表) ===');
console.log('列名:', Object.keys(prices[0] || {}));
console.log('数据量:', prices.length);
console.log('示例数据:', JSON.stringify(prices[0], null, 2));

// 保存完整数据用于分析
console.log('\n' + '='.repeat(60));
console.log('保存完整数据到 temp_excel_data.json 供进一步分析...');
console.log('='.repeat(60));

const tempData = {
    generals: { columns: Object.keys(generals[0] || {}), count: generals.length, sample: generals.slice(0, 5) },
    items: { columns: Object.keys(items[0] || {}), count: items.length, sample: items.slice(0, 5) },
    prices: { columns: Object.keys(prices[0] || {}), count: prices.length, sample: prices.slice(0, 10) }
};

fs.writeFileSync(path.join(dataDir, 'temp_excel_data.json'), JSON.stringify(tempData, null, 2), 'utf8');
console.log('已保存到 temp_excel_data.json');
