import os
import serial
import csv
from datetime import datetime

def get_com_port():
    return input("Enter the COM port: ")

def initialize_serial(com_port):
    try:
        return serial.Serial(
            port="COM" + com_port,
            baudrate=115200,
            timeout=10
        )
    except serial.SerialException as e:
        print("Error opening serial port:", e)
        return None

def read_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        return list(reader)

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def add_data_to_csv(file_path, row_data):
    data = read_csv(file_path)
    row_number = 0
    while row_number < len(data):
        if all(cell == '' for cell in data[row_number][2:]):
            break
        row_number += 1
    while len(data) <= row_number:
        data.append([''] * 20)
    data[row_number][:len(row_data)] = row_data
    write_csv(file_path, data)
    print(f"Data added successfully at row {row_number + 1}.")

def setup_csv_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ESN', 'Timestamp', 'Board ID', 'VIN Test Result', 'IIN Test Result', 'VBAT Test Result', 
                             'IBAT Test Result', 'CT1', 'CT2', 'CT3', 'OR1', 'OR2', 'OR3', 'DC1 Shorted Result', 
                             'DC1 Result', 'DC2 Shorted Result', 'DC2 Result', 'ModBus Detached Result', 'ModBus Attached Result'])

def main():
    com_port = get_com_port()
    ser = initialize_serial(com_port)
    if ser is None:
        return

    esn = input("Please enter the ESN: ")
    universal_file_path = "OAQ_v2.0.0"
    setup_csv_file(universal_file_path)

    os.makedirs("OAQ_v2.0.0 data points", exist_ok=True)
    board_id = None
    vin_result = iin_result = vbat_result = ibat_result = None
    ct1_result = ct2_result = ct3_result = or1_result = or2_result = or3_result = None
    dc1_short_result = dc1_result = dc2_short_result = dc2_result = None
    modbus_detached_result = modbus_attached_result = None

    try:
        if not ser.is_open:
            ser.open()
        print("Serial port opened:", ser.name)

        while True:
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{current_time}: {data}')
                
                if data.startswith("Board ID:"):
                    if board_id:
                        # Save the collected data for the previous board_id
                        csv_filename = os.path.join("ESN data points", f'{board_id}_{current_time.replace(":", "-")}.csv')
                        with open(csv_filename, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Timestamp', 'Serial Output'])
                            writer.writerow([current_time, data])
                            
                    board_id = data.split(":")[1].strip()
                    print(f'Detected Board ID: {board_id}')
                    
                    # Reset test results for the new board_id
                    vin_result = iin_result = vbat_result = ibat_result = None
                    ct1_result = ct2_result = ct3_result = or1_result = or2_result = or3_result = None
                    dc1_short_result = dc1_result = dc2_short_result = dc2_result = None
                    modbus_detached_result = modbus_attached_result = None

                if board_id:
                    # Continue writing serial output to the current device's file
                    csv_filename = os.path.join("OAQ_v2.0.0 data points", f'{board_id}_{current_time.replace(":", "-")}.csv')
                    with open(csv_filename, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([current_time, data])

                if "VIN Test Result" in data:
                    vin_result = data.split(":")[1].strip()
                if "IIN Test Result" in data:
                    iin_result = data.split(":")[1].strip()
                if "VBAT Test Result" in data:
                    vbat_result = data.split(":")[1].strip()
                if "IBAT Test Result" in data:
                    ibat_result = data.split(":")[1].strip()
                if "Charging Test 1 Result" in data:
                    ct1_result = data.split(":")[1].strip()
                if "Charging Test 2 Result" in data:
                    ct2_result = data.split(":")[1].strip()
                if "Charging Test 3 Result" in data:
                    ct3_result = data.split(":")[1].strip()
                if "O-Ring Test 1 Result" in data:
                    or1_result = data.split(":")[1].strip()
                if "O-Ring Test 2 Result" in data:
                    or2_result = data.split(":")[1].strip()
                if "O-Ring Test 3 Result" in data:
                    or3_result = data.split(":")[1].strip()
                if "Dry Input DC1 Shorted Result" in data:
                    dc1_short_result = data.split(":")[1].strip()
                if "Dry Input DC1 Result" in data:
                    dc1_result = data.split(":")[1].strip()
                if "Dry Input DC2 Shorted Result" in data:
                    dc2_short_result = data.split(":")[1].strip()
                if "Dry Input DC2 Result" in data:
                    dc2_result = data.split(":")[1].strip()
                if "ModBus Detached Result" in data:
                    modbus_detached_result = data.split(":")[1].strip()
                if "ModBus Attached Result" in data:
                    modbus_attached_result = data.split(":")[1].strip()

                if "Test Done!" in data:
                    row_data = [esn, current_time, board_id, vin_result, iin_result, vbat_result, ibat_result,
                                ct1_result, ct2_result, ct3_result, or1_result, or2_result, or3_result,
                                dc1_short_result, dc1_result, dc2_short_result, dc2_result, modbus_detached_result, modbus_attached_result]
                    add_data_to_csv(universal_file_path, row_data)
                    print("Test completed and data saved.")
                    if input("Type 'y' to exit: ").lower() == 'y':
                        break

    except serial.SerialException as e:
        print("Error:", e)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
