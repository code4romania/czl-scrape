/**
 * Created by antoanetaopris on 11/03/17.
 */
//Import Express libs
var request = require('request');
var http = require('http');
var fs = require('fs');
var path = require('path');

//Import custom libs
var cheerio = require('cheerio');
var async = require('async');
var pdf2json = require('pdf2json');
var string = require('string');

//Import files
var config = require('./../config.json');
var keywords = require('./../config/keywords');

function requestOption(url) {
    return {
        url: url,
        headers: {
            'User-Agent': config.userAgent
        }
    };
}

function getBodyfromURL(url, callback) {
    var options = requestOption(url);
    request(options, callback);
}


function retrieveArticleLinks(callback) {
    var links = [];
    getBodyfromURL(config.mainURL, function (err, response, body) {
        var $ = cheerio.load(body);
        var entry = $('.entry');

        entry.each(function (elementIndex, element) {
            async.each(element.children, function (item, callback) {
                if (item.attribs && item.attribs.href) {
                    links.push(item.attribs.href);
                }
                callback();
            });
        });
        callback(null, links);
    });
}

function retrieveDownloadLinks(links, callback) {
    var downloadLinks = [];
    async.eachSeries(links, function (articleLink, callback) {
        getBodyfromURL(articleLink, function (err, body, response) {
            //get PDF file download link
            var $ = cheerio.load(response);
            var gdeText = $('.gde-text');
            gdeText.each(function (elementIndex, element) {
                async.each(element.children, function (item, callback) {
                    if (item.attribs && item.attribs.href) {
                        downloadLinks.push(item.attribs.href);
                    }
                    callback();
                });
            });
            callback();
        });
    }, function (err) {
        callback(err, downloadLinks);
    });
}

function processFiles(links, callback) {
    async.eachSeries(links, function (downloadLink, callback) {

        console.log('Downloading file from ' + downloadLink + '...');
        //var fileLocation = path.join(config.downloadsFolder, downloadLink.split('/').pop());
        var fileLocation = './downloads/' + downloadLink.split('/').pop();
        var fileStream = fs.createWriteStream(fileLocation);

        request.get(requestOption(downloadLink)).pipe(fileStream);
        fileStream.on('finish', function () {
            var pdfParser = new pdf2json(this, 1);
            pdfParser.on('pdfParser_dataError', function (err) {
                console.log(err.message);
            });
            pdfParser.on('pdfParser_dataReady', function (data) {
                console.log('Finished downloading file ' + downloadLink);
                var content = pdfParser.getRawTextContent();
                processFile(downloadLink, content, function (err, result) {
                    if (err) {
                        console.log("Error processing file: " + err.message);
                        //do not return error in callback, otherwise next files will not be processed
                        return callback();
                    }
                    //send result to api
                    request.post({
                        headers: {
                            'Authorization': config.APIKey
                        },
                        url: 'http://czl-api.code4.ro/api/publications/',
                        form: result
                    }, function (err, response) {
                        if (err) {
                            console.log("Error sending scrapped info to API: " + err.message);
                            //do not return error in callback, otherwise next files will not be processed
                        } else {
                            console.log("API response: " + response.body);
                        }
                        fs.unlink(fileLocation);
                        callback();
                    });
                });
            });
            pdfParser.loadPDF(fileLocation);
        });
    }, callback);
}

function scrapContent(content, callback) {
    //remove extra white spaces
    while (content.indexOf('  ') > -1) {
        content = content.replace('  ', ' ');
    }

    //normalize text in paragraphs
    var lines = string(content).lines();
    var paragraphs = [];
    var paragraph = "";
    var firstImportantParagraph, docType, title;
    while (lines.length) {
        var line = lines.shift().replace(/[\-]*?Page \(\d{1,}\) Break[\-]*?(?!-)/, '').trim();
        if (line.length) {
            paragraph += line + ' ';
        } else {
            if (paragraph.length) {
                paragraphs.push(paragraph);
                if (!firstImportantParagraph) {
                    //scan paragraph to determine type: HG/OUG/etc
                    if (!docType) {
                        var keepGoing = true;
                        for (var i = 0; i < keywords.docType.length && keepGoing; i++) {
                            if (keywords.docType[i].regex.test(paragraph)) {
                                docType = keywords.docType[i].type;
                                keepGoing = false;
                            }
                        }
                    }

                    //determine first important paragraph as a number of minimum words and letters
                    if (paragraph.split(' ').length >= config.firstParagraphMinWords && paragraph.length >= config.firstParagraphMinLetters) {
                        firstImportantParagraph = paragraph;

                        //once first paragraph is found, retrieve title from it
                        var startIndex = paragraph.length - 1;
                        for (var i = 0; i < keywords.titleStartMarkStrings.length; i++) {
                            var previousStartIndex = startIndex;
                            var startIndex = paragraph.indexOf(keywords.titleStartMarkStrings[i]);
                            if (startIndex > -1) {
                                //found keyword where title starts
                                if (startIndex > previousStartIndex && previousStartIndex > -1)
                                    continue;

                                var startContent = paragraph.substring(startIndex + keywords.titleStartMarkStrings[i].length, paragraph.length - 1);

                                //find position where title ends as first match of the string end keyword
                                var endIndexBasedOnString = startContent.length;
                                for (var j = 0; j < keywords.titleEndMarkStrings.length; j++) {
                                    var prevIndex = endIndexBasedOnString;
                                    endIndexBasedOnString = startContent.indexOf(keywords.titleEndMarkStrings[j]);
                                    if (endIndexBasedOnString < 0 || (endIndexBasedOnString > prevIndex && prevIndex > -1)) {
                                        endIndexBasedOnString = prevIndex;
                                    }
                                }

                                //find position where title ends as first match of the regex end keyword
                                var endIndexBasedOnRegex = startContent.length;
                                for (var j = 0; j < keywords.titleEndMarkRegex.length; j++) {
                                    var prevIndex = endIndexBasedOnRegex;
                                    var matches = startContent.match(keywords.titleEndMarkRegex[j]);
                                    if (matches) {
                                        endIndexBasedOnRegex = startContent.indexOf(matches[0]);
                                        if (endIndexBasedOnRegex < 0 || (endIndexBasedOnRegex > prevIndex && prevIndex > -1)) {
                                            endIndexBasedOnRegex = prevIndex;
                                        }
                                    }
                                }

                                var finalEndIndex = (endIndexBasedOnRegex * endIndexBasedOnString < 0) ? Math.max(endIndexBasedOnRegex, endIndexBasedOnString) :
                                    Math.min(endIndexBasedOnRegex, endIndexBasedOnString);
                                title = startContent.substring(0, finalEndIndex).trim();
                            }
                        }
                    }
                }
            }
            paragraph = '';
        }
    }
    var newContent = '';
    for (var i = 0; i < paragraphs.length; i++) {
        newContent += paragraphs[i] + '\n';
    }
    callback(null, newContent, firstImportantParagraph, docType, title);
}

function processFile(downloadLink, content, callback) {

    scrapContent(content, function (err, newContent, firstImportantParagraph, docType, title) {
        var id = title.split(',').join('');
        id = id.split(' ').join('-');
        id = string(id).latinise().s;
        var result = {
            identifier: id.substring(0, 128), //hack si nu e frumos, dar incercam
            title: title,
            type: docType,
            institution: "afaceri",
            date: "2017-03-20", //date is not retrievable from document
            description: title,
            feedback_days: 30, //set default, there's no source to retrieve this value
            contact: {
                tel: "021.202.54.36",
                email: "contact@antreprenoriat.gov.ro",
                addr: "Calea Victoriei 152, Sector 1, Bucuresti"
            },
            documents: [
                {
                    url: downloadLink,
                    type: "anexa"
                }
            ]
        };

        callback(null, result);
    });
}

function init() {
    retrieveArticleLinks(function (err, articleLinks) {
        retrieveDownloadLinks(articleLinks, function (err, downloadLinks) {
            //download and scrap files
            processFiles(downloadLinks, function (err, files) {
            })
        });
    });
}

module.exports = {
    init: init
};
