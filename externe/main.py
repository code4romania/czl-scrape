import argparse

from scraper.engine import *
from scraper.settings import *


def main():
  arg_parser = argparse.ArgumentParser()
  for arg in ARGS.values():
    arg_parser.add_argument(
        arg.short, arg.long, help=arg.help_text, action=arg.action
    )

  parsed_args = arg_parser.parse_args()
  scraper_type = parsed_args.scraper
  if scraper_type:
    Extractor(settings.URLS.get(scraper_type)).extract_all_entries()

if __name__ == '__main__':
  main()
