/**
 * Created by jinwang on 12/9/16.
 */
var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true,
    logLevel: "debug"
});

var links = [];

var myParents = {};


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

        var parent = obj.getCurrentUrl();
        console.log('parent is ' + parent);

        iframes.forEach(function (index) {
            this.withFrame(index, function () {
                this.echo(": " + this.getCurrentUrl());
                var curUrl = this.getCurrentUrl();
                var l = unique(get_links(this));
                for (var i = 0; i < l.length; i++) {
                    console.log(l[i]);
                    links.push(l[i]);
                }

                if (myParents[parent]) {
                    console.log('existed....');
                    myParents[parent].push(curUrl);
                } else {
                    console.log('new ones');
                    myParents[parent] = [curUrl];
                }

                links = unique(links);
                to_frame(this)//multi lvl
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


casper.start("http://www.93959.com/", function () {

    //casper.wait(10000, function() {

        casper.log('wait is done');

        getLinksFromIframes.call(this, function () {
            console.log("Done!\n");
            for (var i = 0; i < links.length; i++) {
                this.echo("test@" + links[i]);
            }

            console.log("my parents");
            console.log(Object.keys(myParents));
            console.log(Object.keys(myParents).length);

            if (Object.keys(myParents)) {
                for (var key in Object.keys(myParents)) {
                    console.log("###### " + key);
                }
            }

            console.log('###!' + myParents["http://www.93959.com/"]);
            console.log('size ' + myParents["http://www.93959.com/"].length);

            var l = myParents["http://www.93959.com/"];
            for (var i=0; i<l.length; ++i) {
                console.log('````` ' + l[i]);
            }

            casper.thenOpen(links[links.length - 1], function () {
                this.echo('Second Page: ' + this.getTitle());
                this.exit();
            });
        });
    //});


}).run();