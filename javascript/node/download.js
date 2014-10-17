/*
 * download.js
 *
 * asynchronous download of files
 *
 */

'use strict';
process.chdir(__dirname);

var async = require('async'),
	fs = require('fs'),
    request = require('request'),
	folder = './', // or 'whatever/'
	files = [];

function download(uri, filename, cb){
	request.head(uri, function(err, res, body){
		if (err) {
			cb(err);
		}
		if (res.statusCode !== 200) {
			cb(new Error("Status Code: "+res.statusCode));
		} else {
			request(uri).pipe(fs.createWriteStream(filename)).on('close', cb);
		}
	});
}

async.series([
    function(cb){ // create folder
		fs.mkdir(folder, function(err) {
	        if (err) {
	            if (err.code == 'EEXIST') {
					cb(); // ignore the error if the folder already exists
				}
	            else {
					cb(err); // something else went wrong
				}
	        } else cb(); // successfully created folder
	    });
	},
    function(cb){ // generate array of files
		files.push({
			url: 'http://upload.wikimedia.org/wikipedia/meta/0/08/Wikipedia-logo-v2_1x.png',
			name: folder+'wiki-logo.png'
		});
		cb();
	},
    function(cb){ // download
		async.each(files, function (file, callback) {
		    download(file.url, file.name, function(err) {
				if (err) {
					console.log(file.name+'\t\t'+err.message);
				} else {
					console.log(file.name+'\t\tOK');
				}
			});
		});
	}
]);
