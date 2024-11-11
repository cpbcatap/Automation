import serial
import csv,os
from time import sleep

print("ST50H Credential configuration V1.0")
print('''
Defined Lora tx: 900 000 ms
Defined modbus heartbeat: 60 000 ms
''')

csv_file="Credential.csv"
com_port = input("Enter the COM port: ")
#lora_tx = int(input('input desired lora tx interval: '))
#mb_hb = int(input('input desired modbus heartbeat interval: '))

def query_csv(esn):
    with open(csv_file, 'r') as file:

        csv_reader = csv.DictReader(file)
        print("CSV is open")

        for row in csv_reader:
            if esn in row['ESN']:
                dev_eui = row['Deveui']
                appkey = row['Appkey']
                appeui = row['Appeui']
                
                return dev_eui, appkey, appeui

ser = serial.Serial(
    port= f"COM{com_port}",       
    baudrate=115200,     
    timeout=0.5
)

try:
 
    if not ser.is_open:
        ser.open()

    print("Serial port opened:", ser.name)
    wrong_esn = False
    
    while True:
        data = ser.readline()
        try:
            data = data.decode()
        except:
            data = str(data).replace('\xfe','')
            
        if data or wrong_esn:
            print("Received:", data)
            if data:
                ser.write("set config on \n".encode())
   
                esn=input("input desired esn: ")
                dev_eui, appkey, appeui=query_csv(esn)
                if dev_eui:
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    print("ESN VALID")
         
                    ser.write("set lora-config on \n".encode())
                    
                    ser.write(("set deveui " + dev_eui + "\n").encode())                  
                    
                    ser.write(("set appeui " + appeui + "\n").encode())
                    
                    ser.write(("set appkey " + appkey +"\n").encode())

                    ser.write(("set lora-tx interval 900000 \n").encode())
                    ser.write(("set lora-tx interval 900000 \n").encode())
    
                    ser.write((f"set modbus-hb interval 600000" + "\n").encode())
                    
                    ser.write(("save lora-config" + "\n").encode())
                    print("save lora-config")

                    while 1:
                        data=ser.readline().decode('utf-8', errors='ignore').strip()
                        ser.write("set config off\n".encode())
                        
                        print(data)
                        if "Configuration Mode: OFF" in data:
                            print("ENTER if credential is correct!")
                            exit=input("")
                            ser.write("exit\n".encode())
                        

                            break
                    print("Credential successfully saved, remove device.")
                    sleep(100)
                    
                else:
                    print("ESN does not exist! Please input ESN that is in the 'Credential' sheet")
            
except serial.SerialException as e:
    print("Error:", e)

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    #Close the serial port
    if ser.is_open:
        ser.close()
        print("Serial port closed.")
