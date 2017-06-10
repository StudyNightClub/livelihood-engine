import logging
from flask import Flask, request, json
from service_location import ServiceLocation

VERSION = 'v0.0.0'
app = Flask(__name__)

locations = ServiceLocation()
if not locations.is_all_set():
    logging.error(locations.__dict__)
    #raise EnvironmentError('Environment variables are incomplete.')

@app.route('/')
def greet():
    return json.jsonify({'greetings': 'You\'re accessing livelihood engine version {}'.format(VERSION)})

@app.route('/get_map/<string:user_id>')
def get_map(user_id):
    return user_id

@app.route('/notify_here/<string:user_id>', methods=['POST'])
def notify_here(user_id):
    return json.jsonify(request.form)

@app.route('/notify_interest/<string:user_id>', methods=['POST'])
def notify_interest(user_id):
    return user_id

@app.route('/notify_all/<string:user_id>', methods=['POST'])
def notify_all(user_id):
    return user_id
