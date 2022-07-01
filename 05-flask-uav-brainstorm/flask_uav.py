#!/usr/bin/env python

import sys
import argparse
import atexit

# Import from inside project
from args_manager import get_args
from blueprints.send_cmds_to_uav import send_cmds_to_uav
from blueprints.request_data_from_uav import request_data_from_uav
from copter_connection import get_copter_instance
from flask_uav_functions import send_location_start, interrupt

from flask import Flask
from flask_cors import CORS


parser = argparse.ArgumentParser(
    description='Copy Common Files as needed, stripping out non-relevant wiki content',  
)
parser.add_argument(
    '--uav_sysid',
    dest='uav_sysid',
    default=-1,
    help="Value for uav SYSID to connect through mavlink",  
)
parser.add_argument(
    '--uav_udp_port',
    dest='uav_udp_port',
    default=-1,
    help="Value for uav UAV on localhost",  
)
parser.add_argument(
    '--uav_ip',
    dest='uav_ip',
    help="IP to run the flask server",  
)

args = parser.parse_args()

if (args.uav_sysid == -1) or (args.uav_udp_port == -1):
    print("Bad parameters. Check uav_sysid and uav_udp_port")
    sys.exit(1)

# Register args from this file to the application
get_args(args)

#__license__ = "GPLv3}"

def create_app():
    global app

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(send_cmds_to_uav)
    app.register_blueprint(request_data_from_uav)

    return app

#----------------------------------------------------------------------

flask_port = str(5000 + int(str(args.uav_udp_port)[-2:]))
print("Running MAIN!!!")
copter = get_copter_instance(args)

# to enable a task for pooling GS with its position
app = create_app()  

# Initiate a Copter instance and send location thread
send_location_start(flask_port)
# When you kill Flask (SIGTERM), clear the trigger for the next thread
atexit.register(interrupt)

app.run(host="0.0.0.0", port=flask_port)