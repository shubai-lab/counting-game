const { execSync } = require('child_process');

const data = [
  {time:'4/4',group:'0数据部',value:47},{time:'4/4',group:'1对照组',value:302},{time:'4/4',group:'2算法',value:null},
  {time:'4/5',group:'0数据部',value:86},{time:'4/5',group:'1对照组',value:416},{time:'4/5',group:'2算法',value:null},
  {time:'4/6',group:'0数据部',value:126},{time:'4/6',group:'1对照组',value:523},{time:'4/6',group:'2算法',value:null},
  {time:'4/7',group:'0数据部',value:109},{time:'4/7',group:'1对照组',value:541},{time:'4/7',group:'2算法',value:null},
  {time:'4/8',group:'0数据部',value:133},{time:'4/8',group:'1对照组',value:522},{time:'4/8',group:'2算法',value:null},
  {time:'4/9',group:'0数据部',value:149},{time:'4/9',group:'1对照组',value:548},{time:'4/9',group:'2算法',value:null},
  {time:'4/10',group:'0数据部',value:2519},{time:'4/10',group:'1对照组',value:605},{time:'4/10',group:'2算法',value:null},
  {time:'4/11',group:'0数据部',value:2737},{time:'4/11',group:'1对照组',value:630},{time:'4/11',group:'2算法',value:null},
  {time:'4/12',group:'0数据部',value:2732},{time:'4/12',group:'1对照组',value:605},{time:'4/12',group:'2算法',value:null},
  {time:'4/13',group:'0数据部',value:2756},{time:'4/13',group:'1对照组',value:674},{time:'4/13',group:'2算法',value:null},
  {time:'4/14',group:'0数据部',value:2976},{time:'4/14',group:'1对照组',value:665},{time:'4/14',group:'2算法',value:null},
  {time:'4/15',group:'0数据部',value:2202},{time:'4/15',group:'1对照组',value:540},{time:'4/15',group:'2算法',value:null},
  {time:'4/16',group:'0数据部',value:2167},{time:'4/16',group:'1对照组',value:272},{time:'4/16',group:'2算法',value:null},
  {time:'4/17',group:'0数据部',value:2496},{time:'4/17',group:'1对照组',value:264},{time:'4/17',group:'2算法',value:2421},
  {time:'4/18',group:'0数据部',value:2375},{time:'4/18',group:'1对照组',value:631},{time:'4/18',group:'2算法',value:2618},
  {time:'4/19',group:'0数据部',value:3037},{time:'4/19',group:'1对照组',value:761},{time:'4/19',group:'2算法',value:2177},
  {time:'4/20',group:'0数据部',value:3034},{time:'4/20',group:'1对照组',value:749},{time:'4/20',group:'2算法',value:1354},
  {time:'4/21',group:'0数据部',value:2981},{time:'4/21',group:'1对照组',value:753},{time:'4/21',group:'2算法',value:1172},
  {time:'4/22',group:'0数据部',value:2748},{time:'4/22',group:'1对照组',value:668},{time:'4/22',group:'2算法',value:982},
  {time:'4/23',group:'0数据部',value:1837},{time:'4/23',group:'1对照组',value:471},{time:'4/23',group:'2算法',value:733}
];

const payload = {
  tool: 'generate_line_chart',
  args: {
    data: data,
    title: '预流失各组登录用户数趋势（4/4-4/23）',
    axisXTitle: '日期',
    axisYTitle: '登录用户数',
    width: 1200,
    height: 500,
    style: { palette: ['#E67E22', '#3498DB', '#2ECC71'], lineWidth: 2 },
    theme: 'default'
  }
};

const specPath = 'c:/Users/zhangfan/my-openspec-project/temp_spec.json';
require('fs').writeFileSync(specPath, JSON.stringify(payload));
const result = execSync('node c:/Users/zhangfan/my-openspec-project/.claude/skills/chart-visualization/scripts/generate.js ' + specPath, {encoding:'utf8'});
console.log(result);
