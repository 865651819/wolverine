/**
 * view
 */


var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true,
    logLevel: "debug"
});

casper.userAgent(casper.cli.get('ua'));
casper.log('ua is nidaye ' + casper.cli.get('ua'))

var INDEX = 1;
var urls = casper.cli.args;

function getRandomInt() {
    return Math.floor(Math.random() * (10000 - 3000)) + 3000;
}

casper.start(urls[0], function() {
    var ms = getRandomInt();
    casper.wait(ms, nextPage);
});

function nextPage() {

    if (INDEX > urls.length) {
        casper.exit();
    }

    casper.log('visit next page ' + urls[INDEX]);

    casper.thenOpen(urls[INDEX], function () {
        INDEX = INDEX + 1;
        var ms = getRandomInt();
        casper.wait(ms, nextPage);
    });
}

casper.run();