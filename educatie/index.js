var Nightmare = require('nightmare');
var moment = require('moment');
var jsonfile = require('jsonfile');
var diacritics = require('diacritics');
var request = require('request-promise');
var config = require('./config');

var nightmare = Nightmare({ show: true });

var pages = [];
var results = [];
var count = 0;

function getType(title) {
  title = diacritics.remove(title)
    .toLowerCase()
    .replace(/ +/g, ' ')
    .replace(/&nbsp;/g, ' ');
  if (title.match(/^proiect(ul)? (de lege|l e g e)|^lege/)) {
    return 'LEGE';
  } else if (title.match(/^(proiect(ul)?|propunere) (de )?ordonanta de urgenta/)) {
    return 'OUG';
  } else if (title.match(/^proiect(ul)? de or?donanta/)) {
    return 'OG';
  } else if (title.match(/^proiect(ul)? (de )?hotarare/)) {
    return 'HG';
  } else if (title.match(/^proiect|^program/)) {
    return 'OM';
  }
  //throw 'not parsable: "' + title + '"';
  return null;
}

function getIdentifier(url) {
  var match = /^.*\/(.*?)(\..+)?$/.exec(url);
  return diacritics.remove(decodeURIComponent(match[1]))
    .toLowerCase()
    .replace(/\s+/g, '-');
}

function isFile(url) {
  return url.match(/\.([a-z]{3})$/i);
}

function getExtension(url) {
  var match = /\.([a-z]{3})$/i.exec(url);
  return match[1];
}

function parseTitle(title) {
  var res = {
    title: title,
    date: null
  };
  var match = /(.+)\(data public[aă]rii (\d+)\.(\d+)\.(\d+)\)?/.exec(title);
  if (match !== null) {
    res.title = match[1].trim();
    res.date = match[4] + '-' + match[3] + '-' + match[2];
  }
  return res;
}

function parseEmails(text) {
  var emails = [];
  var regex = /(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))/g;
  var match;
  while ((match = regex.exec(text)) !== null) {
    emails.push(match[0]);
  }
  return emails;
}

function post(data) {
  if (data.date === null) {
    delete data.date;
  }

  if (data.type !== null) {
    var token = process.env['API_TOKEN'] || config.api.token;
    return request
      .post({
        url: config.api.url,
        headers: {
          Authorization: 'Token ' + token
        },
        json: data
      })
      .then(function () {
        count++;
      })
      .catch(function (err) {
        if (!err.message.match(/Integrity Error/)) {
          console.error('post error:', err.message);
          console.error('post data:', data);
          throw err;
        }
      });
  } else {
    return Promise.resolve();
  }
}

function scrapePages() {
  return nightmare
    .goto(config.scrape.baseUrl)
    .evaluate(function () {
      return Array.prototype.slice.call(document.querySelectorAll('div.field-items ul li a'))
        .map(function (el) {
          return {
            href: el.href,
            title: el.innerHTML.replace(/\n|\t/g, '')
          };
        });
    })
    .then(function (res) {
      pages = res.slice(0, config.scrape.proposals);
    });
}

function scrapeContent() {
  //console.log(pages.length, 'proposals');

  if (pages.length > 0) {
    var page = pages.shift();
    var title = page.title
      .replace(/&nbsp;/g, ' ')
      .replace(/\s+/g, ' ');
    var parsedTitle = parseTitle(title);
    var res = {
      identifier: getIdentifier(page.href),
      title: parsedTitle.title,
      type: getType(page.title),
      institution: 'educatie',
      date: parsedTitle.date,
      feedback_days: 10,
      contact: {
        email: config.scrape.defaultEmail
      }
    };

    if (isFile(page.href)) {
      res.documents = [{
        type: getExtension(page.href),
        url: page.href
      }];
      res.url = config.scrape.baseUrl;

      results.push(res);

      return post(res)
        .then(scrapeContent);
    } else {
      console.log('scraping proposal page', page.href + '...');

      return nightmare
        .goto(page.href)
        .evaluate(function () {
          var documents = [];
          var text = '';
          [].slice.call(document.querySelectorAll('div.field-item p'))
            .forEach(function(el) {
              text += (el.innerText + "\n");
            });
          [].slice.call(document.querySelectorAll('span.file a'))
            .forEach(function(el) {
              documents.push({
                type: el.innerText,
                url: el.href
              });
            });
          var date = document.querySelector('span.date-display-single').innerText.split('.');
          return {
            documents: documents,
            text: text,
            date: date[2] + '-' + date[1] + '-' + date[0]
          };
        })
        .then(function(data) {
          res.description = data.text;
          res.documents = data.documents;
          res.date = data.date;
          res.url = page.href;

          var emails = parseEmails(data.text);
          for (var i = 0; i < emails.length; i++) {
            var key = 'email';
            if (i > 0) {
              key = key + (i + 1).toString();
              res.contact[key] = emails[i];
            }
          }

          results.push(res);

          return post(res)
            .then(scrapeContent);
        });
    }
  } else {
    return nightmare.end();
  }
}

scrapePages()
  .then(scrapeContent)
  .then(function() {
    console.log('done, imported', count, 'proposals');
  })
  .catch(function(err) {
    console.error('done with error:', err.message);
    return nightmare.end();
  });
