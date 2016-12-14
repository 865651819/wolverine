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

var myParents = {};


function get_links(obj) {
    return obj.evaluate(function () {
        var l = document.querySelectorAll("a"),
            l2 = [];
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

var COUNT = 1;

function getLinksFromIframes(callback) {

    this.echo("Visit Page: " + this.getCurrentUrl() + "\n");
    function to_frame(obj) {
        var iframes = to_evaluate(obj);

        var parent = obj.getCurrentUrl();

        iframes.forEach(function (index) {
            this.withFrame(index, function () {
                this.echo("find iframe : " + this.getCurrentUrl());
                var curUrl = this.getCurrentUrl();

                if (curUrl === 'about:blank') {
                    console.log('my name is about:blank, bad need a new name');
                    curUrl = 'about:blank' + COUNT;
                    console.log('my new name is ' + curUrl);
                    COUNT = COUNT + 1;
                }

                var curLinks = [];
                var l = unique(get_links(this));
                console.log('find these links under the iframe ' + curUrl);
                for (var i = 0; i < l.length; i++) {
                    console.log(l[i]);
                    links.push(l[i]);
                    curLinks.push(l[i]);
                }


                if (myParents[parent]) {
                    console.log('parent is already existed....' + parent);
                    console.log('i am child ' + curUrl);
                    if (myParents[parent].indexOf(curUrl) < 0) {
                        console.log('parent exists, but does not include me added me! ' + curUrl);
                        myParents[parent].push(curUrl);
                    }
                } else {
                    console.log('my parent does not exist, add both of us! my parent is ' + parent);
                    console.log('add me as well ' + curUrl);
                    myParents[parent] = [curUrl];
                }

                if (myParents[curUrl]) {
                    console.log('i am already existed....' + curUrl);


                    for (var j=0; j<curLinks.length; ++j) {
                        if (myParents[curUrl].indexOf(curLinks[j]) < 0) {
                            console.log('i do not have this link ' + curLinks[j]);
                            myParents[curUrl].push(curLinks[j]);
                            console.log('add new link ' + curLinks[j])
                        } else {
                            console.log('i already have !!duplicate ' + curLinks[j]);
                        }
                    }


                } else {
                    console.log('I am not existed, added me ' + curLinks);
                    console.log('added my child links as well');
                    myParents[curUrl] = [];
                    for (var j=0; j<curLinks.length; ++j) {
                        if (myParents[curUrl].indexOf(curLinks[j]) < 0) {
                            console.log('i do not have this link ' + curLinks[j]);
                            myParents[curUrl].push(curLinks[j]);
                            console.log('add new link ' + curLinks[j])
                        } else {
                            console.log('i already have !!duplicate ' + curLinks[j]);
                        }
                    }
                }

                links = unique(links);
                to_frame(this); //multi lvl
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

function getLinks(iframe_key) {
    casper.log('current key is ' + iframe_key);
    var curLinks = myParents[iframe_key];
    if (!curLinks) {
        casper.log('I am the leaf node, return');
        return [];
    }
    var links = [];
    for (var i=0; i<curLinks.length; ++i) {
        casper.log('add to list and trace child ' + curLinks[i]);
        links.push(curLinks[i]);
        //links.concat(getLinks(curLinks[i]));

        var childLinks = getLinks(curLinks[i]);
        for (var j=0; j<childLinks.length; ++j) {
            if (links.indexOf(childLinks[j]) < 0) {
                links.push(childLinks[j]);
                console.log('add new link ' + childLinks[j])
            } else {
                console.log('!!duplicate');
            }
        }

    }
    casper.log('get all links for this iframe ' + iframe_key)
    casper.log(links);
    return links;
}


casper.start('http://www.91txs.net/shehui/quwen/201507/6527.html');

casper.thenOpen("http://www.91txs.net/shehui/tuku/201603/11054.html", function () {

    //casper.wait(10000, function() {

        casper.log('wait is done');

        getLinksFromIframes.call(this, function () {
            console.log("Done!\n");
            for (var i = 0; i < links.length; i++) {
                this.echo("test@" + links[i]);
            }

            //console.log("my parents");
            //console.log(Object.keys(myParents));
            //console.log(Object.keys(myParents).length);

            var ads_by_spot = {}

            console.log("we have these spots!!!!");
            var spots = myParents['http://www.91txs.net/shehui/tuku/201603/11054.html'];
            console.log("Number is " + str(spots.length));
            console.log(spots);
            for (var i=0; i<spots.length; ++i) {
                console.log(spots[i]);
            }

            console.log("Get links for each spot!!");
            for (var i=0; i<spots.length; ++i) {
                console.log('spot key is ' + spots[i]);
                ads_by_spot[spots[i]] = getLinks(spots[i]);
            }


            // console.log('###!' + myParents["http://www.93959.com/"]);
            // console.log('size ' + myParents["http://www.93959.com/"].length);

            // var l = myParents["http://www.93959.com/"];
            // for (var i=0; i<l.length; ++i) {
            //     console.log('````` ' + l[i]);
            // }

            var ads_candidate = [];
            console.log('find candidates');
            for (var i=0; i<spots.length; ++i) {
                var links_for_cur_spot = ads_by_spot[spots[i]];
                console.log('candidate for spot ' + spots[i]);
                console.log('links_for_cur_spot ' + links_for_cur_spot);
                console.log('links_candidate ' + links_for_cur_spot.length);
                var min = 0;
                var candidate;
                for (var j=0; j<links_for_cur_spot.length; ++j) {
                    console.log('cur link ' + links_for_cur_spot[j]);
                    console.log('link length ' + links_for_cur_spot[j].length)
                    if (links_for_cur_spot[j].length >= min) {
                        candidate = links_for_cur_spot[j];
                        min = candidate.length;
                    }
                }
                if (candidate) {
                    console.log('add candidate ' + candidate);
                    if (ads_candidate.index(candidate) < 0) {
                        console.log('new candidate, welcome ' + candidate);
                        ads_candidate.push(candidate);
                    } else {
                        console.log('we already have you, bye! ' + candidate);
                    }
                }
            }

            console.log('ads candidate ' + ads_candidate.length);
            console.log(ads_candidate);

            for(var k=0; k<ads_candidate.length; ++k) {
                casper.thenOpen(ads_candidate[k], function () {
                    this.echo('Second Page: ' + this.getTitle());
                    this.exit();
                });
            }
        });
    //});


});

casper.run();