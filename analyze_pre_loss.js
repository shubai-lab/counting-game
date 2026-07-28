const XLSX = require('xlsx');

const workbook = XLSX.readFile('C:/Users/zhangfan/Downloads/拉活功能分析-预流失干预.xlsx');
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];
const data = XLSX.utils.sheet_to_json(worksheet);

console.log('=== 数据概览 ===');
console.log('行数:', data.length);
console.log('列名:', Object.keys(data[0]));
console.log('\n前5行:');
data.slice(0, 5).forEach((row, i) => console.log(i, JSON.stringify(row)));
console.log('\n是否干预分布:');
const counts = {};
data.forEach(r => { const k = r['是否干预']; counts[k] = (counts[k]||0)+1; });
console.log(counts);

// 按组统计
const groups = {0: [], 1: [], 2: []};
data.forEach(r => {
  const g = r['是否干预'];
  if (groups[g] !== undefined) groups[g].push(r);
});

console.log('\n\n=== 各组数据样本 ===');
Object.keys(groups).forEach(g => {
  console.log(`\n组别 ${g} (${groups[g].length} 行):`);
  groups[g].slice(0, 3).forEach(row => console.log(JSON.stringify(row)));
});

// 找到留存相关的列
const cols = Object.keys(data[0]);
console.log('\n\n所有列名:', cols);

// 尝试识别留存列
const retentionCols = cols.filter(c => c.includes('留') || c.includes('次日') || c.includes('7') || c.includes('3') || c.includes('30'));
console.log('可能的留存列:', retentionCols);

// 输出所有数据用于人工检查
console.log('\n\n=== 完整数据 ===');
data.forEach((row, i) => console.log(i, JSON.stringify(row)));
