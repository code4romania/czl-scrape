let nightmareConfig = {show: false},
    cheerio = require('cheerio'),
    request = require('request'),
    parseProject = require('./parseProject'),
    jsonfile = require('jsonfile'),
    argv = require('yargs').argv,
    secrets = require('./secrets.json') || {},
    parseResults = [];

const URL = 'http://economie.gov.ro/transparenta-decizionala/proiecte-in-dezbatere-publica',
    BASE = 'http://economie.gov.ro';

const FILE = 'data.json';

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
    console.log('processing pages...');
    let pages = [URL];

    cheerio.load(result)('a')
        .each(function (i, link) {
            pages.push(BASE + link.attribs['href']);
        });

    return pages;
}


/** ====== list items ====== */

function getAndParsePageListItems(urlArr) {
    console.log('processing items...');
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

    return Promise.all(getAndParsePromiseArr).then(function (result) {
        let itemsArray = [];
        result.forEach(function (items) {
            itemsArray = itemsArray.concat(items);
        });

        return itemsArray;
    }).catch(function (err) {
        throw new Error(err);
    });
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

    console.log('saving data to file...');

    jsonfile.writeFileSync(FILE, parsedResultsArr, {spaces: 4});

    if (argv.post) {
        if (!(secrets.API_URL && secrets.TOKEN)) {
            throw new Error('Share your secrets with me. Pretty please :)');
        }

        console.log('posting data to api...');

        let requestsArr = [];

        parsedResultsArr.forEach(function (result, i) {
            let promise = new Promise(function(resolve, reject) {
                request({
                    uri: secrets.API_URL,
                    method: 'POST',
                    headers: {
                        'Authorization': 'Token ' + secrets.TOKEN,
                        'Content-Type': 'application/json'
                    },
                    json: result
                }, function (error, response, body) {
                    if (error || response.statusCode !== 200) {
                        console.error('request failed: ', error)
                    }

                    resolve(body);
                })
            });

            requestsArr.push(promise);
        });

        Promise.all(requestsArr).then(function(response) {
            console.log('done!');
            process.exit(0);
        }).catch(function (err) {
            throw new Error(err);
        });
    } else {
        console.log('done!');
        process.exit(0);
    }
}


/** ====== utils ====== */

function getNightmareInstance() {
    return require('nightmare')(nightmareConfig);
}

function handleErrors(error) {
    throw new Error(error);
}