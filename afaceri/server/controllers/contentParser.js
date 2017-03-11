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

//Import files
var config = require('./../config.json');

var keywords = {
  title: [
    {
      type: "LEGE",
      regex: "proiect ([a-zA-Z]+\s?\b){1,3}ordonan"
    },
    {
      type: "OUG",
      regex: "ordonan\S{1,2} de urgen\S{1,2}"
    }
  ]
};

function requestOption(url) {
  return {
    url:url,
    headers: {
      'User-Agent': config.userAgent
    }
  };
}

function getBodyfromURL(url, callback) {
  var options = requestOption(url);
  request(options, callback);
}


function retrieveArticleLinks (callback) {
  var links = [];
  getBodyfromURL('http://www.antreprenoriat.gov.ro/categorie/transparenta-decizionala/proiecte-in-dezbatere-publica/', function(err, response, body) {
    var $ = cheerio.load(body);
    var entry = $('.entry');

    entry.each(function(elementIndex, element) {
      async.each(element.children, function(item, callback) {
        if(item.attribs && item.attribs.href) {
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
  async.eachSeries(links, function(articleLink, callback) {
    getBodyfromURL(articleLink, function(err, body, response) {
      //get PDF file download link
      var $ = cheerio.load(response);
      var gdeText = $('.gde-text');
      gdeText.each(function(elementIndex, element) {
        async.each(element.children, function(item, callback) {
          if(item.attribs && item.attribs.href) {
            downloadLinks.push(item.attribs.href);
          }
          callback();
        });
      });
      callback();
    });
  }, function(err) {
    callback(err, downloadLinks);
  });
}

function processFiles(links, callback) {
  async.eachSeries(links, function(downloadLink, callback) {

    console.log('Downloading file from ' + downloadLink + '...');
    //var fileLocation = path.join(config.downloadsFolder, downloadLink.split('/').pop());
    var fileLocation = './downloads/' + downloadLink.split('/').pop();
    var fileStream = fs.createWriteStream(fileLocation);

    request.get(requestOption(downloadLink)).pipe(fileStream);
    fileStream.on('finish', function() {
      var pdfParser = new pdf2json(this, 1);
      pdfParser.on('pdfParser_dataError', function(err) {
        console.log(err.message);
      });
      pdfParser.on('pdfParser_dataReady', function(data) {
        console.log('Finished downloading file ' + downloadLink);
        var content = pdfParser.getRawTextContent();
        scrapFile(content, function(err) {
          if (err) {
            console.log(err.message);
          }
          callback();
        });
      });
      pdfParser.loadPDF(fileLocation);
    });
  }, callback);
}

function scrapFile(content, callback) {

  var result = {
    identifier: "lawproposal-first-document-name-slug-or-something", // un identificator unic, predictibil (repetabil), pereferabil human-readable
    title: "Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor", // titlul actului legislativ propus
    type: "HG", // HG, OG, OUG, PROIECT
    institution: "afaceri", // ID-ul platformei din care provine actul legislativ
    date: "2017-03-08", // ISO 8601
    description: "Cookie jelly-o sesame snaps donut sesame snaps sweet roll chocolate. Tootsie roll pie bonbon tart chocolate cake. Gummi bears gummies chupa chups ice cream croissant donut marzipan. Macaroon bear claw halvah carrot cake liquorice powder.",
    feedback_days: 12, // numarul zilelor disponibile pentru feedback
    contact: {
      tel: "12345",
      email: "feedback@example.org"
    } // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
  };

  //remove extra white spaces
  while(content.indexOf('  ') > -1) {
    content = content.replace('  ', ' ');
  }
  while(content.indexOf(' \r\n') > -1) {
    content = content.replace(' \r\n', '\r\n');
  }

  //retrieve title relevant words
  var paragraph = '';
  var inset = 0;
  var spaces = config.titleRelevantNumberOfWords - 1;
  while(spaces) {
    paragraph += content[inset];
    if(content[inset] == ' ') {
      spaces--;
    }
    inset++;
  }

  //search relevant keywords in title
  var keepGoing = true;
  for (var i=0; i<keywords.title.length && keepGoing; i++) {
    var currentRelevant = keywords.title[i];
    var re = new RegExp(currentRelevant.regex, 'i');
    if(re.test(paragraph)) {
      keepGoing = false;
      result.type = currentRelevant.type;
    }
  }
  console.log(paragraph);
}

function init() {
  retrieveArticleLinks(function(err, articleLinks) {
    retrieveDownloadLinks(articleLinks, function(err, downloadLinks) {
      //download and scrap files
      processFiles(downloadLinks, function(err, files) {
      })
    });
  });
}

module.exports = {
  init:init
};
