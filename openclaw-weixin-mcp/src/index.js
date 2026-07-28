import http from 'node:http';
import crypto from 'node:crypto';
import QRCode from 'qrcode';

// ============================================================================
// MCP Server Configuration
// ============================================================================
const MCP_SERVER_PORT = 3100;

// ============================================================================
// WeChat API Constants (from openclaw-weixin)
// ============================================================================
const FIXED_BASE_URL = 'https://ilinkai.weixin.qq.com';
const DEFAULT_ILINK_BOT_TYPE = '3';
const ILINK_APP_ID = 'bot';
const ILINK_APP_CLIENT_VERSION = 256; // 0x0100 = 1.0.0

// ============================================================================
// Helper: HTTP Request (GET) - using native fetch
// ============================================================================
async function apiGetFetch(baseUrl, endpoint, timeoutMs = 35000) {
    const url = new URL(endpoint, baseUrl);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const res = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'iLink-App-Id': ILINK_APP_ID,
                'iLink-App-ClientVersion': String(ILINK_APP_CLIENT_VERSION),
            },
            signal: controller.signal,
        });

        clearTimeout(timeoutId);
        return await res.text();
    } catch (err) {
        clearTimeout(timeoutId);
        if (err.name === 'AbortError') {
            return JSON.stringify({ status: 'wait' });
        }
        throw err;
    }
}

// ============================================================================
// Helper: HTTP Request (POST) - using native fetch
// ============================================================================
async function apiPostFetch(baseUrl, endpoint, body, token) {
    const url = new URL(endpoint, baseUrl);
    const data = JSON.stringify(body);

    const headers = {
        'Content-Type': 'application/json',
        'iLink-App-Id': ILINK_APP_ID,
        'iLink-App-ClientVersion': String(ILINK_APP_CLIENT_VERSION),
        'AuthorizationType': 'ilink_bot_token',
        'X-WECHAT-UIN': Buffer.from(String(Math.floor(Math.random() * 0xFFFFFFFF))).toString('base64'),
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(url.toString(), {
        method: 'POST',
        headers,
        body: data,
    });

    const rawText = await res.text();
    if (res.status >= 400) {
        throw new Error(`${res.status}: ${rawText}`);
    }
    return rawText;
}

// ============================================================================
// Helper: Generate random ID
// ============================================================================
function generateId(prefix) {
    const timestamp = Date.now().toString(36);
    const random = crypto.randomBytes(4).toString('hex');
    return `${prefix}-${timestamp}-${random}`;
}

// ============================================================================
// MCP Protocol Handler
// ============================================================================
let mcpRequestId = 0;

async function handleMcpRequest(req, res) {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const body = JSON.parse(Buffer.concat(chunks).toString());

    const jsonrpc = body.jsonrpc || '2.0';
    const id = body.id || ++mcpRequestId;

    try {
        const result = await processMcpMethod(body.method, body.params);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ jsonrpc, id, result }));
    } catch (err) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ jsonrpc, id, error: { code: -32603, message: err.message } }));
    }
}

async function processMcpMethod(method, params) {
    switch (method) {
        case 'initialize':
            return {
                protocolVersion: '2024-11-05',
                capabilities: {
                    tools: {},
                    resources: {},
                },
                serverInfo: {
                    name: 'openclaw-weixin-mcp',
                    version: '1.0.0',
                },
            };

        case 'notifications/initialized':
            return null;

        case 'tools/list':
            return {
                tools: [
                    {
                        name: 'wechat_send_message',
                        description: 'Send a text message to a WeChat user',
                        inputSchema: {
                            type: 'object',
                            properties: {
                                to: { type: 'string', description: 'WeChat user ID (format: xxx@im.wechat)' },
                                text: { type: 'string', description: 'Message text to send' },
                            },
                            required: ['to', 'text'],
                        },
                    },
                    {
                        name: 'wechat_get_qrcode',
                        description: 'Get QR code URL for WeChat login authorization',
                        inputSchema: {
                            type: 'object',
                            properties: {},
                        },
                    },
                    {
                        name: 'wechat_poll_login_status',
                        description: 'Poll login status after QR code scan. Returns login result when confirmed.',
                        inputSchema: {
                            type: 'object',
                            properties: {
                                qrcode: { type: 'string', description: 'QR code identifier from get_qrcode' },
                            },
                            required: ['qrcode'],
                        },
                    },
                    {
                        name: 'wechat_get_accounts',
                        description: 'List all logged-in WeChat accounts',
                        inputSchema: {
                            type: 'object',
                            properties: {},
                        },
                    },
                    {
                        name: 'wechat_get_updates',
                        description: 'Long-poll for new messages from WeChat (call this to receive messages)',
                        inputSchema: {
                            type: 'object',
                            properties: {},
                        },
                    },
                    {
                        name: 'wechat_logout',
                        description: 'Logout a WeChat account by accountId',
                        inputSchema: {
                            type: 'object',
                            properties: {
                                accountId: { type: 'string', description: 'Account ID to logout' },
                            },
                            required: ['accountId'],
                        },
                    },
                ],
            };

        case 'tools/call':
            return await handleToolCall(params.name, params.arguments);

        default:
            throw new Error(`Unknown method: ${method}`);
    }
}

// ============================================================================
// Tool Handlers
// ============================================================================
const accountStore = new Map();
const activeLogins = new Map();

// Message store for received messages (persisted)
let getUpdatesBuf = '';

// ============================================================================
// WeChat Tool Implementations
// ============================================================================

async function wechatGetQRCode() {
    console.log('[MCP] Getting WeChat QR code...');

    // Fetch QR code from WeChat backend
    const localTokenList = [];
    const responseText = await apiPostFetch(
        FIXED_BASE_URL,
        `ilink/bot/get_bot_qrcode?bot_type=${DEFAULT_ILINK_BOT_TYPE}`,
        {
            local_token_list: localTokenList,
            base_info: {
                channel_version: '1.0.0',
                bot_agent: 'ClaudeCode/1.0',
            },
        }
    );

    console.log('[MCP] QR response:', responseText.substring(0, 200));

    const resp = JSON.parse(responseText);
    const qrcodeUrl = resp.qrcode_img_content;

    // Generate QR code as base64 PNG
    const qrcodeBase64 = await QRCode.toDataURL(qrcodeUrl, {
        width: 300,
        margin: 2,
        color: {
            dark: '#000000',
            light: '#ffffff',
        },
    });

    // Store QR code for polling
    activeLogins.set(resp.qrcode, {
        qrcodeUrl,
        qrcodeId: resp.qrcode,
        createdAt: Date.now(),
    });

    return {
        qrcode_url: qrcodeUrl,
        qrcode_id: resp.qrcode,
        qrcode_base64: qrcodeBase64,
        message: '请用手机微信扫描此二维码',
    };
}

async function wechatPollLoginStatus(qrcode) {
    console.log(`[MCP] Polling login status for QR: ${qrcode.substring(0, 20)}...`);

    // Long-poll QR status using GET
    const rawText = await apiGetFetch(
        FIXED_BASE_URL,
        `ilink/bot/get_qrcode_status?qrcode=${encodeURIComponent(qrcode)}`
    );

    let result;
    try {
        result = JSON.parse(rawText);
    } catch {
        result = { status: 'wait' };
    }

    console.log(`[MCP] Poll result: ${result.status}`);

    switch (result.status) {
        case 'wait':
            return {
                status: 'waiting',
                message: '请用手机微信扫描二维码',
            };

        case 'scaned':
            return {
                status: 'scaned',
                message: '已扫描，请在手机确认',
            };

        case 'confirmed':
            if (!result.ilink_bot_id) {
                return { status: 'error', message: '登录失败：服务器未返回 ilink_bot_id' };
            }

            // Save account
            const accountId = result.ilink_bot_id;
            accountStore.set(accountId, {
                token: result.bot_token,
                baseUrl: result.baseurl,
                userId: result.ilink_user_id,
                contextTokens: {},
            });

            return {
                status: 'connected',
                accountId: accountId,
                userId: result.ilink_user_id,
                message: '已成功连接到微信',
            };

        case 'expired':
            return {
                status: 'expired',
                message: '二维码已过期，请重新获取',
            };

        case 'need_verifycode':
            return {
                status: 'need_verifycode',
                message: '请输入手机微信显示的验证码',
            };

        default:
            return {
                status: 'unknown',
                raw: result,
            };
    }
}

async function wechatSendMessage(to, text) {
    console.log(`[MCP] Sending message to ${to}: ${text.substring(0, 50)}...`);

    // Find account with context token for this user
    let account = null;
    let contextToken = null;

    for (const [accId, accData] of accountStore) {
        if (accData.userId === to) {
            account = accData;
            contextToken = accData.contextTokens?.[to];
            break;
        }
    }

    if (!account) {
        // Try to use any available account
        const accounts = Array.from(accountStore.values());
        if (accounts.length === 0) {
            return { success: false, error: 'No WeChat account connected. Please login first.' };
        }
        account = accounts[0];
    }

    const clientId = generateId('wechat');

    try {
        await apiPostFetch(
            account.baseUrl,
            'ilink/bot/sendmessage',
            {
                msg: {
                    from_user_id: '',
                    to_user_id: to,
                    client_id: clientId,
                    message_type: 2, // BOT
                    message_state: 2, // FINISH
                    item_list: [{ type: 1, text_item: { text } }],
                    context_token: contextToken,
                },
            },
            account.token
        );

        return {
            success: true,
            messageId: clientId,
        };
    } catch (err) {
        console.error(`[MCP] Send failed: ${err.message}`);
        return { success: false, error: err.message };
    }
}

async function wechatGetUpdates() {
    console.log('[MCP] Long-polling for WeChat updates...');

    // Get first available account
    const accounts = Array.from(accountStore.values());
    if (accounts.length === 0) {
        return { ret: 0, msgs: [], message: 'No account connected' };
    }

    const account = accounts[0];

    try {
        const responseText = await apiPostFetch(
            account.baseUrl,
            'ilink/bot/getupdates',
            {
                get_updates_buf: getUpdatesBuf,
                base_info: {
                    channel_version: '1.0.0',
                    bot_agent: 'ClaudeCode/1.0',
                },
            },
            account.token
        );

        const resp = JSON.parse(responseText);
        console.log(`[MCP] getUpdates response: ret=${resp.ret}, msgs=${resp.msgs?.length ?? 0}`);

        // Update sync buf
        if (resp.get_updates_buf) {
            getUpdatesBuf = resp.get_updates_buf;
        }

        // Store context tokens
        if (resp.msgs?.length) {
            for (const msg of resp.msgs) {
                if (msg.context_token && msg.from_user_id) {
                    if (!account.contextTokens) {
                        account.contextTokens = {};
                    }
                    account.contextTokens[msg.from_user_id] = msg.context_token;
                    console.log(`[MCP] Stored context token for ${msg.from_user_id}`);
                }
            }
        }

        return resp;
    } catch (err) {
        console.error(`[MCP] getUpdates failed: ${err.message}`);
        return { ret: -1, error: err.message, msgs: [] };
    }
}

async function wechatGetAccounts() {
    const accounts = [];
    for (const [accountId, data] of accountStore) {
        accounts.push({
            accountId,
            userId: data.userId,
            baseUrl: data.baseUrl,
            hasToken: !!data.token,
        });
    }
    return { accounts };
}

async function wechatLogout(accountId) {
    if (accountStore.has(accountId)) {
        accountStore.delete(accountId);
        return { success: true, message: '已登出' };
    }
    return { success: false, error: 'Account not found' };
}

async function handleToolCall(toolName, args) {
    switch (toolName) {
        case 'wechat_get_qrcode':
            return await wechatGetQRCode();

        case 'wechat_poll_login_status':
            return await wechatPollLoginStatus(args.qrcode);

        case 'wechat_send_message':
            return await wechatSendMessage(args.to, args.text);

        case 'wechat_get_updates':
            return await wechatGetUpdates();

        case 'wechat_get_accounts':
            return await wechatGetAccounts();

        case 'wechat_logout':
            return await wechatLogout(args.accountId);

        default:
            throw new Error(`Unknown tool: ${toolName}`);
    }
}

// ============================================================================
// MCP Server Startup
// ============================================================================
const server = http.createServer(async (req, res) => {
    // CORS headers for browser requests
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.method === 'POST' && req.url === '/mcp') {
        await handleMcpRequest(req, res);
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

server.listen(MCP_SERVER_PORT, () => {
    console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   OpenClaw WeChat MCP Server                              ║
║   已启动在 http://localhost:${MCP_SERVER_PORT}                    ║
║                                                           ║
║   可用工具:                                                ║
║   - wechat_get_qrcode        获取登录二维码                  ║
║   - wechat_poll_login_status  轮询登录状态                   ║
║   - wechat_send_message     发送消息                       ║
║   - wechat_get_updates      接收消息（长轮询）               ║
║   - wechat_get_accounts      列出账号                        ║
║   - wechat_logout            登出账号                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);
});

process.on('SIGINT', () => {
    console.log('\n[MCP] Shutting down...');
    server.close();
    process.exit(0);
});