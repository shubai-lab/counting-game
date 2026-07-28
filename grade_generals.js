// 使用pickle解析库读取pkl文件
const { load } = require('pickle');

const fs = require('fs');
const buffer = fs.readFileSync('temp_valid_generals.pkl');

// 尝试解析pickle数据
try {
    const data = load(buffer);
    console.log('Data loaded:', typeof data);
    console.log('Keys:', Object.keys(data));
} catch(e) {
    console.log('Pickle parse failed:', e.message);
    // 尝试直接读取文件内容
    const content = buffer.toString('utf8');
    console.log('File size:', buffer.length);
}