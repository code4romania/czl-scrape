import argparse
import requests

from scraper.engine import *
from scraper.settings import *
from scraper.serializer import *


def main():
  arg_parser = argparse.ArgumentParser()
  for arg in ARGS.values():
    arg_parser.add_argument(
        arg.short, arg.long, help=arg.help_text, action=arg.action
    )

  parsed_args = arg_parser.parse_args()
  scraper_type = parsed_args.scraper
  if scraper_type:
    articles = Extractor(settings.URLS.get(scraper_type)).extract_all_entries()
    post_results(articles)

POST_URL = 'http://czl-api.code4.ro/api/publications/'
HEADERS = dict(
  Authorization='Token externe-very-secret-key'#todo get tokens
)
#todo set mandatory fields
def post_results(articles):
  serializer = Serializer()
  for a in articles:
    data = serializer.serialize(a)
    requests.post(POST_URL, data, headers=HEADERS)


if __name__ == '__main__':
  main()
