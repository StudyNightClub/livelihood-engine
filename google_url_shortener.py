# encoding: utf-8

import logging
import os
import sys
import requests

_KEY = os.environ['URL_SHORTENER_KEY']

def shorten(url):
    data = { 'longUrl': url }
    response = requests.post(
        'https://www.googleapis.com/urlshortener/v1/url?key='+_KEY,
        json=data)
    result = response.json()
    if result and result.get('id'):
        return result.get('id')
    else:
        logging.error('Unable to shorten URL {}, response {}.'.format(url, result))
        return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(shorten(sys.argv[1]))
    else:
        print('google_url_shortener')
