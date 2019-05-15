import serial

def main():
    lora_data = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    data_read = []
    count = 1
    while count < 6:
        #data_read = lora_data.read(2000)
        #data_read = lora_data.readline()
        #print(len(lora_data.readline()))
        print("{0} len: {1}".format(lora_data.readline(),len(lora_data.readline())))
        if len(lora_data.readline()) == 0:
            continue
        data_read.append(lora_data.readline())
        #if data_read[0] == "R":
         #   print("okkkk")
        #print(data_read)
        #print(count)
        count = count + 1
    print(data_read)
            
if __name__ == "__main__":
    main()