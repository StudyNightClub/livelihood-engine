# encoding: utf-8

from datetime import datetime, timedelta
import logging
from http import HTTPStatus
from flask import Flask, request, json
from mapplotter import MapPlotter

from chatbot_client import ChatbotClient, NotificationCategory
import event_filter
from google_url_shortener import shorten
from ldb_client import LivelihoodDbClient
from service_location import ServiceLocation
from udb_client import UserDbClient


VERSION = 'v1.2.0'
app = Flask(__name__)


locations = ServiceLocation()
if not locations.is_all_set():
    logging.error(locations.__dict__)
    raise EnvironmentError('Environment variables are incomplete.')


livelihood = LivelihoodDbClient(locations.ldb_url)
chatbot = ChatbotClient(locations.chatbot_url)
users = UserDbClient(locations.udb_url, locations.udb_token)
plotter = MapPlotter(locations.ldb_url, locations.map_url)


logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def greet():
    return json.jsonify({'greetings': 'You\'re accessing livelihood engine version {}'.format(VERSION)})


@app.route('/get_map/<string:user_id>')
def get_map(user_id):
    user = users.get_user_config(user_id)
    location = get_user_location(user)

    events = get_events_of_tomorrow(['all'])
    ids = [e['id'] for e in events]
    event_map = plotter.drawMarkerById(ids, location)
    return shorten(event_map)


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

    water_map, power_map, road_map = get_maps(events, body)
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
        # Filter events only on system schedule
        lat = float(location['latitude'])
        lon = float(location['longitude'])
        events = event_filter.nearby_events(events, lat, lon)
    else:
        category = NotificationCategory.USER_SCHEDULED

    water_map, power_map, road_map = get_maps(events, location)
    chatbot.push_notification(user_id, category, events, water_map, power_map,
            road_map)

    return json.jsonify({})



@app.route('/notify_all/<string:user_id>', methods=['POST'])
def notify_all(user_id):
    events = get_events_of_tomorrow(['all'])
    water_map, power_map, road_map = get_maps(events, get_user_location(None))
    chatbot.push_notification(user_id, NotificationCategory.BROADCAST,
        events, water_map, power_map, road_map)
    return json.jsonify({})


def get_events_of_tomorrow(types):
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    return livelihood.get_events({ 'after': tomorrow, 'before': tomorrow, 'type': ','.join(types) })


def get_event_ids(events, event_type):
    return [e['id'] for e in events if e['type'] == event_type]


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


def get_maps(events, location):
    water_map = plotter.drawMarkerById(get_event_ids(events, 'water'), location)
    power_map = plotter.drawMarkerById(get_event_ids(events, 'power'), location)
    road_map = plotter.drawMarkerById(get_event_ids(events, 'road'), location)
    return shorten(water_map), shorten(power_map), shorten(road_map)
