from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

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
        
def change_altitude(aTargetAltitude):
    print("Change altitude")
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
        
def tansfer_data_at_target_altitude(loraConnection, outputFile, aTargetAltitude):
    lora_data = loraConnection
    write_to_file_path = outputFile
    output_file = open(write_to_file_path, "w+")
    count = 1
    arm_and_takeoff(aTargetAltitude) 
    print("take off complete")
    now = time.time()
    future = now + 120
    print("Stopwatch has been set for 2 mins.")
    while count < 31:
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
        if(length_data == 11):
            count = count + 1
    if count >= 31:
        is_completed_data = True
    return is_completed_data
    
def main():
    lora_data = serial.Serial("/dev/ttyACM1", 9600, timeout=1)
    is_completed_data = tansfer_data_at_target_altitude(lora_data, output_5m, 5)
    if is_completed_data:
        is_completed_data = tansfer_data_at_target_altitude(lora_data, output_10m, 10)    
    print("Now let's land")
        vehicle.mode = VehicleMode("LAND")  
        vehicle.close()  
   
if __name__ == "__main__":
    main()