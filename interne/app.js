let nightmareConfig = {show: false},
    cheerio = require('cheerio'),
    request = require('request'),
    parseProject = require('./parseProject'),
    jsonfile = require('jsonfile'),
    argv = require('yargs').argv,
    secrets = require('./secrets.json') || {};

const URL = 'http://www.mai.gov.ro/index05_1.html',
    BASE = 'http://www.mai.gov.ro',
    FILE = 'data.json';

/** ====== MAIN ====== */

getNightmareInstance()
    .goto(URL)
    .wait('body')
    .evaluate(getHTMLContent)
    .end()
    .then(processHTMLContent)
    .then(parseListItems)
    .then(postParsedResults)
    .catch(handleErrors);


/** ====== page ====== */

function getHTMLContent() {
    return document.querySelector('.postBox').innerHTML;
}

function processHTMLContent(result) {
    console.log('processing html page...');

    let $ = cheerio.load(result, {normalizeWhitespace: true});

    let items = [];
    let counter = 0;
    $('.textPreview').children().each(function(index, element) {
        let $elem = cheerio.load(element);
        if(element.name == 'div' && $elem.text().replace(/\s+/, '').indexOf('Publicat') === 0) {
            counter++;
        }

        if(!items[counter]) {
            items[counter] = '';
        }

        items[counter] += $elem.html();
    });

    items.shift();
    return items;
}


/** ====== list items ====== */

function parseListItems(items) {
    let parseResults = [];

    items.forEach(function (item) {
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

    // console.log(parsedResultsArr);

    jsonfile.writeFileSync(FILE, parsedResultsArr, {spaces: 4});

    if (argv.post) {
        if (!(secrets.API_URL && secrets.TOKEN)) {
            throw new Error('Share your secrets with me. Pretty please :)');
        }

        console.log('posting data to api...');

        let requestsArr = [];
        parsedResultsArr.forEach(function (result, i) {
            let promise = new Promise(function (resolve, reject) {
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
                        console.error('request failed: ', response.body)
                    } else if (response.statusCode === 201) {
                        console.log('created: ', response.body)
                    }

                    resolve(body);
                })
            });

            requestsArr.push(promise);
        });

        Promise.all(requestsArr).then(function (response) {
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