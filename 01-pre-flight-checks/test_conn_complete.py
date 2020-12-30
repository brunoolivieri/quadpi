#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This script aims to test a connection to an MAVlink vehicle.

    It relies on Dronekit above pymavlink to handle the mavlink connection. Only works with Python2.x (due to Dronekit)

"""

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import dronekit
import time
import socket
import sys
import argparse
import exceptions
import math
from tabulate import tabulate

parser = argparse.ArgumentParser(description="python test_conn_basic.py --connect IP:PORT")
parser.add_argument("--connect", dest='connection_string', default=" --connect 127.0.0.1:17171", help="try: python test_conn_complete.py --connect 127.0.0.1:14550")
args = parser.parse_args()
ABRADF_CONTROL_AREA = LocationGlobalRelative(-15.840643,-47.925915,0) 

def connect_to_vehicle():
    print('Trying to connect to Vehicle... ', end = '')
    try:
        vehicle = connect(args.connection_string, wait_ready=True)
        return vehicle
    except socket.error:
        print('Bad TCP connection.')
        sys.exit(1)
    except exceptions.OSError as e:
        print('Bad TTY connection.')
        sys.exit(1)
    except APIException:
        print('API error.')
        sys.exit(1)
    except Exception as e:
        print('Error on connection: ' + str(e))
        sys.exit(1)
    finally:
        print('Vehicle connected!\n') 

def release_vehicle(vehicle):
   if vehicle:
        try:
            print('Closing vehicle... ', end = '')
            vehicle.close()
        except Exception as e:
            print('Error when closing connection: ' + str(e) + '\n')
        finally:
            print('Connection closed!\n') 

def get_distance_meters(target_location, current_location):
	dLat = target_location.lat - current_location.lat
	dLon = target_location.lon - current_location.lon

	return math.sqrt((dLat*dLat)+(dLon*dLon))*1.113195e5

def print_vehicle_summary(vehicle):

    print('Vehicle coords: %s \n' % str(vehicle.location.global_relative_frame).split(':')[1].replace(',', ', ') ) 


    titles=['Sys Parameter', 'Value']
    values=[]
    values.append(['Flight Mode',str(vehicle.mode).split(':')[1]])

    values.append(['SYSID_THISMAV',str(int(vehicle.parameters['SYSID_THISMAV']))])
    values.append(['SYSID_MYGCS',str(int(vehicle.parameters['SYSID_MYGCS']))])

    dist_to_ctrl_place = str(int(get_distance_meters(ABRADF_CONTROL_AREA,vehicle.location.global_relative_frame)))
    values.append(['Dist to ctrl place', dist_to_ctrl_place + ' meters'])

    batt_voltage =  vehicle.battery
    values.append(['BATT_CAPACITY',str(vehicle.parameters['BATT_CAPACITY']) + ' mAh'])
    values.append(['Current', str(batt_voltage.current  ) + ' amps'])
    values.append(['Energy left', str(batt_voltage.level  ) + ' %'])
    values.append(['Battery', str(batt_voltage.voltage ) + ' volts'])

    print(tabulate(values, headers=titles) + '\n')    

if __name__ == '__main__':
    print('\n')
    vehicle = connect_to_vehicle()
    if vehicle:
        print_vehicle_summary(vehicle)
        release_vehicle(vehicle)

    print('Script reached its end.\n')
    sys.exit(0)  
