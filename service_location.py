# encoding: utf-8

import os

class ServiceLocation(object):

    def __init__(self):
        self.chatbot_url = os.environ.get('CHATBOT_URL')
        self.udb_url = os.environ.get('UDB_URL')
        self.udb_token = os.environ.get('UDB_TOKEN')
        self.map_url = os.environ.get('MAP_URL')
        self.ldb_url = os.environ.get('LDB_URL')

    def is_all_set(self):
        return self.chatbot_url and self.udb_url and self.udb_token and\
            map_url and ldb_url
