/**
 * logic
 */

module.exports = function(node, data, control) {

    var that = {};

    logicmsg();
    
    return that;

    function logicmsg(){
        var dom = document.getElementById('logicmsg');
        dom.innerHTML = data.logicmsg;
    }
};