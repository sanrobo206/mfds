import serial
import time
import threading
import re

import os

class IRTempReader:
    def __init__(self, port="/dev/irtemp", baudrate=9600):
        # Fallback to ttyUSB1 if symlink doesn't exist
        # if not os.path.exists(port):
        #     port = '/dev/ttyUSB1'
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.current_temp = {"ambient_c": 0.0, "object_c": 0.0, "ambient_f": 0.0, "object_f": 0.0}
        self.running = False
        self.thread = None
        self.connected = False

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.connected = True
            print(f"IR Temp Sensor connected on {port}")
            self.start()
        except Exception as e:
            print(f"Failed to connect to IR Temp Sensor: {e}")

    def start(self):
        if not self.connected:
            return
        self.running = True
        self.thread = threading.Thread(target=self.read_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.ser:
            self.ser.close()

    def read_loop(self):
        while self.running and self.ser.is_open:
            try:
                if self.ser.in_waiting > 0:
                    # Expected format lines:
                    # Ambient = 26.89*C	Object = 24.83*C
                    # Ambient = 80.40*F	Object = 76.69*F
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        # Check for Celsius
                        if "*C" in line:
                            match = re.search(r"Ambient\s*=\s*([-+]?\d*\.\d+|\d+)\*C\s+Object\s*=\s*([-+]?\d*\.\d+|\d+)\*C", line)
                            if match:
                                self.current_temp["ambient_c"] = float(match.group(1))
                                self.current_temp["object_c"] = float(match.group(2))
                        # Check for Fahrenheit
                        elif "*F" in line:
                            match = re.search(r"Ambient\s*=\s*([-+]?\d*\.\d+|\d+)\*F\s+Object\s*=\s*([-+]?\d*\.\d+|\d+)\*F", line)
                            if match:
                                self.current_temp["ambient_f"] = float(match.group(1))
                                self.current_temp["object_f"] = float(match.group(2))
            except Exception as e:
                print(f"Error reading IR temp: {e}")
                time.sleep(1)
            time.sleep(0.01)

    def get_temp(self):
        return self.current_temp

if __name__ == '__main__':
    reader = IRTempReader()
    if reader.connected:
        try:
            while True:
                print(f"Current Temp: {reader.get_temp()}")
                time.sleep(1)
        except KeyboardInterrupt:
            reader.stop()

