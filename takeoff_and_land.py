from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument('--connect', default='127.0.0.1:14550')
#args = parser.parse_args()

# Connect to the vehicle
connection_string = "/dev/ttyACM0"
baud_rate = 57600
print('Connecting to Vehicle on: %s' %connection_string)
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    #check that vehicle has reached takeoff altitude
    while True:
	current_altitude =  vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %(current_altitude, aTargetAltitude))
        # Break and return from function just below target altitude
        if current_altitude >= aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Initialize the take off sequence to 1m
arm_and_takeoff(1)
print("take off complete")

# Hover for 5 seconds
time.sleep(5)

# landed
print("Now let's land")
vehicle.mode = VehicleMode("LAND")

#close vehicle object
vehicle.close()

