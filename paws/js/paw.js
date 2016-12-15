/**
 * Created by jinwang on 12/9/16.
 */
var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true,
    logLevel: "debug"
});

casper.userAgent(casper.cli.get('ua'));

var links = [];

var paw_url = 'http://www.91txs.net/tansuo/faming/201607/11930.html'

var SPOTS_COUNT=0;

var links = [];
function get_links(obj) {
    return obj.evaluate(function () {
        var i,
            l = document.querySelectorAll("a"),
            l2 = [];
        for (i = 0; i < l.length; i++) {
            l2[i] = l[i].href;
        }
        return l2
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
    this.echo("Here we come: " + this.getCurrentUrl() + "\n");

    var parent =this.getCurrentUrl();

    function to_frame(obj) {
        var iframes = to_evaluate(obj);
        iframes.forEach(function (index) {
            this.withFrame(index, function () {
                this.echo("We are here: " + this.getCurrentUrl());

                if (parent === paw_url) {
                    SPOTS_COUNT = SPOTS_COUNT + 1;
                }

                var l = unique(get_links(this));
                var i;
                for (i = 0; i < l.length; i++) {
                    console.log(l[i]);
                    links.push(l[i])
                }
                links = unique(links);
                console.log("");
                to_frame(this) //multi lvl
            }); //The first iframe
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


//casper.start('http://www.91txs.net/shehui/quwen/201507/6527.html');

casper.start(paw_url, function () {

    //casper.wait(10000, function() {

    casper.log('wait is done');

    getLinksFromIframes.call(this, function () {
        console.log("Done!\n");

        console.log('found spots [' + SPOTS_COUNT + ']');

        for (var i = 0; i < links.length; i++) {
            this.echo("candidate@" + i + ' ' + links[i]);
        }

        console.log('find candidates');

        var target_count = links.length > SPOTS_COUNT ? SPOTS_COUNT : links.length;

        links.sort(function (a, b) {
            return b.length - a.length;
        });

        var ads_candidate = links.slice(0, target_count);

        console.log('candidates are ');
        for (var i = 0; i < ads_candidate.length; ++i) {
            console.log('candidate ' + i + ' ' + ads_candidate[i]);
        }

        casper.each(ads_candidate, function (self, url) {
            self.thenOpen(url, function () {
                this.echo('Second Page: ' + this.getTitle());
                // Do Whatever
            });
        });
    });
    //});


});

casper.run();