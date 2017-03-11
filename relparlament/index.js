var Nightmare = require('nightmare');
var nightmare = Nightmare({ show: false });
var request = require('request');
var cheerio = require('cheerio');

const URL = "http://mrp.gov.ro/web/category/consultare-publica/";
nightmare
    .goto(URL)
    .wait("article")
    .evaluate( () => {
        return [... document.querySelectorAll('article')].map(elem => {
            var postCategory = elem.querySelector('.post-category').innerText;
            var timestamp = elem.querySelector('time').getAttribute('datetime');
            var titlu = elem.querySelector('.post-title a').innerText;
            var detailLink = elem.querySelector('.post-title a').getAttribute('href');

            // request(detailLink, function(err, resp, body){
            //     var $ = cheerio.load(body);
            //     var linkElement = $('.post-inner a');
            //     var link = linkElement.attr('href');
            //     console.log(link);
            //
            //     });

            result = {
                postcat:postCategory,
                timestamp : timestamp,
                titlu : titlu,
                link : detailLink,

            };

            return result;


        }
        )

})
    .end()

    .then(function (result) {
        var count = 0;
        result.forEach(function(item) {
           require('nightmare')({show: false})
               .goto(item.link)
               .wait("a")
               .evaluate((uri) => {
                   var docLinks = {};
                   docLinks[uri] = [];
                   [... document.querySelectorAll('.entry-inner a[target="_blank"]')].map( (aHref) => {
                       docLinks[uri].push(aHref.href);
                   });

                   [... document.querySelectorAll('.entry-inner a.gde-link')].map( (aHref) => {
                       docLinks[uri].push(aHref.href);
                   });

                   return docLinks;
               },item.link)
               .end()
               .then(function (res) {
                   count++;
                   result.map((value)=> {
                       for(let key in res) {
                           if(key == value.link) {
                               value.docLinks = res[value.link];
                               break;
                           }
                       }
                   });

                   if(result.length == count) {
                       console.log("DONE: ", result);
                   }
                   // finalJson = result;
                    // console.log("result: ", result);
                   // console.log(result);
                   // result.docLinks.map((element) => {console.log("PAGE LINKS " ,element)})

               });

        });
        // console.log("final: ", finalJson);

    });