#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This script controls a Copter in a specific site and goes around.

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
ARMABLE_TIMEOUT = 10
ARM_TIMEOUT = 10
FLIGHTMODE_CHG_TIMEOUT = 5
TAKEOFF_TIMEOUT = 60




def connect_to_vehicle():
    print('Trying to connect to Vehicle... ', end = '')
    try:
        vehicle = connect(args.connection_string, wait_ready=True)
        print('Vehicle connected!\n') 
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

def arm_and_takeoff(vehicle, target_height):
	
    print('Checking if the vehicle is armable... ', end = '')
    arm_timeout = 0
    while vehicle.is_armable!=True:
        if arm_timeout >= ARMABLE_TIMEOUT:
            print('\nChecking for an armable failed! Aborting script execution.')
            sys.exit(1)
        else:
            print(str(arm_timeout) + '..', end = '')
            arm_timeout += 1
        time.sleep(1)
    print('\nVehicle is armable!\n')


    print('Changing flight mode to GUIDED... ', end = '')
    chg_mode_timeout = 0
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode!='GUIDED':
        if chg_mode_timeout >= FLIGHTMODE_CHG_TIMEOUT:
            print('\nTimeout to change flight mode! Aborting script execution.')
            sys.exit(1)
        else:
            print(str(chg_mode_timeout) + '..', end = '')           
            chg_mode_timeout += 1
        time.sleep(1)
    print('\nVehicle is in GUIDED mode!\n')


    print('Arming vehicle... ', end = '')
    arm_timeout = 0
    vehicle.armed = True
    while vehicle.armed==False:
        if arm_timeout >= ARM_TIMEOUT:
            print('\nTimeout to arm vehicle! Aborting script execution.')
            sys.exit(1)
        else:
            print(str(arm_timeout) + '..', end = '')
            arm_timeout += 1
        time.sleep(1)
    print('\nVehicle is armed!')


    print('\nTaking off...')    
    vehicle.simple_takeoff(target_height) #meters
    simple_takeoff = 0
    while True:
        print("Current altitude: %s" % vehicle.location.global_relative_frame.alt)
        if (vehicle.location.global_relative_frame.alt >=.95*target_height)or(simple_takeoff>=TAKEOFF_TIMEOUT):
            print('\nDesidered height of %s reached.\n' % target_height)
            break
        else:
            simple_takeoff += 1
            time.sleep(1)
    print('Simple takeoff finished!')

    return None

def land(vehicle):

    print('\nVehicle commanded to land... ', end = '')
    vehicle.mode = VehicleMode("LAND")
    time.sleep(1)
    while vehicle.mode.name !='LAND':
        print("Waiting to vehicle to enter LAND mode...")
        time.sleep(1)
    print("Vechicle in LAND mode!")

    while True:
        print("Current altitude: %s" % vehicle.location.global_relative_frame.alt)
        if (vehicle.location.global_relative_frame.alt <=1):
            print('Reached 1 meter above ground. Exiting from land() method.')
            break
        time.sleep(1)

    return None

if __name__ == '__main__':
    print('\n')
    vehicle = connect_to_vehicle()
    if vehicle:
        print_vehicle_summary(vehicle)
        arm_and_takeoff(vehicle, 10) 
        land(vehicle)
        release_vehicle(vehicle)

    print('Script reached its end.\n')
    sys.exit(0)  
