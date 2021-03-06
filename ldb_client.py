# encoding: utf-8

import logging
from urllib.parse import urljoin
import requests

class LivelihoodDbClient(object):

    _FIELDS = 'affected_areas,city,description,detail_addr,district,end_date,'\
              'end_time,road,start_date,start_time,type'

    def __init__(self, url):
        self.url = urljoin(url, '/events')

    def get_events(self, parameters):
        parameters['fields'] = self._FIELDS
        param_pairs = ('{}={}'.format(key, value) for key, value in parameters.items())
        query = '?{}'.format('&'.join(param_pairs))
        return self._get_json(urljoin(self.url, query))

    def get_single_event(self, event_id):
        url = '{}/{}?fields={}'.format(self.url, event_id, self._FIELDS)
        return self._get_json(url)

    def _get_json(self, url):
        logging.info('GET ' + url)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
