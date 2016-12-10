/**
 * Created by jinwang on 12/9/16.
 */
var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true
});


var links = [];
function get_links(obj) {
    return obj.evaluate(function () {
        var l = document.querySelectorAll("a"),
            l2 = [];
        for (var i = 0; i < l.length; i++) {
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
    this.echo("Visit Page: " + this.getCurrentUrl() + "\n");
    function to_frame(obj) {
        var iframes = to_evaluate(obj);
        iframes.forEach(function (index) {
            this.withFrame(index, function () {
                this.echo(": " + this.getCurrentUrl());
                var l = unique(get_links(this));
                var i;
                for (i = 0; i < l.length; i++) {
                    console.log(l[i]);
                    links.push(l[i])
                }
                links = unique(links);
                console.log("");
                to_frame(this)//multi lvl
            });//The first iframe
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


casper.start("http://www.51yrj.com/ad/ggj_51yrj.html", function () {
    var theLinks = links;
    getLinksFromIframes.call(this, function () {
        console.log("Done!\n");
        var i;
        for (i = 0; i < links.length; i++) {
            this.echo("test@" + links[i]);
        }
        casper.thenOpen(links[links.length - 1], function () {
            this.echo('Second Page: ' + this.getTitle());
            this.exit();
        });
    });
}).wait(1000000).run();