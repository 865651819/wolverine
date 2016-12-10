/**
 * click
 */


var casper = require("casper").create({
    webSecurityEnabled: false,
    verbose: true,
    logLevel: "debug"
});

var INDEX = 1;
var urls = casper.cli.args;

function getRandomInt() {
    return Math.floor(Math.random() * (10000 - 1000)) + 1000;
}

casper.start(urls[0]);

function nextPage() {

    if (INDEX > urls.length) {
        casper.echo('Complete visiting, exiting...');
        casper.exit();
    }

    casper.thenOpen(urls[INDEX], function() {
        casper.echo('LINK ' + urls[INDEX]);
        INDEX = INDEX + 1;
        var ms = getRandomInt();
        casper.echo('Waiting ms ' + ms);
        casper.wait(ms, nextPage);
    });
}

casper.then(function () {
    var ms = getRandomInt();
    casper.echo('Waiting ms ' + ms);
    casper.wait(ms, nextPage);
});

casper.run();