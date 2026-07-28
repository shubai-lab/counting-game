/**
 * 数据传输对象
 */

var ERROR_MSG = '服务器错误';

module.exports = function(config) {


    var ret = {};

    for (var key in config) {
        ret[key] = (function(options) {
            return function(data, success, fail) {
                return $.ajax($.extend($.extend({
                    dataType: "json"
                }, options), {
                    data: data
                })).done(function(res) {
                    if (checkCode(res)) {
                        success && success(res);
                    } else {
                        res = res || {};
                        if (!fail || fail(res)) {
                            showTip(res);
                        }
                    }
                }).fail(function(res) {
                    res = res || {};
                    if (!fail || fail(res)) {
                        showTip(res);
                    }
                });
            }
        })(config[key]);
    }

    return ret;

};


function checkCode(res) {
    var code = res && (res.code + '') || '200000';
    if (code === '100000') {
        return true;
    }
    if (code === '100002') {
        location.href = '/static/html/login.html?r=' + encodeURIComponent(location.href);
        return false;
    }

    return false;
}

function showTip(res) {
    // bootbox.alert(res.msg || ERROR_MSG);
    console.log(res.msg || ERROR_MSG)
}