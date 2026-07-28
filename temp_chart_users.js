const { execSync } = require('child_process');

const data = [
  {time:'3/2',group:'0数据部',value:null},{time:'3/2',group:'1对照组',value:6000},{time:'3/2',group:'2算法',value:null},
  {time:'3/3',group:'0数据部',value:null},{time:'3/3',group:'1对照组',value:6391},{time:'3/3',group:'2算法',value:null},
  {time:'3/4',group:'0数据部',value:null},{time:'3/4',group:'1对照组',value:5541},{time:'3/4',group:'2算法',value:null},
  {time:'3/5',group:'0数据部',value:null},{time:'3/5',group:'1对照组',value:5278},{time:'3/5',group:'2算法',value:null},
  {time:'3/6',group:'0数据部',value:null},{time:'3/6',group:'1对照组',value:5395},{time:'3/6',group:'2算法',value:null},
  {time:'3/7',group:'0数据部',value:null},{time:'3/7',group:'1对照组',value:4911},{time:'3/7',group:'2算法',value:null},
  {time:'3/8',group:'0数据部',value:null},{time:'3/8',group:'1对照组',value:4849},{time:'3/8',group:'2算法',value:null},
  {time:'3/9',group:'0数据部',value:null},{time:'3/9',group:'1对照组',value:4923},{time:'3/9',group:'2算法',value:null},
  {time:'3/10',group:'0数据部',value:null},{time:'3/10',group:'1对照组',value:4586},{time:'3/10',group:'2算法',value:null},
  {time:'3/11',group:'0数据部',value:null},{time:'3/11',group:'1对照组',value:5243},{time:'3/11',group:'2算法',value:null},
  {time:'3/12',group:'0数据部',value:null},{time:'3/12',group:'1对照组',value:4635},{time:'3/12',group:'2算法',value:null},
  {time:'3/13',group:'0数据部',value:null},{time:'3/13',group:'1对照组',value:4667},{time:'3/13',group:'2算法',value:null},
  {time:'3/14',group:'0数据部',value:null},{time:'3/14',group:'1对照组',value:4218},{time:'3/14',group:'2算法',value:null},
  {time:'3/15',group:'0数据部',value:null},{time:'3/15',group:'1对照组',value:4858},{time:'3/15',group:'2算法',value:null},
  {time:'3/16',group:'0数据部',value:null},{time:'3/16',group:'1对照组',value:4506},{time:'3/16',group:'2算法',value:null},
  {time:'3/17',group:'0数据部',value:null},{time:'3/17',group:'1对照组',value:4271},{time:'3/17',group:'2算法',value:null},
  {time:'3/18',group:'0数据部',value:null},{time:'3/18',group:'1对照组',value:4683},{time:'3/18',group:'2算法',value:null},
  {time:'3/19',group:'0数据部',value:null},{time:'3/19',group:'1对照组',value:4383},{time:'3/19',group:'2算法',value:null},
  {time:'3/20',group:'0数据部',value:null},{time:'3/20',group:'1对照组',value:4337},{time:'3/20',group:'2算法',value:null},
  {time:'3/21',group:'0数据部',value:null},{time:'3/21',group:'1对照组',value:4684},{time:'3/21',group:'2算法',value:null},
  {time:'3/22',group:'0数据部',value:null},{time:'3/22',group:'1对照组',value:5127},{time:'3/22',group:'2算法',value:null},
  {time:'3/23',group:'0数据部',value:null},{time:'3/23',group:'1对照组',value:4720},{time:'3/23',group:'2算法',value:null},
  {time:'3/24',group:'0数据部',value:null},{time:'3/24',group:'1对照组',value:3861},{time:'3/24',group:'2算法',value:null},
  {time:'3/25',group:'0数据部',value:null},{time:'3/25',group:'1对照组',value:4324},{time:'3/25',group:'2算法',value:null},
  {time:'3/26',group:'0数据部',value:null},{time:'3/26',group:'1对照组',value:4043},{time:'3/26',group:'2算法',value:null},
  {time:'3/27',group:'0数据部',value:null},{time:'3/27',group:'1对照组',value:4392},{time:'3/27',group:'2算法',value:null},
  {time:'3/28',group:'0数据部',value:null},{time:'3/28',group:'1对照组',value:4329},{time:'3/28',group:'2算法',value:null},
  {time:'3/29',group:'0数据部',value:null},{time:'3/29',group:'1对照组',value:4865},{time:'3/29',group:'2算法',value:null},
  {time:'3/30',group:'0数据部',value:null},{time:'3/30',group:'1对照组',value:4523},{time:'3/30',group:'2算法',value:null},
  {time:'3/31',group:'0数据部',value:null},{time:'3/31',group:'1对照组',value:3964},{time:'3/31',group:'2算法',value:null},
  {time:'4/1',group:'0数据部',value:null},{time:'4/1',group:'1对照组',value:4023},{time:'4/1',group:'2算法',value:null},
  {time:'4/2',group:'0数据部',value:null},{time:'4/2',group:'1对照组',value:3973},{time:'4/2',group:'2算法',value:null},
  {time:'4/3',group:'0数据部',value:2876},{time:'4/3',group:'1对照组',value:3706},{time:'4/3',group:'2算法',value:null},
  {time:'4/4',group:'0数据部',value:3011},{time:'4/4',group:'1对照组',value:3868},{time:'4/4',group:'2算法',value:null},
  {time:'4/5',group:'0数据部',value:3798},{time:'4/5',group:'1对照组',value:4663},{time:'4/5',group:'2算法',value:null},
  {time:'4/6',group:'0数据部',value:3281},{time:'4/6',group:'1对照组',value:4146},{time:'4/6',group:'2算法',value:null},
  {time:'4/7',group:'0数据部',value:2830},{time:'4/7',group:'1对照组',value:3644},{time:'4/7',group:'2算法',value:null},
  {time:'4/8',group:'0数据部',value:2788},{time:'4/8',group:'1对照组',value:3504},{time:'4/8',group:'2算法',value:null},
  {time:'4/9',group:'0数据部',value:2915},{time:'4/9',group:'1对照组',value:3598},{time:'4/9',group:'2算法',value:null},
  {time:'4/10',group:'0数据部',value:17051},{time:'4/10',group:'1对照组',value:3525},{time:'4/10',group:'2算法',value:null},
  {time:'4/11',group:'0数据部',value:19445},{time:'4/11',group:'1对照组',value:4009},{time:'4/11',group:'2算法',value:null},
  {time:'4/12',group:'0数据部',value:23396},{time:'4/12',group:'1对照组',value:4779},{time:'4/12',group:'2算法',value:null},
  {time:'4/13',group:'0数据部',value:22774},{time:'4/13',group:'1对照组',value:4721},{time:'4/13',group:'2算法',value:null},
  {time:'4/14',group:'0数据部',value:19082},{time:'4/14',group:'1对照组',value:3960},{time:'4/14',group:'2算法',value:null},
  {time:'4/15',group:'0数据部',value:15523},{time:'4/15',group:'1对照组',value:3251},{time:'4/15',group:'2算法',value:null},
  {time:'4/16',group:'0数据部',value:13549},{time:'4/16',group:'1对照组',value:2954},{time:'4/16',group:'2算法',value:null},
  {time:'4/17',group:'0数据部',value:15551},{time:'4/17',group:'1对照组',value:2924},{time:'4/17',group:'2算法',value:6153},
  {time:'4/18',group:'0数据部',value:14377},{time:'4/18',group:'1对照组',value:3665},{time:'4/18',group:'2算法',value:7489},
  {time:'4/19',group:'0数据部',value:26986},{time:'4/19',group:'1对照组',value:6783},{time:'4/19',group:'2算法',value:6931},
  {time:'4/20',group:'0数据部',value:37292},{time:'4/20',group:'1对照组',value:9413},{time:'4/20',group:'2算法',value:5669},
  {time:'4/21',group:'0数据部',value:44740},{time:'4/21',group:'1对照组',value:11147},{time:'4/21',group:'2算法',value:5204},
  {time:'4/22',group:'0数据部',value:53606},{time:'4/22',group:'1对照组',value:13205},{time:'4/22',group:'2算法',value:5236},
  {time:'4/23',group:'0数据部',value:30971},{time:'4/23',group:'1对照组',value:7622},{time:'4/23',group:'2算法',value:5042},
  {time:'4/24',group:'0数据部',value:16371},{time:'4/24',group:'1对照组',value:4288},{time:'4/24',group:'2算法',value:5717}
];

const payload = {
  tool: 'generate_line_chart',
  args: {
    data: data,
    title: '预流失各组圈选人数趋势（3/2-4/24）',
    axisXTitle: '日期',
    axisYTitle: '圈选用户数',
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
