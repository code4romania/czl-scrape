class Arg:
    def __init__(self, short, long, help_text, action):
        self.short = short
        self.long = long
        self.help_text = help_text
        self.action = action

    short = None
    long = None
    help_text = None
    action = None


ARGS = dict(
    verbose=Arg('-v', '--verbose', "activate verbosity", 'store_true'),
    scraper=Arg(
        '-s', '--scraper', "pick the scraper that you want to run", None
    ),
)

SCRAPER_OPTIONS = [
    '2014-2015',
    '2016',
    'latest'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'
}

URLS = {
    'feed': 'https://www.mae.ro/node/2011#null',
    '2016': 'http://www.mae.ro/node/40248',
    '2014-2015': 'http://www.mae.ro/node/35609'
}

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

INSTITUTION = 'externe'

MAE_BASE_URL = 'http://www.mae.ro'

MANDATORY_FIELDS = ['identifier', 'title', 'published_at', 'article_type']

# POLITNESS = 1 #SECOUNDS
