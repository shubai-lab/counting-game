@echo off
REM 获取 Confluence 登录 Cookie 并保存到文件
REM 通过 spawn 调用 cdp.mjs，避免 execSync 的 shell 引号问题
node "%~dp0.claude\skills\chrome-cdp-skill\scripts\cdp.mjs" evalraw F5E19A9E Network.getAllCookies > "%~dp0confluence_cookies.txt"
