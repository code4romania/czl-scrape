const Nightmare = require('nightmare');
const nightmare = Nightmare({ show: false, typeInterval: 2, waitTimeout: 5000 });

const YEAR_THRESHOLD = 2017;

function parsePage(page = 1) {
    nightmare
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
            for (let doc of item.querySelectorAll('a.downlPDF')) {
              documents.push({
                type: 'act',
                url: doc.href
              });
            }

            let returnObj = {
                title: match[1],
                date: `${match[4]}-${match[3]}-${match[2]}`,
                documents: documents
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

            // TODO upload to API
            console.log(val);
        }

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
