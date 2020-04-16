#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This script aims to test a connection to an MAVlink vehicle.

    It relies on Dronekit above pymavlink to handle the mavlink connection. Only works with Python2.x (due to Dronekit)

"""

from __future__ import print_function
#from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import dronekit
import time
import socket
import sys
import argparse
import exceptions

parser = argparse.ArgumentParser(description="python test_conn_basic.py --connect IP:PORT")
parser.add_argument("--connect", dest='connection_string', default=" --connect 127.0.0.1:14550", help="try: python test_conn_basic.py --connect 127.0.0.1:14550")
args = parser.parse_args()


def connect_my_vehicle():
    print('Trying to connect to Vehicle...')
    try:
        vehicle = dronekit.connect(args.connection_string, wait_ready=True)
        return vehicle
    except socket.error:
        print('Bad TCP connection.')
    except exceptions.OSError as e:
        print('Bad TTY connection.')
    except dronekit.APIException:
        print('API error.')
    except Exception as e:
        print('Error on connection: ' + str(e))
        sys.exit(1)  


if __name__ == '__main__':
    
    vehicle = connect_my_vehicle()
    if vehicle:
        print('Vehicle connected!')
        try:
            print('Closing vehicle...')
            vehicle.close()
        except Exception as e:
            print('Error when closing connection: ' + str(e))
        finally:
            print('Connection closed!')    
        
    print('Script finished.')

    sys.exit(1)  
