import serial

def main():
    lora_data = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    write_to_file_path = ["output_5m", "output_10m"]
    is_checked_5m = False
    for i in write_to_file_path:
        output_file = open(i, "w+")
        count = 1
        while count < 31:
            line = lora_data.readline()
            line = line.decode("utf-8")
            length_data = len(line)
            print(line)
            print(count)
            output_file.write(line)
            if(length_data == 11):
                count = count + 1
        is_checked_5m = True
        print("-------------------------------------------------")
   
if __name__ == "__main__":
    main()