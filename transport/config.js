module.exports = {
  api: {
    url: 'http://czl-api.code4.ro/api/publications/',
    token: 'educatie-very-secret-key'
  },
  scrape: {
    //url of the proposals listing page
    baseUrl: 'http://mt.gov.ro/web14/transparenta-decizionala/consultare-publica/acte-normative-in-avizare',
    //number of listing pages to scrape
    pages: 2
  }
};
