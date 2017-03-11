#!/usr/bin/env python
import re

from setuptools import setup

install_requires = [
  'beautifulsoup4',
  'requests',
  'simplejson',
  'argparse',
  'lxml'
]

version_regex = re.compile("VERSION\s*=\s*'(.*?)'$")

with open('core/__init__.py') as stream:
  VERSION = version_regex.search(stream.read()).group(1)

setup(
  version=VERSION,
  name='mae-scraper',
  url='https://github.com/code4romania/czl-scrape/tree/master/externe',
  author='',
  author_email='',
  description='Scraper pentru site-ul Ministerului de afaceri externe',
  install_requires=install_requires,
)
