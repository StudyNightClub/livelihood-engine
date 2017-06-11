# encoding: utf-8

from datetime import datetime, timedelta
import logging
from http import HTTPStatus
from flask import Flask, request, json

from chatbot_client import ChatbotClient, NotificationCategory
import event_filter
import important_images
from ldb_client import LivelihoodDbClient
from service_location import ServiceLocation
from udb_client import UserDbClient

VERSION = 'v0.0.0'
app = Flask(__name__)

locations = ServiceLocation()
if not locations.is_all_set():
    logging.error(locations.__dict__)
    raise EnvironmentError('Environment variables are incomplete.')

livelihood = LivelihoodDbClient(locations.ldb_url)
chatbot = ChatbotClient(locations.chatbot_url)
users = UserDbClient(locations.udb_url, locations.udb_token)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def greet():
    return json.jsonify({'greetings': 'You\'re accessing livelihood engine version {}'.format(VERSION)})

@app.route('/get_map/<string:user_id>')
def get_map(user_id):
    return important_images.get_image()

@app.route('/notify_here/<string:user_id>', methods=['POST'])
def notify_here(user_id):
    try:
        body = request.get_json(force=True, silent=True)
        lon = body['longitude']
        lat = body['latitude']
    except (KeyError, TypeError):
        logging.warn('Incomplete post data when /notify_here. {}'.format(request.form))
        return json.jsonify({'error': 'Please specify longitude and latitude.'}), HTTPStatus.BAD_REQUEST

    events = get_events_of_tomorrow()
    events = event_filter.nearby_events(events, lat, lon)
    chatbot.push_notification(user_id, NotificationCategory.USER_REQUESTED,
        events, important_images.get_image(), important_images.get_image(),
        important_images.get_image())
    return json.jsonify({})

@app.route('/notify_interest/<string:user_id>', methods=['POST'])
def notify_interest(user_id):
    return user_id

@app.route('/notify_all/<string:user_id>', methods=['POST'])
def notify_all(user_id):
    events = get_events_of_tomorrow()
    chatbot.push_notification(user_id, NotificationCategory.BROADCAST,
        events, important_images.get_image(), important_images.get_image(),
        important_images.get_image())
    return json.jsonify({})

def get_events_of_tomorrow():
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    return livelihood.get_events({ 'after': tomorrow, 'before': tomorrow })
