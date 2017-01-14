/**
 * This is used to walk pages and click the ads on last page.
 */
var utils = require('utils');


var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true,
    logLevel: "info"
});

//casper.options.onResourceRequested = function(C, requestData, request) {
//    utils.dump(requestData.headers);
//};
//casper.options.onResourceReceived = function(C, response) {
//    utils.dump(response.headers);
//};

casper.options.onResourceRequested = function(C, requestData, request) {
    if ((/https?:\/\/.+?\.css/gi).test(requestData['url']) || requestData['Content-Type'] == 'text/css') {
        console.log('Skipping CSS file: ' + requestData['url']);
        request.abort();
    }
}

function getRandomInt() {
    return Math.floor(Math.random() * (10000 - 3000)) + 3000;
}

function getSeconds(min, max) {
    return Math.floor(Math.random() * (max * 1000 - min * 1000)) + min * 1000;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// @Required
// Set user agent by passing argument --ua
casper.userAgent(casper.cli.get('ua'));


// @Required
var ads_page = casper.cli.args[0];
casper.log('ads_page is ' + ads_page, 'debug');


// The count of ads window in the page
var SPOTS_COUNT = 0;


// All ads(or not) links
var links = [];
function get_links(obj) {
    return obj.evaluate(function () {
        var l = document.querySelectorAll("a");
        var l2 = [];
        for (var i = 0; i < l.length; i++) {
            l2[i] = l[i].href;
        }
        return l2;
    });
}


function unique(arr) {
    var obj = {};
    for (var i = 0; i < arr.length; i++) {
        if (/http(.*)?/.test(arr[i])) {
            var str = arr[i];
            obj[str] = true;
        }
    }
    return Object.keys(obj);
}


function getLinksFromIframes(callback) {
    casper.log("Get links for this link " + this.getCurrentUrl() + "\n", 'debug');
    var parent = this.getCurrentUrl();

    function to_frame(obj) {

        // Get iframes inside this
        var iframes = to_evaluate(obj);

        // Evaluate each iframe
        iframes.forEach(function (index) {

            this.withFrame(index, function () {
                // casper.log("Evaluate the iframe : " + this.getCurrentUrl(), 'debug');

                // if parent is the ads_page, assuming each iframe means one ads window.
                if (parent === ads_page) {
                    SPOTS_COUNT = SPOTS_COUNT + 1;
                }

                var l = unique(get_links(this));
                for (var i = 0; i < l.length; i++) {
                    casper.log('Get the link ' + l[i], 'debug');
                    links.push(l[i]);
                }
                links = unique(links);
                to_frame(this);
            });
        }, obj);
    }

    function to_evaluate(obj) {
        return obj.evaluate(function () {
            var iframes = [];
            [].forEach.call(document.querySelectorAll("iframe"), function (iframe, i) {
                iframes.push(i);
            });
            return iframes;
        })
    }

    to_frame(this);
    this.then(function () {
        callback.call(this);
    });
}

function getLinks() {
    var links = document.querySelectorAll('a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href');
    });
}


casper.start(ads_page, function () {
    casper.log('Get all ads candidate and click candidates ' + ads_page, "info");
    getLinksFromIframes.call(this, function () {
        /*
         casper.log("Done!\n", "debug");
         casper.log('found spots [' + SPOTS_COUNT + ']', "debug");
         for (var i = 0; i < links.length; i++) {
         casper.log("candidate@" + i + ' ' + links[i], "debug");
         }
         casper.log('find candidates', "debug");
         */

        // Get ads link candidates
        var target_count = links.length > SPOTS_COUNT ? SPOTS_COUNT : links.length;
        links.sort(function (a, b) {
            return b.length - a.length;
        });
        var ads_candidate = links.slice(0, target_count);

        // Debugging purpose
        for (var i = 0; i < ads_candidate.length; ++i) {
            casper.log('candidate ' + i + ' ' + ads_candidate[i], "info");
        }

        /*
        casper.each(ads_candidate, function (self, url) {
            self.thenOpen(url, function () {
                casper.log('Clicking the ad ' + url, 'info');
                casper.log('Second Page: ' + this.getTitle(), "info");
            });
        });
        */

        var billcpc = "bill_cpc";
        var target = "target";

        var index = Math.floor(Math.random() * (ads_candidate.length));
        if (index >= ads_candidate.length) {
            index = 0;
        }

        this.page.customHeaders = {
            "Referer": ads_candidate[index]
        };


        var page_wait = getSeconds(5, 10);
        console.log('wait on the page ' + page_wait, 'warning');
        this.wait(page_wait, function() {
            this.thenOpen(ads_candidate[index], function() {
                casper.log('ads index ' + index);
                casper.log('Clicking the ad ' + ads_candidate[index], 'warning');
                casper.log('Second Page: ' + this.getTitle(), "warning");
                var links_nested = get_links(this);
                // casper.log(links_nested, "info");
                for (var i=0; i<links_nested.length; ++i) {
                    // casper.log('link is ' + links_nested[i], "info");
                    if (links_nested[i].indexOf(billcpc) > 0) {
                        target = links_nested[i];
                        break;
                    }
                }
                if (target === "target") {
                    target = links[0];
                }

                this.page.customHeaders = {
                    "Referer": target
                };

                casper.log("candidate is " + target, "info");
                var sougou_search_wait = getSeconds(5, 10);
                casper.log('wait on sougou searching ' + sougou_search_wait, 'warning');

                casper.wait(sougou_search_wait, function() {
                    casper.thenOpen(target, function() {
                        casper.log('Clicking the searching result ' + target, 'warning');
                        casper.log('Third Page: ' + this.getTitle(), "warning");

                        var customer_wait = getSeconds(10, 60);
                        casper.log('wait on customer ' + customer_wait, 'warning');

                        var links_customer = get_links(this);

                        /*
                        var links_candidate = [];
                        for (var j=0; j<links_customer.length; ++j) {
                            casper.log('child link ' + links_customer[j], 'warning');
                            if (links_customer[j].indexOf("html")>0
                                || (links_customer[j].indexOf("htm")>0)
                                || (links_customer[j].indexOf('jpg') <= 0)) {
                                links_candidate.push(links_customer[j]);
                                casper.log('Found ', 'warning');
                            }
                        }
                        var t = -1;
                        if (links_customer) {
                            t = getRandomInt(0, links_candidate.length);
                        }

                        var new_referer = this.getCurrentUrl();
                        casper.log('customer page ' + new_referer, 'warning');
                        this.page.customHeaders = {
                            "Referer": new_referer
                        };
                        */
                        casper.wait(customer_wait, function() {
                            casper.log('customer waiting is done');
                            /*
                            if (t !== -1) {
                                casper.thenOpen(links_candidate[t], function() {
                                    casper.log('wait on customer second level ' + customer_wait);
                                    casper.log('child page ' + this.getCurrentUrl());
                                    var next_wait = getSeconds(5, 15);
                                    this.wait(next_wait, function() {});
                                });
                            } else {
                                casper.log('cannot find nested link ', 'warning');
                            }
                            */
                        });
                    });
                });
            });
        });
    });
});


casper.run();