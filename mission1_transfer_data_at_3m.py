from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import serial

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


def main():
    now = time.time()
    future = now + 120
    while time.time() < future:
        lora_data = serial.Serial("/dev/ttyACM1", 9600, timeout=1)  
        write_to_file_path = "output_5m"
        #is_checked_5m = False
        # for i in write_to_file_path:
        output_file = open(write_to_file_path, "w+")
        count = 1
        arm_and_takeoff(3) 
        print("take off complete")
        while count < 31:
            line = lora_data.readline()
            line = line.decode("utf-8")
            length_data = len(line)
            print(line)
            print(count)
            output_file.write(line)
            if(length_data == 11):
                count = count + 1
        # is_checked_5m = True
        print("Now let's land")
        vehicle.mode = VehicleMode("LAND")  
        vehicle.close()   
    if count < 31:
        print("Now let's land")
        vehicle.mode = VehicleMode("LAND")  
        vehicle.close()   
   
if __name__ == "__main__":
    main()