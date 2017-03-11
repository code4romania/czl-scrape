var nightmareConfig = { show: false },
    cheerio = require('cheerio'),
    parseFunction = require('./parseProject');

var URL = 'http://economie.gov.ro/transparenta-decizionala/proiecte-in-dezbatere-publica',
    BASE = 'http://economie.gov.ro';

function parseItem(item) {
    parseFunction(item, BASE);
}

require('nightmare')(nightmareConfig)
    .goto(URL)
    .wait('body')
    .evaluate(function () {
        return document.querySelector('.pagination').innerHTML;
    })
    .end()
    .then(function (result) {
        var pages = [URL];
        cheerio.load(result)('a').each(function (i, link) {
            pages.push(BASE + link.attribs['href']);
        });

        return pages;
    })
    .then(function (result) {
        result.forEach(function (page) {
            require('nightmare')(nightmareConfig)
                .goto(page)
                .wait('body')
                .evaluate(function () {
                    return document.querySelector('.blog').innerHTML;
                })
                .end()
                .then(function (result) {
                    var items = cheerio.load(result)('.items-row');
                    items.each(function(i, item) {
                        parseItem(item);
                    });
                });
        });
    })
    .catch(function (error) {
        throw new Error(error);
    });