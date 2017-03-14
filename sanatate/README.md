# Ministerul Sănătăţii
Crawler simplu, de la țară, făcut cu scrapy. Nu știe bine românește, dar înțelege oricum (face fuzzy matching pe titluri ca să scoată tipul de act normativ).
## Tehnologie
- python3, pip
- scrapy, fuzzywuzzy, urllib3
- python-Levenshtein [opțional]

## Instructiuni
Bagi chestii în _credentials.json_, după care un clasic _pip install -r requirements.txt_ și un clasic _scrapy crawl sanatate_.
## Exceptii
Detectarea tipului de act normativ nu e perfectă, și nici a tipului de documente. Asta e o problemă mai mare, și nu are sens să o tratăm doar într-un singur crawler.
