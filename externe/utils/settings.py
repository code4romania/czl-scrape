WAIT = {
    '1_sec': 1,
    '0.5_sec': 0.5
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Token externe-very-secret-key'
}

SCRAPER_PAGES = [
    'arhiva-1415',
    'arhiva-2016',
    'feed'
]

# The keys linking to MAE pages need to match the items in SCRAPER_PAGES
URLS = {
    'mae_base': 'http://www.mae.ro',
    'feed': 'https://www.mae.ro/node/2011#null',
    'arhiva-2016': 'http://www.mae.ro/node/40248',
    'arhiva-1415': 'http://www.mae.ro/node/35609',
    'api-publications': 'http://czl-api.code4.ro/api/publications/'
}

STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
ALREADY_EXISTS = 'already exists'

TYPES = {
    'HOTARARE': 'HG',
    'ORDONANTA': 'OG',
    'ORDONANTA DE URGENTA': 'OUG',
    'ORDINUL MINISTRULUI AFACERILOR EXTERNE': 'OM',
    'ORDIN': 'OM',
    'PROIECT DE LEGE': 'LEGE',
    'LEGE': 'LEGE',
    'OTHER': 'OTHER'
}

MONTHS = dict(
    ianuarie='01',
    februarie='02',
    martie='03',
    aprilie='04',
    mai='05',
    iunie='06',
    iulie='07',
    august='08',
    septembrie='09',
    octombrie='10',
    noiembrie='11',
    decembrie='12'
)

CLICK_HELPER = {

    'log-level': '\b Sets the logging level. Available values: ERROR, WARNING, INFO, DEBUG,',
    'page': """
\b Selects the page to scrape. Available options are:
\b <feed> scrapes the latest articles and falls back to observer mode
____________________________________________________
\b <arhiva-2016> scrape the 2016 archive and switch to observer mode
____________________________________________________
\b <arhiva-1415> scrape the 2014-2015 archive and switch
   to observer mode
____________________________________________________
            """,
    'observer': 'Periodically checks for changes and scrapes them if available. '
                'NOTE: in observer mode, any <page> argument is ignored.',
    'delay': 'Number of hours to wait before checking for changes. Default=1'
}

LOG_LEVELS = {
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10
}

LOG_FILE = 'logs/scraper.log'

INSTITUTION = 'externe'

MANDATORY_FIELDS = ['identifier', 'title', 'published_at', 'article_type']

DATE_FMT = '%Y-%m-%d'


def hours_to_sec(hours):
    return hours * 3600
