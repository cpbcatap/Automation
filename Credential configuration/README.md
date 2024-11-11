# 8080 Proof Configuration Tool

This tool is designed for configuring the ST50H device credentials over serial communication. 
It reads configuration data, such as `Deveui`, `Appkey`, and `Appeui`, from a CSV file and writes it to the device via serial commands. 
The tool also sets predefined intervals for LoRa transmission and Modbus heartbeat.

## Features

- Serial communication with ST50H devices.
- Reads device credentials (ESN, Deveui, Appkey, Appeui) from `Credential.csv`.
- Sets LoRa transmission and Modbus heartbeat intervals.
- Verifies and saves device configurations.

## Prerequisites

- Python 3.x
- `pyserial` library

### Installation of Required Libraries

To install the required libraries, run:

```bash
pip install pyserial
