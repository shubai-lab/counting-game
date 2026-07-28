const { spawn } = require('child_process');
const CDP = '.claude/skills/chrome-cdp-skill/scripts/cdp.mjs';
const TARGET = 'C309766D';
const fs = require('fs');

const code = `JSON.stringify([...document.links].filter(a=>a.href.includes('pageId=')).map(a=>a.href.match(/pageId=(\\d+)/)?.[1]).filter(Boolean).filter((v,i,a)=>a.indexOf(v)===i).slice(0,50))`;

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
    fs.writeFileSync('page_list.json', stdout);
    try {
      const pages = JSON.parse(stdout.trim());
      console.log('SUCCESS! Pages found:', pages.length);
      pages.slice(0,5).forEach((p,i) => console.log((i+1)+'.', JSON.stringify(p)));
    } catch(e) {
      console.log('PARSE ERROR. Raw (300):', stdout.substring(0, 300));
    }
  } else {
    console.log('FAILED. stderr:', stderr.substring(0, 300));
  }
});
