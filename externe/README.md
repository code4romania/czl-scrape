# Ministerul Afacerilor Externe

## Tehnologie
- Python 3 (developed and tested on 3.5.2)
- BeautifulSoup 4
- Requests
- Click
- **E**xtraordinarily **U**nderwhelming but also **S**uper **E**levated **B**inary **I**nformation **U**nit. 

  A.K.A Eusebiu.

## Instructiuni
Pentru a-l convinge pe Eusebiu să ia la mână articolele de pe site-ul MAE, trebuie să: 
- Instalezi `python3` si `pip`
- Rulezi `python3 setup.py install` sau cu `sudo` in fata, daca nu ai un virtualenv
- Ca să aflii ce poate Eusebiu să facă pentru umanitate: `python eusebiu.py --help`:
```
Options:
  --page TEXT       Selects the page to scrape. Available options are:
                    
                    <feed> scrapes the latest articles and falls back to
                    observer mode
                    ____________________________________________________
                    
                    <arhiva-2016> scrape the 2016 archive and switch to
                    observer mode
                    ____________________________________________________
                    
                    <arhiva-2014> scrape the 2014-2015 archive and switch
                    to observer mode
                    ____________________________________________________
  --log_level TEXT  Sets the logging level. Available values: ERROR,
                    WARNING, INFO, DEBUG,
  --delay FLOAT     Number of hours to wait before checking for changes.
                    Default=1
  --observer        Periodically checks for changes and scrapes them if
                    available.
  --help            Show this message and exit.
```
## Exceptii
Eusebiu se bazeaza in mare parte pe regex-uri pentru a extrage (silit, sau nu) informatii
de la MAE. 

In cazul in care persoanele responsabil pentru introducerea articolelor in sistem 
se decid subit sa foloseasca alte pattern-uri decat cele pe le intelege Eusebiu, scraperul va
genera articole invalide. Daca un articol nu contine toate detalii obligatorii, Eusebiu nu-i va 
face POST la API.
