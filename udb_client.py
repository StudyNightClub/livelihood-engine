# encoding: utf-8

import logging
from urllib.parse import urljoin
import requests

class UserDbClient(object):

    _USER_QUERY_PATH_FORMAT = '/user/{}?userToken={}'

    def __init__(self, url, token):
        self.baseurl = url
        self.token = token

    def get_user_id_list(self):
        url = urljoin(self.baseurl, self._USER_QUERY_PATH_FORMAT.format(0, self.token))
        return self._get_json(url)

    def get_user_config(self, uid):
        url = urljoin(self.baseurl, self._USER_QUERY_PATH_FORMAT.format(uid, self.token))
        return self._get_json(url)

    def _get_json(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()
            except:
                logging.warn('Mal-formed user config {}'.format(url))
                return None
        else:
            return None
