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
