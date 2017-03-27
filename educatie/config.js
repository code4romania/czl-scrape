module.exports = {
  api: {
    url: 'http://czl-api.code4.ro/api/publications/',
    token: 'educatie-very-secret-key'
  },
  scrape: {
    //url of the proposals listing page
    baseUrl: 'https://www.edu.ro/proiecte-acte-normative-0',
    //how many proposals to consider
    proposals: 20,
    defaultEmail: 'dgis@edu.gov.ro'
  }
};
