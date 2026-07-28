const xlsx = require('xlsx');
const fs = require('fs');

console.log('='.repeat(60));
console.log('武将品质分类 v3.0 (v2.1分类逻辑 - Node.js版)');
console.log('='.repeat(60));

// 1. 读取主表
const workbook = xlsx.readFile('sgs_general_conf.xlsx');
const sheetName = workbook.SheetNames[0];
const df = xlsx.utils.sheet_to_json(workbook.Sheets[sheetName], {header: 1});

// 跳过前2行(字段描述)，第一行是字段名
const headers = df[1] || [];
const dataRows = df.slice(2).filter(row => row && row[headers.indexOf('GeneralID')] && row[headers.indexOf('LevelTwoGeneralLampType')]);

// 转换为对象数组
const generals = dataRows.map(row => {
    const obj = {};
    headers.forEach((h, i) => obj[h] = row[i]);
    return obj;
}).filter(g => g.GeneralID && g.LevelTwoGeneralLampType);

console.log(`\n主表有效武将数: ${generals.length}`);

// 2. 读取获取途径详情表
const workbook2 = xlsx.readFile('sgs_general_activity_operate_info.xlsx');
const sheetName2 = workbook2.SheetNames[0];
const df2 = xlsx.utils.sheet_to_json(workbook2.SheetNames[0] ? workbook2.Sheets[workbook2.SheetNames[0]] : null, {header: 1});
const headers2 = df2[0] || [];
const operateInfo = df2.slice(1).map(row => {
    const obj = {};
    headers2.forEach((h, i) => obj[h] = row[i]);
    return obj;
});

console.log(`获取途径详情表: ${operateInfo.length}条`);

// 3. 解析获取途径和获取价值
function parseWaysAndValues(text) {
    if (!text) return {};
    const wayMatches = String(text).match(/获取途径[：:](\d+)/g) || [];
    const valueMatches = String(text).match(/获取价值[：:](\d+)/g) || [];
    const result = {};
    wayMatches.forEach((match, i) => {
        const wayId = parseInt(match.match(/\d+/)[0]);
        const valueStr = valueMatches[i];
        const value = valueStr ? parseInt(valueStr.match(/\d+/)[0]) : 0;
        result[wayId] = value;
    });
    return result;
}

// 构建武将数据字典
const generalData = {};
generals.forEach(row => {
    const gid = parseInt(row.GeneralID);
    let wayValue = parseWaysAndValues(row.GetValue);

    // 如果主表没有，从operate_info表获取
    if (Object.keys(wayValue).length === 0) {
        const opRow = operateInfo.find(r => parseInt(r.GeneralID) === gid);
        if (opRow && opRow.ActiveDropWay) {
            wayValue = parseWaysAndValues(opRow.ActiveDropWay);
        }
    }

    generalData[gid] = {
        ways: Object.keys(wayValue).map(Number),
        way_value: wayValue,
        lamp_type: String(row.LevelTwoGeneralLampType || '')
    };
});

const hasWays = Object.values(generalData).filter(g => g.ways.length > 0).length;
console.log(`数据准备完成: 有效武将 ${Object.keys(generalData).length}`);
console.log(`有获取途径的武将: ${hasWays}`);

// 4. 分类函数
function classifyGeneral(generalId, name, lampType, data) {
    const sourceWays = data.ways;
    const wayValue = data.way_value;

    function getPrice(wayId) {
        return wayValue[wayId] || 0;
    }

    // === 优先级1: 武庙/高山仰止/威前缀 → 限定（固定）===
    if (lampType.includes('武庙') || lampType.includes('高山仰止')) {
        return ['限定', `LampType武庙/高山仰止`, 'lamp_type'];
    }

    if (lampType.startsWith('威')) {
        return ['限定', `LampType威前缀(${lampType})`, 'lamp_type'];
    }

    // === 优先级2: 祈福(1004) → 传说（固定）===
    if (sourceWays.includes(1004)) {
        return ['传说', '祈福(1004)', 'operate_info'];
    }

    // === 优先级3: 纳贤(1001)/神将任务(5002) → 史诗（固定）===
    if (sourceWays.includes(1001)) {
        return ['史诗', '纳贤(1001)', 'operate_info'];
    }
    if (sourceWays.includes(5002)) {
        return ['史诗', '神将任务(5002)', 'operate_info'];
    }

    // === 优先级4: 将星招募(2)价格 → 按阈值判断 ===
    // 价格阈值：≥9999传说, 2000~9998史诗, 100~1999稀有, <100普通
    if (sourceWays.includes(2)) {
        const price = getPrice(2);
        if (price >= 9999) {
            return ['传说', `jiangxing_price:${price}`, 'jiangxing'];
        } else if (price >= 2000) {
            return ['史诗', `jiangxing_price:${price}`, 'jiangxing'];
        } else if (price >= 100) {
            return ['稀有', `jiangxing_price:${price}`, 'jiangxing'];
        } else if (price > 0) {
            return ['普通', `jiangxing_price:${price}`, 'jiangxing'];
        }
    }

    // === 优先级5: 宝玉兑换(1101) → 按价格阈值判断 ===
    if (sourceWays.includes(1101)) {
        const price = getPrice(1101);
        if (price >= 10000) {
            return ['史诗', `宝玉兑换(1101)价格:${price}`, 'baoyu'];
        } else if (price >= 1000) {
            return ['稀有', `宝玉兑换(1101)价格:${price}`, 'baoyu'];
        } else {
            return ['普通', `宝玉兑换(1101)价格:${price}`, 'baoyu'];
        }
    }

    // === 优先级6: 珍宝(1003) → 稀有（固定）===
    if (sourceWays.includes(1003)) {
        return ['稀有', '珍宝(1003)', 'zhenbao'];
    }

    // === 优先级7: 普通招募(1) → 普通 ===
    if (sourceWays.includes(1)) {
        return ['普通', '普通招募(1)', 'normal_recruit'];
    }

    // === 优先级8: LampType特殊分类 ===
    if (lampType.includes('无双上将')) {
        return ['史诗', '无双上将', 'lamp_type'];
    }

    if (lampType.includes('界限突破')) {
        return ['稀有', '界限突破', 'lamp_type'];
    }

    // === 优先级9: 待手动确认 ===
    return ['待手动确认', `ways=${JSON.stringify(sourceWays)}`, 'unclassified'];
}

// 5. 执行分类
console.log('\n开始分类...');
const results = [];
generals.forEach(row => {
    const generalId = parseInt(row.GeneralID);
    const namePrefix = row.NamePrefix || '';
    const name = String(namePrefix) + String(row.GeneralName || '');
    const lampType = String(row.LevelTwoGeneralLampType || '');
    const data = generalData[generalId];

    const [tier, reason, source] = classifyGeneral(generalId, name, lampType, data);
    const jiangxingPrice = data.way_value[2] || 0;

    results.push({
        general_id: generalId,
        name: name,
        tier: tier,
        reason: reason,
        source: source,
        jiangxing_price: jiangxingPrice
    });
});

// 6. 统计
const tierCounts = {};
results.forEach(r => {
    tierCounts[r.tier] = (tierCounts[r.tier] || 0) + 1;
});

console.log('\n' + '='.repeat(60));
console.log('分类统计');
console.log('='.repeat(60));
['限定', '传说', '史诗', '稀有', '普通', '待手动确认'].forEach(tier => {
    if (tierCounts[tier]) {
        console.log(`${tier}: ${tierCounts[tier]}`);
    }
});
console.log(`总计: ${results.length}`);

// 7. 待手动确认列表
console.log('\n' + '='.repeat(60));
console.log('待手动确认武将');
console.log('='.repeat(60));
const manual = results.filter(r => r.tier === '待手动确认');
console.log(`共 ${manual.length} 个待手动确认`);
manual.slice(0, 30).forEach(r => {
    console.log(`  ID:${r.general_id} ${r.name} | ${r.reason}`);
});
if (manual.length > 30) {
    console.log(`  ... 还有 ${manual.length - 30} 个`);
}

// 8. 保存结果
const outputPath = 'classification_v3_result.json';
fs.writeFileSync(outputPath, JSON.stringify(results, null, 2), 'utf-8');

console.log(`\n结果已保存到: ${outputPath}`);