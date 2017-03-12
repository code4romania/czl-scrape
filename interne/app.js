let nightmareConfig = {show: false},
    cheerio = require('cheerio'),
    request = require('request'),
    parseProject = require('./parseProject'),
    jsonfile = require('jsonfile'),
    argv = require('yargs').argv,
    secrets = require('./secrets.json') || {};

const URL = 'http://www.research.gov.ro/ro/articol/1029/despre-ancs-legislatie-proiecte-de-acte-normative',
    BASE = 'http://www.research.gov.ro';

const FILE = 'data.json';

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
    return document.querySelector('.icr_main .special_edit').innerHTML;
}

function processHTMLContent(result) {
    console.log('processing html page...');

    return {
        feedback_days_element: cheerio.load(result)('p').children('a[href^=mailto]').parent()[0],
        items: cheerio.load(result)('table tbody tr') //.not(function(item) {return cheerio.load(item).text() && cheerio.load(item).text().indexOf('Data publicarii') === -1})
    };
}


/** ====== list items ====== */

function parseListItems(resultObject) {
    let items = resultObject.items,
        parseResults = [];

    items.each(function (i, item) {
        let $ = cheerio.load(item),
            content = $.text().replace(/\n/g, '').replace(/\t/g, '');

        if(content && content.indexOf('Data publicarii') != 0) {
            parseResults.push(parseItem(resultObject.feedback_days_element, item));
        }
    });

    return parseResults;
}

function parseItem(feedback_days, item) {
    return parseProject(cheerio.load(item), BASE, cheerio.load(feedback_days));
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
                        console.error('request failed: ', error)
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