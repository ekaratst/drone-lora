import serial
import codecs

max_packets = 10
is_rssi = 11  #tansfer completed 1 packet

def main():
    lora_data = serial.Serial("/dev/ttyACM1", 9600, timeout=1)
    #write_to_file_path = ["output_5m", "output_10m"]
    write_to_file_path = ["output_5m"]
    for i in write_to_file_path:
        output_file = codecs.open(i, 'w', encoding='utf-8')
        count = 1
        while count <= max_packets:
            line = lora_data.readline()
            line = line.decode("utf-8")
            length_data = len(line)
            print(line)
            #print(length_data)
            print(count)
            output_file.write(line)
            if(length_data == is_rssi):
                count = count + 1
        print("-------------------------------------------------")
   
if __name__ == "__main__":
    main()