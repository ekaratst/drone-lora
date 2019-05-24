from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import serial
import codecs

# Connect to the vehicle
connection_string = "/dev/ttyACM0"
baud_rate = 57600
print('Connecting to Vehicle on: %s' %connection_string)
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

max_packets = 10
is_rssi = 11  #tansfer completed 1 packet

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
    lora_data = serial.Serial("/dev/ttyACM1", 9600, timeout=1) 
    write_to_file_path = "output_5m"
    output_file = codecs.open(write_to_file_path, 'w', encoding='utf-8')
    count = 1
    altitude = input('Enter altitude in metre as an integer: ')
    if altitude > 15:
        print("Please enter time <= 15 metre.")
        exit()
    stopwatch = input('Enter time in seconds as an integer: ')
    if stopwatch > 900:
        print("Please enter time <= 900secs.")
        exit()
    arm_and_takeoff(altitude) 
    print("take off complete")
    now = time.time()
    future = now + stopwatch
    while count <= max_packets:
        if time.time() >= future:
            print("..timeout..!!")
            is_completed_data = False
            break
        line = lora_data.readline()
        line = line.decode("utf-8")
        length_data = len(line)
        print(line)
        print(count)
        output_file.write(line)
        if(length_data == is_rssi):
            count = count + 1
    print("Now let's land")
    vehicle.mode = VehicleMode("LAND")  
    vehicle.close()   
   
if __name__ == "__main__":
    main()