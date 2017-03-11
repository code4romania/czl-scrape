import argparse

from scraper.settings import ARGS


def main():
    arg_parser = argparse.ArgumentParser()
    for arg in ARGS.values():
        arg_parser.add_argument(
            arg.short, arg.long, help=arg.help_text, action=arg.action
        )
    parsed_args = arg_parser.parse_args()
    if parsed_args.scraper:
        pass

main()
