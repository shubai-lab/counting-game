/**
 * steel file for cli-version
 * author: @Lonefy
 */
var path = require('path');
var steel = require('steel');

steel.config({
    port: 80,
    build_path: 'build/',
    pathnamePrefix: '/',
    back_pathnamePrefix: '/',
    cssfix_filter: {
        prefix: true,
        filter: ["components/**/*.*"]
    },
    front_base: 'server_front',
    src_base: 'src/',
    front_hostname: '127.0.0.1 res.test.cn',
    back_base: 'server_back', //模拟后端的文件放置目录
    back_hostname: '127.0.0.1 back.test.cn', //后端的HOST，目的是真实模拟后端的页面路由请求，提供出前端可仿真的功能，比如 /index 对应 /html/index.html
})

steel.task("hw", function() {
    console.log("hello world, Steel");
})