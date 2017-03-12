const moment = require('moment');
const sha256 = require('sha256');
const rp = require('request-promise');
const Nightmare = require('nightmare');
const nightmare = Nightmare({ show: false, typeInterval: 2, waitTimeout: 5000 });

const URL = 'http://www.madr.gov.ro/transparenta-decizionala/proiecte-de-acte-normative.html';
const YEAR_THRESHOLD = 2017;

const API_TOKEN = process.env['API_TOKEN'];

function guessType(text) {
    const replaceMap = [
        [/ș/g, 's'],
        [/ş/g, 's'],
        [/ț/g, 't'],
        [/ţ/g, 't'],
        [/ă/g, 'a'],
        [/î/g, 'i'],
        [/â/g, 'a'],
    ];
    text = text.toLowerCase();
    for(let [orig, repl] of replaceMap) {
        text = text.replace(orig, repl);
    }

    if (text.match(/^o\s?r\s?d\s?o\s?n\s?a\s?n\s?t\s?a\s+d\s?e\s+u\s?r\s?g\s?e\s?n\s?t\s?a /)) return 'OUG';
    if (text.match(/^o\s?r\s?d\s?o\s?n\s?a\s?n\s?t\s?a /)) return 'OG';
    if (text.match(/^h\s?o\s?t\s?a\s?r\s?a\s?r\s?e /)) return 'HG';
    if (text.match(/^o\s?r\s?d\s?i\s?n /)) return 'OM';
    return 'LEGE';
}

function parsePage(firstFlag) {
    if (firstFlag) {
        nightmare
          .goto(URL);
    } else {
        nightmare
          .click('.pagination .next');
    }

    nightmare
      .wait("#itemListPrimary .itemContainer")
      .evaluate(()=> {
        let itemsList = [], items = [... document.querySelectorAll('#itemListPrimary .itemContainer')];
        for (let item of items) {
            let introText = item.querySelector(".catItemIntroText");
            let emHTML = introText.querySelector("em");
            if (emHTML !== null) {
                emHTML.remove();
            }

            let returnObj = {
                title: introText.innerText,
                date: item.querySelector(".catItemDateCreated").innerText,
                documents: [...item.querySelectorAll(".catItemAttachments a")].map((elem)=> {
                    return {
                        type: "act",//elem.title,
                        url: elem.href
                    }

                })
            };

            itemsList.push(returnObj);
        }
        return itemsList;
      })
      .then((result) => {

        let itemsList = [];

        for(let val of result) {
            let date = moment(val.date, 'ddd, DD MMMM YYYY HH:mm', 'ro');
            let year = date.year();
            if (year < YEAR_THRESHOLD) {
                console.log("halt!");
                nightmare.halt();
                return;
            }

            let identifier = sha256(val.title);
            val.date = date.format('YYYY-MM-DD');
            val.identifier = identifier;
            val.institution = 'agricultura';
            val.description = val.title;
            val.type = guessType(val.title);
            itemsList.push(val);
        }

        function postAllItems(remaining) {
            if(! remaining.length) return;
            let val = remaining[0];
            return rp.post({
                url: 'http://czl-api.code4.ro/api/publications/',
                headers: {Authorization: `Token ${API_TOKEN}`},
                json: val
            })
            .then(() => {
                console.log('posted item: ', val.identifier);
                return postAllItems(remaining.slice(1));
            });
        }

        return postAllItems(itemsList);

      })
      .then((result) => {
        nightmare.evaluate(function () {
            let returnValue = document.querySelector('.pagination .next');
            return returnValue !== null;
        })
        .then(function(goNextFlag) {
            setTimeout(function() {
                if (goNextFlag) {
                    parsePage(false);
                }else {
                    console.log("halt!");
                    nightmare.halt();
                }
            }, 0);
        });
      })
      .catch((error) => {
        console.error('error:', error);
        nightmare.halt();
      });
}

parsePage(true);
// http://www.madr.gov.ro/transparenta-decizionala/proiecte-de-acte-normative.html?start=520
