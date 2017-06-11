# encoding: utf-8

from datetime import datetime
from enum import Enum
import logging
from urllib.parse import urljoin
import requests

class ChatbotClient(object):

    def __init__(self, url):
        self.url = urljoin(url, '/push')

    def push_notification(self, userid, category, events, water_map, power_map, road_map):
        notifications = []
        for e in events:
            noti = {
                'type': self._convert_event_type(e['type']),
                'startDate': self._convert_date(e['start_date']),
                'endDate': self._convert_date(e['end_date']),
                'startTime': self._convert_time(e['start_time']),
                'endTime': self._convert_time(e['end_time']),
                'description': e['description'],
                'addrRoad': e['city'] + e['district'] + e['road'],
                'addrDetail': e['detail_addr']
            }
            notifications.append(noti)

        data = {
            'category': category.value,
            'userId': userid,
            'notifications': notifications,
            'mapURL': {
                'water_outage': water_map,
                'power_outage': power_map,
                'road_work': road_map
            }
        }
        logging.info('POST chatbot/push {}'.format(data))
        requests.post(self.url, json=data)

    def _convert_event_type(self, t):
        t = t.lower()
        if t == 'water':
            return 'water_outage'
        elif t == 'power':
            return 'power_outage'
        elif t == 'road':
            return 'road_work'
        else:
            logging.error('Unrecogized event type {}'.format(t))
            return t

    def _convert_date(self, date):
        return datetime.strptime(date, '%Y-%m-%d').strftime('%Y/%m/%d')

    def _convert_time(self, time):
        if time:
            return datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
        else:
            return None

class NotificationCategory(Enum):
    USER_REQUESTED = 'userRequested'
    USER_SCHEDULED = 'userScheduled'
    SYSTEM_SCHEDULED = 'systemScheduled'
    BROADCAST = 'broadcast'
