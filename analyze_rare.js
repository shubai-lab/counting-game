const XLSX = require('xlsx');
const workbook = XLSX.readFile('C:/Users/zhangfan/Desktop/武将品质划分_v21.xlsx');
const sheetName = workbook.SheetNames[0];
const data = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
console.log('Columns:', Object.keys(data[0]));
console.log('Total rows:', data.length);

// Filter rare generals
const rare = data.filter(row => row['品质'] === '稀有');
console.log('稀有数量:', rare.length);
console.log();

// Check each rare general
const issues = [];
console.log('=== 所有稀有武将 ===');
rare.forEach(row => {
    const 将星 = row['将星价格'];
    const 界限 = row['界限突破'];
    const name = row['武将名称'];
    console.log(name + ' - 将星:' + 将星 + ' - 界限突破:' + 界限);

    // Check if it meets rare criteria (将星100-1499 or 界限突破)
    const 将星数值 = parseInt(将星) || 0;
    const isRare = (将星数值 >= 100 && 将星数值 <= 1499) || 界限 === '界限突破';
    if (!isRare) {
        issues.push(name + ' (将星:' + 将星 + ', 界限:' + 界限 + ')');
    }
});

console.log();
console.log('=== 误判为稀有的武将 ===');
if (issues.length === 0) {
    console.log('无');
} else {
    issues.forEach(i => console.log(i));
}
