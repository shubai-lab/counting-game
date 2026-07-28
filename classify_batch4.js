const fs = require('fs');
const path = require('path');

//读取pkl文件 - 使用pickle模块
try {
    const pickle = require('python-pack');
    console.log('python-pack loaded');
} catch(e) {
    console.log('python-pack not available, trying alternative');
}

// 直接用python执行脚本
const { spawn } = require('child_process');

const pythonScript = `
import pickle
import json
import pandas as pd

# 读取pkl文件
with open('temp_valid_generals_v2.pkl', 'rb') as f:
    df = pickle.load(f)

print('=== 数据结构 ===')
print('列名:', df.columns.tolist())
print('数据形状:', df.shape)
print()

# 筛选406-540的武将
df_batch4 = df[(df['GeneralID'] >= 406) & (df['GeneralID'] <= 540)].copy()
print(f'筛选后武将数量: {len(df_batch4)}')
print()

# 显示前5行的关键字段
print('=== 前5行数据 ===')
for idx, row in df_batch4.head().iterrows():
    print(f"ID: {row['GeneralID']}, Name: {row['Name']}")
    print(f"  LampType: {row['LampType']}")
    print(f"  Price: {row['Price']}")
    print(f"  Ways: {row['Ways']}")
    print(f"  source_ways: {row['source_ways']}")
    print()
`;

const python = spawn('python', ['-c', pythonScript], { cwd: 'C:/Users/zhangfan/my-openspec-project' });

python.stdout.on('data', (data) => {
    console.log(data.toString());
});

python.stderr.on('data', (data) => {
    console.error(data.toString());
});

python.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
});