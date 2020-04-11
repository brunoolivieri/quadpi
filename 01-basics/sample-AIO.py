
#############  DEPENDENCIES  #############

from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException

import time
import socket
import exceptions
import math
import argparse


#############  FUNCTIONS  #############


def connectMyCopter():
	print('[method] connectMyCopter()')

	parser = argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args = parser.parse_args()

	connection_string = args.connect

	# if not connection_string:
	# 	import dronekit_sitl
	# 	sitl = dronekit_sitl.start_default()
	# 	connection_string = sitl.connection_string()

	vehicle = connect(connection_string, wait_ready=True)

	return vehicle

def arm_and_takeoff(targetHeight):
	print('[method] arm_and_takeoff()')

	while vehicle.is_armable!=True:
		print('Waiting vehicle be armable...')
		time.sleep(1)
	print('Vehicle is armable.')


	vehicle.mode = VehicleMode("GUIDED")
	while vehicle.mode!='GUIDED':
		print('Waiting vehicle be in GUIDED mode...')
		time.sleep(1)
	print('Vehicle is in GUIDED mode.')


	vehicle.armed = True
	while vehicle.armed==False:
		print('Waiting arm...')
		time.sleep(1)
	print('Vehicle is armed!!!')


	vehicle.simple_takeoff(targetHeight) #meters

	while True:
		print("Current altitude: %d" %vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt >=.95*targetHeight:
			break
		time.sleep(1)


	print('Simple takeoff finished')

	return None


def get_distance_meters(targetLocation, currentLocation):

	dLat = targetLocation.lat - currentLocation.lat
	dLon = targetLocation.lon - currentLocation.lon

	return math.sqrt((dLat*dLat)+(dLon*dLon))*1.113195e5

def goto(targetLocation):
	print('[method] goto()')

	distanceToTargetLocation = get_distance_meters(targetLocation,vehicle.location.global_relative_frame)

	vehicle.simple_goto(targetLocation)

	while vehicle.mode.name=="GUIDED":
		currentDistance = get_distance_meters(targetLocation,vehicle.location.global_relative_frame)
		if currentDistance<distanceToTargetLocation*.01:
			print("Reached target waypoint")
			time.sleep(2)
			break
		time.sleep(1)
	return None

def land():
	print('[method] Land()')
	vehicle.mode = VehicleMode("LAND")
	while vehicle.mode.name !='LAND':
		print("Waiting to vehicle to enter LAND mode")
		time.sleep(1)
	print("Vechicle in LAND mode")

	return None

#############  MAIN PROGRAM  #############

wp1 = LocationGlobalRelative(-15.83947745528681,-47.92709159655583,10) 
wp2 = LocationGlobalRelative(-15.839604179895666,-47.926847217421304,10)
wp3 = LocationGlobalRelative(-15.839684457811742,-47.92714524073613,10)


vehicle = connectMyCopter()
arm_and_takeoff(10)

goto(wp1)
goto(wp2)
goto(wp3)

land()

while True:
	time.sleep(1)

vehicle.close()

print('Script finished')
