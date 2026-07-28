var fs = require('fs');
var path = require('path');
var semver = require('semver');
var chalk = require('chalk');
var _ = require('lodash');

module.exports = function() {
    var packageVersion = {}
        , tplPath = path.join(__dirname, 'templates')
        , files = fs.readdirSync(tplPath);

    for (var i = 0, l = files.length; i < l; i++) {
        var folderName = files[i],
            folderRoot = path.join(tplPath, folderName);
        var stats = fs.statSync(folderRoot);

        if (stats.isDirectory()) {

            // var temp = require(folderRoot + "/" + 'package.json');
            var temp = require(path.join(folderRoot, 'package.json'));
            var type = temp['ria-type'] || _.trim(folderName);
            var version = temp.version;
            var filePaths = getFilePath(folderRoot);

            packageVersion[type] = new Templates({
                folderRoot: folderRoot,
                filePaths: filePaths,
                type: type,
                version: version,
                json: temp,
                libPath: path.join(folderRoot, 'steel.js'),
                taskfilePath: path.join(folderRoot, '_task-steel.js')
            })
        }
    }
    return packageVersion;
}


function getFilePath(root) {
    var arr = [];
    findFile(root, root, arr);
    return arr;
}

function findFile(baseRoot, root, filePaths) {

    var files = fs.readdirSync(root);

    for (var i = 0, l = files.length; i < l; i++) {
        var name = files[i];
        var p = path.join(root, name);
        var stats = fs.statSync(p);
        if (stats.isFile()) {

            //ignore '_'-file
            if (!/^_/.test(name)) {
                filePaths.push(path.relative(baseRoot, p));
            }
        }
        else if (stats.isDirectory()) {
            findFile(baseRoot, p, filePaths);
        }
    }
}

function Templates(data) {
    _.extend(this, data);
    return this;
}

Templates.prototype.getJson = function() {
    return this.json;
}
Templates.prototype.getFilePaths = function() {
    return this.filePaths
}
Templates.prototype.getVersion = function() {
    return this.version;
}
Templates.prototype.getType = function() {
    return this.type;
}
Templates.prototype.getTaskfilePath = function() {
    return this.taskfilePath;
}
Templates.prototype.getLibPath = function() {
    return this.libPath;
}