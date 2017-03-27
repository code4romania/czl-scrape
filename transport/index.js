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
  title = diacritics.remove(title).toLowerCase().replace(/ +/g, ' ');
  if (title.match(/proiectul (de lege|l e g e)/)) {
    return 'LEGE';
  } else if (title.match(/proiect(ul)? de ordin/)) {
    return 'OM';
  } else if (title.match(/proiect(ul)? de ordonanta de urgenta/)) {
    return 'OUG';
  } else if (title.match(/proiect(ul)? de or?donanta/)) {
    return 'OG';
  } else if (title.match(/proiect(ul)? de hotarare/)) {
    return 'HG';
  } else if (title.match(/proiectul pentru modificarea/)) {
    console.log(title, '- HG');
    return 'HG';
  }
  throw 'not parsable: "' + title + '"';
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
      .then(function() {
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
      return Array.prototype.slice.call(document.querySelectorAll('td.list-title a'))
        .map(function (el) {
          return {
            href: el.href,
            title: el.innerHTML.replace(/\n|\t/g, '')
          };
        });
    })
    .then(function(res) {
      pages = pages.concat(res);
      return navigateToNextPage();
    });

  function navigateToNextPage() {
    return nightmare
      .evaluate(function () {
        return document.querySelector('ul.jsn-pagination > span').innerText;
      }).then(function (res) {
        console.log('scraping listing page', res);
        if (res < config.scrape.pages) {
          return nightmare
            .evaluate(function () {
              var pag = document.querySelectorAll('ul.jsn-pagination li a');
              var i;
              for (i = 0; i < pag.length; i++) {
                if (pag[i].innerText === '>') {
                  break;
                }
              }
              var ev = document.createEvent('MouseEvent');
              ev.initEvent('click', true, true);
              pag[i].dispatchEvent(ev);
            })
            .evaluate(function () {
              return Array.prototype.slice.call(document.querySelectorAll('td.list-title a'))
                .map(function (el) {
                  return {
                    href: el.href,
                    title: el.innerHTML.replace(/\n|\t/g, '')
                  };
                })
            })
            .then(function(res) {
              pages = pages.concat(res);
              return navigateToNextPage();
            });
        }
      });
  }
}

function scrapeContent() {
  if (pages.length > 0) {
    var page = pages.shift();
    console.log('scraping proposal page', page.href + '...');
    return nightmare
      .goto(page.href)
      .evaluate(function() {
        var data = {
          contact: {
            addr: null,
            fax: null,
            email: null
          },
          date: null,
          documents: [],
          end_date: null
        };
        var state = 'TEXT';
        Array.prototype.forEach.call(document.querySelectorAll('p'),
          function(el) {
            if (state === 'TEXT') {
              var text = el.innerText;

              var match = /Data publicării: (\d+).(\d+).(\d+)/.exec(text);
              if(match !== null) {
                data.date = match[3] + '-' + match[2] + '-' + match[1];
              }

              match = /Data limită.*: (\d+).(\d+).(\d+)/.exec(text);
              if(match !== null) {
                data.end_date = match[3] + '-' + match[2] + '-' + match[1];
              }

              match = /Documente supuse consultării/.exec(text);
              if (match !== null) {
                state = 'DOCS';
              }

              match = /Prin poştă la adresa (.*)/.exec(text);
              if (match !== null) {
                data.contact.addr = match[1];
              }

              match = /Prin fax la numărul de telefon (.*)/.exec(text);
              if (match !== null) {
                data.contact.fax = match[1];
              }

              match = /Prin poşta electronică la adresa (.*)/.exec(text);
              if (match !== null) {
                data.contact.email = match[1];
              }
            } else if(state === 'DOCS') {
              var a = el.querySelector('a');
              if (a !== null) {
                var type = a.innerText.trim();
                if (type !== '') {
                  data.documents.push({
                    type: type,
                    url: a.href
                  });
                }
              } else {
                state = 'TEXT';
              }
            }
          }
        );
        return data;
      })
      .then(function(res) {
        var href = page.href;
        res.description = page.title;
        res.identifier = 'mt-' + href.substr(href.lastIndexOf('/') + 1);
        res.institution = 'transport';
        res.feedback_days = moment(res.end_date).diff(moment(res.date), 'days') - 1;
        res.title = page.title;
        res.type = getType(page.title);
        res.url = href;
        results.push(res);
        return post(res)
          .then(scrapeContent);
      });
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
