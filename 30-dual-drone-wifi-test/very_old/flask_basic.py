
import json
from flask import Flask
#from flask import jsonify returns a json from a dict
app = Flask(__name__)

simple_counter = 0


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/position')
def info_position():
    my_position_json = json.loads('{"id": 20, "lat": "x", "lng": "y", "high": 27, "bool": true}')
    return my_position_json

@app.route('/dynamic_position')
def dynamic_position():
    global simple_counter
    simple_counter = simple_counter + 1
    my_position_json = json.loads('{"id": 20, "lat": "x", "lng": "y", "high": 27, "bool": true, "counter":' + str(simple_counter) + '}')
    return my_position_json

