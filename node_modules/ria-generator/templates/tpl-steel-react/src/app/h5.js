steel.config({
    
  mainBox: document.body,
  singlePage: true,
  stage: true,
  stageCache: true,
  stageChange: true,
  useCssPrefix: true,
  router: [
    ['/h5/index', 'components/h5/index/ctrl'],
  ]
});

steel.on('stageChange', function(box, renderFromStageCache) {
    var routerType = steel.router.get().type;
    if (routerType === 'init' || routerType === 'forward' || routerType === 'new'  || routerType === 'replace') {
        // box.innerHTML = loadingTpl({
        //     text: '加载中...'
        // });
    }
});

//监听渲染事件
steel.on('renderError', pageError);

function pageError(res) {
    steel.stage.getBox().innerHTML = '';
    // uiTip(res && res.msg || '数据异常', {
    //     type: 'warn',
    //     autoHide: 0
    // });
    if (res && (res.code + '') === '100002') {
        location.href = 'http://passport.weibo.cn/signin/login?r=' + encodeURIComponent(location.href);
    }
}