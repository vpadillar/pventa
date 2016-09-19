/* 
 * @author: Luis Miguel Morlae Pájaro
 * @business: ScriptQuo SAS
 * @date: 19-02-2016
 */

var WAITH = 0;
var ERROR = -1;
var OK = 1;

window.sq = {
    /**
     * 
     * @param {[Object]} options as {success: ..., error: ...}
     * @returns {nothing}
     */
    
    print: function (options) {
        var ID = document.body.getAttribute("sq-print-id");
        chrome.runtime.sendMessage(ID, {data: options.data, status: options.status}, function (data) {
            if (chrome.runtime.lastError) {
                if (options.error) {
                    options.error(chrome.runtime.lastError);
                }
            } else
            if (options.success) {
                console.log(options.status);
                if (data.status === OK) {
                    options.success(data);
                } else
                if (data.status === WAITH) {
                    options.status = WAITH;
                    window.sq.print(options);
                } else {
                    console.log("erro!");
                    options.error(data);
                }
            }
        });
    }

};

