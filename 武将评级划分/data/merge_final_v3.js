// 武将分类最终合并脚本 v3
// 优先级：LampType特殊分类 > 珍宝价格分类 > 主要分类

const fs = require('fs');

console.log('='.repeat(60));
console.log('武将品质最终合并 v3');
console.log('='.repeat(60));

// 读取主要分类（将星价格分类）
const v3Data = JSON.parse(fs.readFileSync('classification_v3_result.json', 'utf-8'));
console.log(`\n主要分类(将星价格): ${v3Data.length} 个武将`);

// 读取珍宝价格分类
const final5Data = JSON.parse(fs.readFileSync('classification_final5_result.json', 'utf-8'));
console.log(`珍宝价格分类: ${final5Data.length} 个武将`);

// 构建珍宝价格字典
const priceFromFinal5 = {};
final5Data.forEach(g => {
    priceFromFinal5[g.general_id] = {
        tier: g.tier,
        reason: g.reason,
        source: g.source
    };
});

// 构建主要分类字典（按将星价格）
const mainClassification = {};
v3Data.forEach(g => {
    mainClassification[g.general_id] = {
        tier: g.tier,
        reason: g.reason,
        source: g.source
    };
});

// 统计各档位
function countTiers(data) {
    const counts = {};
    data.forEach(g => {
        const tier = g.tier || '未知';
        counts[tier] = (counts[tier] || 0) + 1;
    });
    return counts;
}

console.log('\n主要分类档位分布:', JSON.stringify(countTiers(v3Data)));
console.log('珍宝价格分类档位分布:', JSON.stringify(countTiers(final5Data)));

// 合并逻辑
// 优先级：主要分类（LampType特殊分类已经在v3中处理）> 珍宝价格分类

// 步骤1：使用主要分类作为基础
const merged = {};

// 步骤2：将主要分类结果加入
v3Data.forEach(g => {
    merged[g.general_id] = {
        general_id: g.general_id,
        name: g.name,
        tier: g.tier,
        reason: g.reason,
        source: g.source
    };
});

// 步骤3：用珍宝价格分类填充"待手动确认"的武将
let filledCount = 0;
Object.keys(merged).forEach(gid => {
    if (merged[gid].tier === '待手动确认') {
        const priceData = priceFromFinal5[parseInt(gid)];
        if (priceData && priceData.tier !== '待手动确认') {
            merged[gid].tier = priceData.tier;
            merged[gid].reason = priceData.reason + ' (珍宝价格补充)';
            merged[gid].source = 'price_filled';
            filledCount++;
        }
    }
});

console.log(`\n珍宝价格补充武将数: ${filledCount}`);

// 转成数组
const mergedArray = Object.values(merged);

// 排序
mergedArray.sort((a, b) => a.general_id - b.general_id);

// 统计最终结果
const finalCounts = countTiers(mergedArray);

console.log('\n' + '='.repeat(60));
console.log('最终分类结果');
console.log('='.repeat(60));

const tierOrder = ['限定', '传说', '史诗', '稀有', '普通', '待手动确认'];
let total = 0;
tierOrder.forEach(tier => {
    if (finalCounts[tier]) {
        console.log(`${tier}: ${finalCounts[tier]}`);
        total += finalCounts[tier];
    }
});
console.log(`总计: ${total}`);

// 显示待手动确认武将
const manualList = mergedArray.filter(g => g.tier === '待手动确认');
if (manualList.length > 0) {
    console.log('\n待手动确认武将:');
    manualList.slice(0, 30).forEach(g => {
        console.log(`  ID:${g.general_id} ${g.name} | ${g.reason}`);
    });
    if (manualList.length > 30) {
        console.log(`  ... 还有 ${manualList.length - 30} 个`);
    }
}

// 保存结果
const outputPath = 'classification_final_v3_result.json';
fs.writeFileSync(outputPath, JSON.stringify(mergedArray, null, 2), 'utf-8');
console.log(`\n结果已保存到: ${outputPath}`);