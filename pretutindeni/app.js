var nightmare = require('nightmare')({ show: false }),
    cheerio = require('cheerio');

function parseParagraph(paragraph) {
    "use strict";


}

nightmare
    .goto('http://www.dprp.gov.ro/documente-in-consultare-publica/')
    .evaluate(function() {
        return document.querySelector('#principal .entry-content').innerHTML;
    })
    .end()
    .then(function(result) {
        var $ = cheerio.load(result
            .replace(/\n/g,'')
            .replace(/\r/g,'')
            .replace(/\t/g,''));

        var paragraphs = $('p');

        var projects = [];
        var projectsCounter = 0;
        for(var i = 0; i < paragraphs.length; i++) {
            if(paragraphs[i].innerHTML == '—————–') {
                projectsCounter++;
            } else {
                if(!projects[projectsCounter]) projects[projectsCounter] = [];
                projects[projectsCounter].push(paragraphs[i])
            }
        }

        console.log($.html());
    })
    .catch(function(error) {
        throw new Error(error);
    });
