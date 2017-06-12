# livelihood-engine v1.0.1
The notification generating engine.

## Requirements

* Flask 0.12
* requests 2.17

## Run

For development, you can host the engine server on your own machine.

    $ export FLASK_APP=server.py
    $ export CHATBOT_URL=<chatbot_base_url>
    $ export UDB_URL=<user_database_base_url>
    $ export UDB_TOKEN=<userdb_token>
    $ export MAP_URL=<map_url>
    $ export LDB_URL=<livelihood_database_base_url>
    $ flask run
      * Running on http://127.0.0.1:5000

If any of the environment variable isn't set, runtime error will happen.

Now the server should be hosted on http://127.0.0.1:5000
(might be slightly different depending on your environment).

Use the URL shown in the "Running on" line as the base URL for engine.

## Usage

The engine server takes the following requests:

### Greet

    $ curl -X GET <engine_url>/

A greeting message and version of the current engine will be returned.

### Get map URL on user's location of interest

    $ curl -X GET <engine_url>/get_map/<user_id>

A map URL centered on the user's location of interest will be returned.

### Trigger notification on a specific location

    $ curl -X POST -d <body> <engine_url>/notify_here/<user_id>

The body is a JSON object with the following fields:

Field       | Value
----------- | -----
`longitude` | The longitude of user's current location in WGS84.
`latitude`  | The latitude of user's current location in WGS84.

When requested, the engine will find events near the given location, and send
notifications to chatbot. The notification category will be `userRequested`.
Only the events of subscribed types will be used.

For example:

    $ curl -X POST -d '{"longitude":121.5556, "latitude":25.0026}' http://localhost:5000/notify_here/foo

### Trigger notification on user's location of interest

    $ curl -X POST <engine_url>/notify_interest/<user_id>

This method takes one optional parameter `user_scheduled`, the value could be
0 or 1. The value of this parameter affects the generated notification
category, `userScheduled` for 1, and `systemScheduled` for 0.
The default value is 0.

When requested, the engine will get the user's location of interest and other
setting to generated related notifications. The notifications will be sent to
chatbot.
Only the events of subscribed types will be used.

### Trigger notification of all events

    $ curl -X POST <engine_url>/notify_all/<user_id>

When requested, the engine will get all events to happen, and send
notifications to chatbot. The notification category will be `broadcast`.
