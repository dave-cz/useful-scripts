/*
* module-template.js
*
* template for Node.js module
*
*/

'use strict';

var request = require('request');
  
module.exports = function(initParams) {
    /*if (!initParams) {
        throw new Error('module-template.exports: initParams is required');
    }
    // use initParams for whatever
    */
    return {
        requestGet: requestGet,
        requestPost: requestPost
    };
}

function requestGet(reqOpt, callback) {
	request.get(reqOpt, function (err, res, body) {
	    var isValidResponse = (!err && 
				res.statusCode === 200);
		if (!isValidResponse) {
			reqOpt.ca = (reqOpt.hasOwnProperty('ca')) ? typeof reqOpt.ca : null;
			err = err || new Error();
			err.message = 'module-template.requestGet '+ err.message;
			err.reqOpt = reqOpt;
			err.statusCode = (typeof res === 'undefined') ? 'undefined' : res.statusCode;
			err.resBody = (typeof body === 'undefined') ? 'undefined' : body
			callback(err);
	    } else {
	        callback(null, res, body);
	    }
	});
}

function requestPost(reqOpt, callback) {
	request.post(reqOpt, function (err, res, body) {
	    if (err || res.statusCode > 201) {
			err = err || new Error();
			reqOpt.ca = (reqOpt.hasOwnProperty('ca')) ? typeof reqOpt.ca : null;
			err.message = 'module-template.requestPost '+ err.message;
			err.reqOpt = reqOpt;
			err.statusCode = (typeof res === 'undefined') ? 'undefined' : res.statusCode;
			err.resBody = (typeof body === 'undefined') ? 'undefined' : body
			callback(err);
	    } else {
	        callback(null, res, body);
	    }
	});
}
