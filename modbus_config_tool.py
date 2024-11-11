import serial
import csv
import os
from time import sleep

print("Modbus Configuration 11.7.2024 V2")
com_port = input("Enter the COM port number: ")

ser = serial.Serial(
    port=f"COM{com_port}",   
    baudrate=115200,    
    timeout=0.09       
)

def device_params_1(ser):
    """
    Sets the initial device parameters.
    """
    while True:
        data = ser.readline().decode('utf-8', errors='ignore').strip()
        if data:
            print(f"Received data: {data}")

            ser.write("set config on \n".encode())

            if "Configuration Mode: ON" in data:
                print("Debug: Entering configuration mode")
                ser.write("set device-params 01 02 05 00 00 00\n".encode())
                sleep(0.05)

                while True:
                    response = ser.readline().decode('utf-8', errors='ignore').strip()
                    if "READ OK" in response:
                        while True:
                            res = ser.readline().decode('utf-8', errors='ignore').strip()
                            if "ERASE OKWRITE OK" in res:
                                print("device-params 1 set successfully!")
                                return True

def device_params_2(ser):
    
    while True:
        ser.write("set device-params 01 01 05 00 00 01\n".encode())
        sleep(0.05)

        while True:
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            if "READ OK" in response:
                while True:
                    res = ser.readline().decode('utf-8', errors='ignore').strip()
                    if "ERASE OKWRITE OK" in res:
                        print("device-params 2 set successfully!")
                        return True

def segment_params(ser, segment_params):
    
    while True:
        data = ser.readline().decode('utf-8', errors='ignore').strip()
        ser.write(f"set segment-params {segment_params}\n".encode())
        sleep(0.05)
        
        if "READ OK" in data:
            while True:
                res = ser.readline().decode('utf-8', errors='ignore').strip()
                if "ERASE OKWRITE OK" in res:
                    print("Segment parameters set successfully!")
                    return True

def interval(lora_int, mb_int):
    while True:
        data = ser.readline().decode('utf-8', errors='ignore').strip()
        ser.write("set lora-config on \n".encode())
        if "Lora-Configuration Mode: ON" in data:
            response = ser.readline().decode('utf-8', errors='ignore').strip()

            ser.write(f"set lora-tx interval {lora_int} \n".encode())
            ser.write(f"set modbus-hb interval {mb_int} \n".encode()) 

            print(f"lora tx interval set to {lora_int}")
            print(f"lora modbus hb interval set to {mb_int}")
            
            ser.write("save lora-config \n".encode())            
            return True
            
            
# Define segment parameters
segments = [
    "02 01 01 01 01 00 00 3F FF 08 01 03 01 00 00 0E C5 F2",
    "02 01 02 01 01 00 00 FF 3F 08 01 03 01 0E 00 10 24 39",
    "02 01 03 01 01 00 00 00 FF 08 01 03 01 36 00 08 A5 FE",
    "02 01 04 01 01 00 00 FF 3F 08 01 03 01 64 00 10 04 25",
    "02 01 05 01 01 00 00 00 FF 08 01 03 01 8C 00 08 84 1B",
    "02 01 06 01 01 00 00 FF 3F 08 01 03 01 BA 00 10 64 1F",
    "02 01 07 01 01 00 00 00 FF 08 01 03 01 E2 00 08 E5 C6",
    "02 01 08 01 01 00 00 FF 3F 08 01 03 02 10 00 10 44 7B",
    "02 01 09 01 01 00 00 00 FF 08 01 03 02 38 00 08 C4 79"
]

# Run the device parameter functions
device_params_1(ser)
device_params_2(ser)

# Iterate through segment parameters
for i, segment in enumerate(segments, 1):
    print(f"Setting segment_params_{i}...")
    segment_params(ser, segment)
    sleep(0.05)

lora_tx = int(input("Input desired lora tx interval: "))
#lora_tx = 900000
mb_hb = int(input("Input desired modbus-hb interval: "))
#mb_hb = 60000
interval(lora_tx, mb_hb)


while True:
    data = ser.readline().decode('utf-8', errors='ignore').strip()
    ser.write("set config off\n".encode())
    print(data)
    sleep(.1)

    if "Configuration Mode: OFF" in data:
        input("ENTER to exit")
        print("Remove Board!!!")

        break
    
    
