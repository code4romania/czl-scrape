let nightmareConfig = {show: true},
    cheerio = require('cheerio'),
    request = require('request'),
    parseProject = require('./parseProject'),
    secrets = require('./secrets.json') || {},
    parseResults = [];

const URL = 'http://economie.gov.ro/transparenta-decizionala/proiecte-in-dezbatere-publica',
    BASE = 'http://economie.gov.ro';


/** ====== MAIN ====== */

getNightmareInstance()
    .goto(URL)
    .wait('body')
    .evaluate(getPaginationHTMLContent)
    .end()
    .then(getPaginationURLArr)
    .then(getAndParsePageListItems)
    .then(postParsedResults)
    .catch(handleErrors);


/** ====== pagination ====== */

function getPaginationHTMLContent() {
    return document.querySelector('.pagination').innerHTML;
}

function getPaginationURLArr(result) {
    let pages = [URL];

    cheerio.load(result)('a')
        .each(function (i, link) {
            pages.push(BASE + link.attribs['href']);
        });

    return pages;
}


/** ====== list items ====== */

function getAndParsePageListItems(urlArr) {
    let getAndParsePromiseArr = [];

    urlArr.forEach(function (url, i) {
        let promise = getNightmareInstance()
            .wait(1000 * i)
            .goto(url)
            .wait('body')
            .evaluate(getBlogHTMLContent)
            .end()
            .then(parseListItems);

        getAndParsePromiseArr.push(promise);
    });

    return Promise.all(getAndParsePromiseArr);
}

function getBlogHTMLContent() {
    return document.querySelector('.blog').innerHTML;
}

function parseListItems(result) {
    let items = cheerio.load(result)('.items-row'),
        parseResults = [];

    items.each(function (i, item) {
        parseResults.push(parseItem(item));
    });

    return parseResults;
}

function parseItem(item) {
    return parseProject(cheerio.load(item), BASE);
}


/** ====== post ====== */

function postParsedResults(parsedResultsArr) {
    if (!(secrets.API_URL && secrets.TOKEN)) {
        throw new Error('Share your secrets with me. Pretty please :)');
    }

    let options = {
        uri: secrets.API_URL,
        method: 'POST',
        headers: {
            Authorization: 'Token ' + secrets.TOKEN
        },
        json: JSON.stringify(parsedResultsArr)
    };

    request(options, function (error, response, body) {
        if (error || response.statusCode !== 200) {
            throw new Error('POST failed :(', error);
        }

        console.log(response);
        console.log(result);
    });
}


/** ====== utils ====== */

function getNightmareInstance() {
    return require('nightmare')(nightmareConfig);
}

function handleErrors(error) {
    throw new Error(error);
}