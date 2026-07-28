// 获取 Confluence Word 导出所需的一切数据
// 通过 spawn 方式避免 execSync 的 shell 参数处理问题
const { spawn } = require('child_process');
const fs = require('fs');

const CDP = '.claude/skills/chrome-cdp-skill/scripts/cdp.mjs';
const TARGET = 'F5E19A9E';

function cdpSpawn(cmd, args) {
  return new Promise((resolve, reject) => {
    const proc = spawn('node', [CDP, cmd, TARGET, ...args], {
      timeout: 30000,
      windowsHide: true
    });
    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', d => stdout += d.toString());
    proc.stderr.on('data', d => stderr += d.toString());
    proc.on('close', code => {
      if (code !== 0) reject(new Error('CDP error: ' + stderr.substring(0, 300)));
      else resolve(stdout);
    });
    proc.on('error', reject);
  });
}

async function main() {
  // 1. 获取 Cookie
  console.log('Getting cookies...');
  const raw = await cdpSpawn('evalraw', ['Network.getAllCookies']);
  const parsed = JSON.parse(raw);
  const cookies = parsed.result?.cookies || [];
  console.log('  Found ' + cookies.length + ' cookies');
  fs.writeFileSync('confluence_cookies.json', JSON.stringify(cookies));

  // 2. 获取页面列表
  console.log('\nScanning page list...');
  const code = `Array.from(document.querySelectorAll('a[href*="pageId="]')).reduce((acc, el) => { const m = el.href.match(/pageId=(\\d+)/); if (m && !acc.seen.has(m[1])) { acc.seen.add(m[1]); acc.list.push({ text: el.textContent.trim().substring(0,80).replace(/[/:*?"<>|]/g,'_'), pageId: m[1] }); } return acc; }, {seen:new Set(),list:[]}).list`;
  const encoded = encodeURIComponent(code);
  const raw2 = await cdpSpawn('eval', [encoded]);
  const pages = JSON.parse(raw2.trim());
  console.log('  Found ' + pages.length + ' pages');
  fs.writeFileSync('page_list.json', JSON.stringify(pages, null, 2));

  // 3. 测试下载
  console.log('\nTest download...');
  const p = pages[0];
  const url = 'http://jira.sanguosha.com:8090/exportword?pageId=' + p.pageId;
  console.log('  ' + p.text + ' -> ' + url);

  // 使用 Node 内置 http 来下载
  const http = require('http');
  const cookieStr = cookies.map(c => c.name + '=' + c.value).join('; ');

  const u = new URL(url);
  const req = http.request({
    hostname: u.hostname,
    port: u.port || 80,
    path: u.pathname + u.search,
    method: 'GET',
    headers: {
      'Cookie': cookieStr,
      'User-Agent': 'Mozilla/5.0',
      'Referer': 'http://jira.sanguosha.com:8090/',
    }
  }, (res) => {
    const chunks = [];
    res.on('data', c => chunks.push(c));
    res.on('end', () => {
      const buf = Buffer.concat(chunks);
      console.log('  HTTP ' + res.statusCode + ' | ' + res.headers['content-type']);
      console.log('  Size: ' + buf.length + ' bytes');
      fs.writeFileSync('test_' + p.text + '.response', buf);
      console.log('  Saved to test_' + p.text + '.response');
    });
  });
  req.on('error', e => console.log('  Error: ' + e.message));
  req.end();
}

main().catch(e => { console.error('FATAL:', e.message); process.exit(1); });
