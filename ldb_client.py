# encoding: utf-8

from urllib.parse import urljoin
import requests

class LivelihoodDbClient(object):

    def __init__(self, url):
        self.url = urljoin(url, '/events')

    def get_events(self, parameters):
        parameters['fields'] = 'affected_areas,city,description,detail_addr,'\
                               'district,end_date,end_time,road,start_date,'\
                               'start_time,type'
        param_pairs = ('{}={}'.format(key, value) for key, value in parameters.items())
        query = '?{}'.format('&'.join(param_pairs))
        return self._get_json(self.url)

    def _get_json(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
