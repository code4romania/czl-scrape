const sha256 = require('sha256');
const rp = require('request-promise');
const Nightmare = require('nightmare');
const nightmare = Nightmare({ show: false, typeInterval: 2, waitTimeout: 5000 });

const YEAR_THRESHOLD = 2017;

const API_TOKEN = process.env['API_TOKEN'];

function guessType(text) {
  text = text.toLowerCase().trim();
  text = text.replace(/^proiect\s*/, '');
  if(text.match(/^ordonanță de urgență/)) return 'OUG';
  if(text.match(/^lege/)) return 'LEGE';
  if(text.match(/^ordin/)) return 'OG';
  if(text.match(/^hotărâre/)) return 'HG';
  throw new Error(`failz: ${text}`);
}

function parsePage(page = 1) {
    nightmare
      .cookies.clear()
      .useragent(`Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.${Math.round(Math.random()*100)}`)
      .goto(`http://www.mfinante.gov.ro/transparent.html?method=transparenta&pagina=acasa&locale=ro&d-6834775-p=${page}`)
      .wait("#transparentaList")
      .evaluate(()=> {
        if(document.querySelector('#transparentaList').innerText.trim() == '') return;
        let itemsList = [], items = [... document.querySelectorAll('#transparentaList > tbody > tr ')];
        for (let item of items) {
            let text = item.innerText;
            let match = text.replace(/\s+/g, ' ').match(
              /(.*?)\s*- publicat în data de\s*(\d{2})\.(\d{2})\.(\d{4})/);

            if(! match) {
              throw new Error(`Can't match title and date in text: "${text}"`);
            }

            let documents = []
            let links = item.querySelectorAll('a.downlPDF');
            for (let doc of links) {
              documents.push({
                type: 'act',
                url: doc.href
              });
            }

            let returnObj = {
                title: match[1],
                date: `${match[4]}-${match[3]}-${match[2]}`,
                documents: documents,
                label: links[0].innerText
            };

            itemsList.push(returnObj);
        }
        return itemsList;
      })
      .then((result) => {

        if(! result) {
          console.log("halt!");
          nightmare.halt();
          return;
        }

        let itemsList = [];

        for(let val of result) {
            let year = val.date.split('-')[0]
            if (year < YEAR_THRESHOLD) {
                console.log("halt!");
                nightmare.halt();
                return;
            }

            val.identifier = sha256(val.documents[0].url);
            val.institution = 'finantepub';
            val.description = '';
            val.type = guessType(val.label);
            delete val.label;
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
      .then(() => {
        parsePage(page + 1);
      })
      .catch((error) => {
        console.error('error:', error);
        nightmare.halt();
      });
}

parsePage();
