import time
import click
import logging

from scraper.article_serializer import ArticleSerializer
from scraper.extractor import *
from utils.api_client import post_data
from utils.settings import *


@click.command()
@click.option('--page', default='feed', help=CLICK_HELPER['page'])
@click.option('--log_level', default='INFO', help=CLICK_HELPER['log-level'])
@click.option('--delay', default=1, type=float, help=CLICK_HELPER['delay'])
@click.option('--observer', is_flag=True, default=False,
              help=CLICK_HELPER['observer'])
def get_to_work(page, delay, observer, log_level):
    # init logging
    if log_level not in LOG_LEVELS:
        logging.warning('Unrecognized log_level: %s. Defaulting to INFO')
        log_level = 'INFO'
    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVELS[log_level],
                        format='%(asctime)s %(levelname)s %(message)s')

    # if observer flag is set, ignore everything else and start eavesdropping
    if observer:
        shut_up_and_listen(delay)

    # validate page selection
    if page not in SCRAPER_PAGES:
        logging.error('Page name: %s not recognized. See help for available pages', page)
        exit()

    # scrape all articles on this page, and dump them on the API
    dump_one_of_these(page)

    # then get back to eavesdropping
    shut_up_and_listen(delay)


def shut_up_and_listen(delay):
    """ Eusebiu skillfully lurks in the shadows, waiting for a new article to be posted.
    :param delay: int: number of hours to wait before the next tactical strike.
    :return: None
    """
    current_latest = []
    while True:
        feed_extractor = Extractor(settings.URLS.get('feed'))
        latest_entries = feed_extractor.get_identifier_list()
        logging.debug('latest_entries: %s', latest_entries)

        if not current_latest:
            logging.info('Assuming current state of feed is the latest ...')
            current_latest = latest_entries[:]

        diff = set(current_latest) - set(latest_entries)
        for identifier in diff:
            # be polite to the MAE website
            time.sleep(0.5)
            logging.info('Found new article: %s', identifier)
            article = feed_extractor.get_article_by_id(identifier)
            diff.remove(article.identifier)
            post_article(article)

        logging.info('ETA until next scrape: %s hour(s)', delay)
        time.sleep(hours_to_sec(delay))


def dump_one_of_these(page):
    """
    Eusebiu masterfully extracts all the articles on a given page, and swiftly dumps
    them onto the API.
    :param page: the page to eviscerate.
    :return: None
    """
    extractor = Extractor(settings.URLS.get(page))
    articles = extractor.get_all_articles()
    for article in articles:
        # be polite to the API
        time.sleep(0.5)
        post_article(article)


def post_article(article):
    """Attempts to POST and article to the API.
    :param article: the object to POST.
    :return: True if successful, False otherwise.
    """
    if not ArticleSerializer().is_valid(article):
        logging.error('Invalid article: %s \n WILL NOT POST TO API', article)
        return False
    data = ArticleSerializer().serialize(article)
    return post_data(data)


if __name__ == '__main__':
    get_to_work()
