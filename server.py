# encoding: utf-8

from datetime import datetime, timedelta, timezone
import logging
from http import HTTPStatus
from urllib.parse import urljoin
from flask import Flask, request, json

from chatbot_client import ChatbotClient, NotificationCategory
import event_filter
from ldb_client import LivelihoodDbClient
from service_location import ServiceLocation
from udb_client import UserDbClient


VERSION = 'v1.3.0'
app = Flask(__name__)


service_urls = ServiceLocation()
if not service_urls.is_all_set():
    logging.error(service_urls.__dict__)
    raise EnvironmentError('Environment variables are incomplete.')


livelihood = LivelihoodDbClient(service_urls.ldb_url)
chatbot = ChatbotClient(service_urls.chatbot_url)
users = UserDbClient(service_urls.udb_url, service_urls.udb_token)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def greet():
    return json.jsonify({'greetings': 'You\'re accessing livelihood engine version {}'.format(VERSION)})


@app.route('/get_map/<string:user_id>')
def get_map(user_id):
    user = users.get_user_config(user_id)
    location = get_user_location(user)
    return get_map_url(location, 'all')


@app.route('/notify_here/<string:user_id>', methods=['POST'])
def notify_here(user_id):
    try:
        body = request.get_json(force=True, silent=True)
        lon = body['longitude']
        lat = body['latitude']
    except (KeyError, TypeError):
        logging.warn('Incomplete post data when /notify_here. {}'.format(request.form))
        return json.jsonify({'error': 'Please specify longitude and latitude.'}), HTTPStatus.BAD_REQUEST

    events = get_events_of_tomorrow(['all'])
    events = event_filter.nearby_events(events, lat, lon)
    logging.info('notify_here events {}'.format(events))

    water_map, power_map, road_map = get_all_types_of_maps(body)
    chatbot.push_notification(user_id, NotificationCategory.USER_REQUESTED,
        events, water_map, power_map, road_map)
    return json.jsonify({})


@app.route('/notify_interest/<string:user_id>', methods=['POST'])
def notify_interest(user_id):
    user = users.get_user_config(user_id)
    location = get_user_location(user)
    types = get_user_subscribed_types(user)
    events = get_events_of_tomorrow(types)

    user_scheduled = request.args.get('user_scheduled', 0, int)
    if user_scheduled == 0:
        category = NotificationCategory.SYSTEM_SCHEDULED
    else:
        category = NotificationCategory.USER_SCHEDULED

    water_map, power_map, road_map = get_all_types_of_maps(location)
    chatbot.push_notification(user_id, category, events, water_map, power_map,
            road_map)

    return json.jsonify({})



@app.route('/notify_all/<string:user_id>', methods=['POST'])
def notify_all(user_id):
    water_events = get_events_of_tomorrow(['water'])
    power_events = get_events_of_tomorrow(['power'])
    road_events = get_events_of_tomorrow(['road'])
    water_map, power_map, road_map = get_all_types_of_maps(get_user_location(None))
    chatbot.push_notification(user_id, NotificationCategory.BROADCAST,
        water_events + power_events + road_events, water_map, power_map, road_map)
    return json.jsonify({})


def get_events_of_tomorrow(types):
    tomorrow = get_tomorrow_date_str()
    return livelihood.get_events({ 'after': tomorrow, 'before': tomorrow, 'type': ','.join(types) })


def get_user_location(user):
    if user and user.get('longitude'):
        return user
    else:
        return { 'latitude': 25.047760, 'longitude': 121.517029 }


def get_user_subscribed_types(user):
    types = []
    if user['subscribe_electricity']:
        types.append('power')
    if user['subscribe_water']:
        types.append('water')
    if user['subscribe_road']:
        types.append('road')
    return types


def get_map_url(location, event_type):
    tomorrow = get_tomorrow_date_str()
    query = {
        'current_location': '{},{}'.format(location['latitude'], location['longitude']),
        'before': tomorrow,
        'after': tomorrow,
        'type': event_type,
    }
    query_str = '&'.join([key + '=' + value for key, value in query.items()])
    return urljoin(service_urls.map_url, 'map.html?' + query_str)


def get_all_types_of_maps(location):
    return get_map_url(location, 'water'), get_map_url(location, 'power'), get_map_url(location, 'road')


def get_tomorrow_date_str():
    tz = timezone(timedelta(hours=8))
    return (datetime.now(tz) + timedelta(days=1)).strftime('%Y-%m-%d')
