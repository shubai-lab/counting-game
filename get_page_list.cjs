const { spawn } = require('child_process');
const CDP = '.claude/skills/chrome-cdp-skill/scripts/cdp.mjs';
const TARGET = 'C309766D';
const fs = require('fs');

// Get pageId + text together
const code = `JSON.stringify([...document.links].filter(a=>a.href.includes('pageId=')).reduce((acc,a)=>{const m=a.href.match(/pageId=(\\d+)/);if(m&&!acc.s.has(m[1])){acc.s.add(m[1]);acc.l.push({pageId:m[1],text:a.textContent.trim().substring(0,80).replace(/[/:*?"<>|]/g,'_')})}return acc},{s:new Set(),l:[]}).l)`;

const proc = spawn('node', [CDP, 'eval', TARGET, code], {
  timeout: 30000,
  windowsHide: true,
  stdio: ['ignore', 'pipe', 'pipe']
});

let stdout = '';
let stderr = '';
proc.stdout.on('data', d => stdout += d.toString());
proc.stderr.on('data', d => stderr += d.toString());
proc.on('close', code => {
  if (code === 0) {
    try {
      const pages = JSON.parse(stdout.trim());
      console.log('SUCCESS! Pages found:', pages.length);
      fs.writeFileSync('page_list.json', stdout.trim());
      pages.forEach((p,i) => console.log(String(i+1).padStart(2,'0') + '. ' + p.pageId + ' | ' + p.text));
    } catch(e) {
      console.log('PARSE ERROR. Raw (300):', stdout.substring(0, 300));
    }
  } else {
    console.log('FAILED. stderr:', stderr.substring(0, 300));
  }
});
