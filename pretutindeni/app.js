var nightmare = require('nightmare')({ show: true });

nightmare
    .goto('http://www.dprp.gov.ro/')
    .evaluate(function() {
        return document.querySelector('#slider').innerHTML;
    })
    .end()
    .then(function(result) {
        console.log(result);
    })
    .catch(function(error) {
        throw new Error(error);
    });
