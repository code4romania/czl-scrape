var Nightmare = require('nightmare');
var moment = require('moment');
var jsonfile = require('jsonfile');
var diacritics = require('diacritics');
var request = require('request-promise');

var nightmare = Nightmare({ show: true });

var pages = [];
var results = [];

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
    return request
      .post({
        url: 'http://czl-api.code4.ro/api/publications/',
        headers: {
          Authorization: 'Token educatie-very-secret-key'
        },
        json: data
      })
      .catch(function (err) {
        if (!err.message.match(/Integrity Error/)) {
          console.log('post err:', err.message);
          console.log('data:', data);
        }
      });
  } else {
    return Promise.resolve();
  }
}

function scrapePages() {
  return nightmare
    .goto('https://www.edu.ro/proiecte-acte-normative-0')
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
      pages = res.slice(0, 20);
    });
}

function scrapeContent() {
  console.log(pages.length, 'pages');

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
        email: 'dgis@edu.gov.ro'
      }
    };

    if (isFile(page.href)) {
      res.documents = [{
        type: getExtension(page.href),
        url: page.href
      }];

      results.push(res);

      return post(res)
        .then(scrapeContent);
    } else {
      console.log('scraping ' + page.href + '...');

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
          return {
            documents: documents,
            text: text
          };
        })
        .then(function(data) {
          res.description = data.text;
          res.documents = data.documents;

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
  .then(scrapeContent);
