# Scrapere scrise cu scrapy

O colecție de scrapere implementate folosind [scrapy](https://scrapy.org).
Fiecărei instituții îi corespunde un scraper care descarcă publicații de pe site.
Mai departe, publicațiile sunt validate într-un pipeline comun, și trimise la
[api](http://czl-api.code4.ro).

## Spidere implementate
* [`dialog`](czlscrape/spiders/dialog.py) - Ministerul Consultărilor Publice și
  Dialogului Social

## Instrucțiuni
* Ai nevoie de python3, preferabil cu un
  [virtualenv](https://virtualenv.pypa.io).

* Instalezi dependențele:
   ```sh
   pip install -r requirements.txt
   ```

* Configurezi variabile de mediu:
   ```sh
   export API_TOKEN='the secret token'
   export SENTRY_DSN='the sentry dsn' # opțional
   ```

* Rulezi unul din spidere:
   ```sh
   scrapy crawl dialog
   ```

* După ce faci schimbări în cod, rulezi testele:
   ```sh
   pytest
   ```
