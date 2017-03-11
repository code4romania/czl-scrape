import requests
from bs4 import BeautifulSoup as bs
import scraper.settings as settings


def fetch_page(page_url):
  page = requests.get(page_url, headers=settings.HEADERS)
  return bs(page.text, 'html.parser')


def extract(content):
  tables = content.select_one('div.art').select('table')
  for t in tables:
    '''
    "identifier": "lawproposal-first-document-name-slug-or-something",
    // un identificator unic, predictibil (repetabil), pereferabil
    human-readable
    '''
    # "type": "HG", // HG, OG, OUG, PROIECT
    # contact
    instituion = 'externe'
    description = ''
    title = t.select('tr')[0].select('td')[0].text.strip().replace('\n', ' ')
    documents = [
      dict(
        type='Decizie - anexa',
        url=t.select('tr')[0].select('td > p > a')[0].attrs['href']
      ),
      dict(
        type='Nota de fundamentare - anexa',
        url=t.select('tr')[1].select('td > p > a')[0].attrs['href']
      )
    ]
    published = t.select('tr')[2].select('td')[0].select('p')[1].text \
      .split(' ')[1].replace('\xa0', ' ')
    print('title: %s \n url: %s \n published: %s \n\n' % (title, documents, published))


def parse_page(page_url):
  content = fetch_page(page_url)
  extract(content)
