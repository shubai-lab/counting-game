var fs = require('fs');
var path = require('path');
var semver = require('semver');
var chalk = require('chalk');
var _ = require('lodash');
var mkdirp = require('mkdirp');
var tpl = require('./template')();
var minimatch = require('minimatch');


var generator = module.exports

function findLastest(versions) {
    var t = '0.0.0';
    for (var v in versions) {
        if (semver.lt(t, v)) t = v;
    }
    return t;
}

generator.getJSON = function(type) {
    if(!hasType(type)) return;
    return tpl[type].getJson();
}

generator.getType = function (){
    var arr = [];
    for(var i in tpl){
        arr.push(i);
    }
    return arr;
}

generator.getTaskfilePath = function getTaskfilePath(type) {
    if(!hasType(type)) return;
    return tpl[type].getTaskfilePath();
}

generator.template = function template(type, destination, checkexist, glob) {
    
    if(!hasType(type)) return;
      
    var t = tpl[type];
    var filepath = t.filePaths;
    var folderRoot = t.folderRoot;
  
    for (var i = 0, l = filepath.length; i < l; i++) {
        if(glob !== undefined && !minimatch(filepath[i], glob)) continue;
        
        var source = path.join(folderRoot, filepath[i]);
        var filedest = path.join(destination, filepath[i])
        output(source, filedest, checkexist)
    }

}

generator.templateMatch = function templateOne(type, destination, glob) {
    this.template(type, destination , false, glob);
}

function hasType(type){
    var flag = !!tpl[type];
    !flag && console.log('No '+ type +' template');
    return flag;
}

function output(source, destination, checkexist) {
    var body = read(source);
    write(destination, body, checkexist);
}

function read(filepath, encoding) {
    var contents = fs.readFileSync(filepath);

    return contents.toString(encoding || 'utf8');
};

function write(filepath, content, checkexist) {

    mkdirp.sync(path.dirname(filepath));
    fs.stat(filepath, function(err, stat) {
        if(err == null) {
            checkexist && fs.writeFile(filepath, content, function(e) {
                !e && console.log('generate file: ' ,filepath)
            })
        } else if(err.code == 'ENOENT') {
            fs.writeFile(filepath, content, function(e) {
                !e && console.log('generate file: ' ,filepath)
            })
        } else {
            console.log('Some other error: ', err.code);
        }
    });
    
    return this;
};
