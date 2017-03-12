import logging
import requests
import time

from utils.settings import *


def post_data(data):
    attempts = 5
    success = False

    while not success and attempts > 0:
        attempts -= 1
        response = requests.post(URLS['api-publications'], data, headers=HEADERS)

        # If it already exists, skip retrying
        if _already_exists(response):
            logging.warning(
                'Object: %s \nalready exists, according to API. Skipping.', data
            )
            break

        success = response.status_code == STATUS_CREATED
        # wait 30 seconds before retrying
        time.sleep(30)

    if not success:
        logging.error('Failed to POST data to API: %s', data)

    return success


def _already_exists(response):
    return response.status_code == STATUS_BAD_REQUEST \
           and ALREADY_EXISTS in response.text.lower()
