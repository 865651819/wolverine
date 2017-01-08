/**
 * This is used to walk pages and click the ads on last page.
 */
var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true,
    logLevel: "info"
});


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
            // casper.log('candidate ' + i + ' ' + ads_candidate[i], "info");
        }

        casper.each(ads_candidate, function (self, url) {
            self.thenOpen(url, function () {
                casper.log('Clicking the ad ' + url, 'info');
                casper.log('Second Page: ' + this.getTitle(), "info");
            });
        });
    });
});


casper.run();