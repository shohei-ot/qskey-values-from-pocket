# coding: UTF-8

import sys
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from loguru import logger
import json
import fire
import urllib

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CONSUMER_KEY = environ.get("POCKET_CONSUMER_KEY")
ACCESS_TOKEN = environ.get("POCKET_ACCESS_TOKEN")
TAG = environ.get("POCKET_TAG")
KEY_NAME = environ.get("KEY_NAME")

def fetch_posts(tag=None):
    if CONSUMER_KEY is None or ACCESS_TOKEN is None or KEY_NAME is None:
        logger.error('Requrie POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, KEY_NAME')
        sys.exit(1)

    params = {
        'consumer_key': CONSUMER_KEY,
        'access_token': ACCESS_TOKEN,
        'tag': tag
    }
    resp = requests.request('GET', 'https://getpocket.com/v3/get', params=params)

    if resp.status_code != 200:
        logger.error(resp.text)
        sys.exit(1)

    respJson = json.loads(resp.content)

    if respJson['status'] != 1:
        logger.error('unexpected status: ' + str(respJson['status']) + ', ' + str(respJson['error']))
        sys.exit(1)

    keyNameValueList = ''

    keys = respJson['list'].keys()
    for key in keys:
        post = respJson['list'][key]
        url = post['given_url']
        queries = url.split('?')

        if len(queries) != 2:
            logger.error('unexpected count: ' + str(queries.count()))
            continue

        param = urllib.parse.parse_qs(queries[1])
        keyNameValue = param[KEY_NAME][0]
        keyNameValueList += keyNameValue + '\n'

    if len(keyNameValueList) == 0:
        logger.error('no ' + KEY_NAME)
        sys.exit(1)

    print(keyNameValueList)

    return

def run():
    if TAG is None:
        logger.error('Required tag')
        sys.exit(1)

    return fetch_posts(TAG)

if __name__ == '__main__':
    fire.Fire(run)