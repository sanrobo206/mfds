import serial
import time
import os
import glob
import json
import subprocess
import sys

# Add path to import drivers
sys.path.append(os.path.join(os.path.dirname(__file__), 'mfds/gimbal'))
try:
    from feetech_driver import FeetechDriver
except ImportError:
    # Quick mock if driver missing, but it should be there
    FeetechDriver = None

def get_device_path(tty_dev):
    """Gets the physical path for a tty device"""
    try:
        # Run udevadm to get the path
        # udevadm info -q path -n /dev/ttyACM0
        cmd = f"udevadm info -q path -n {tty_dev}"
        result = subprocess.check_output(cmd, shell=True).decode().strip()
        # We want the part that represents the physical chain, typically ending before the tty part
        # But for rules, we usually match ENV{ID_PATH}
        
        cmd_path = f"udevadm info --query=property --name={tty_dev} | grep ID_PATH="
        res_path = subprocess.check_output(cmd_path, shell=True).decode().strip()
        return res_path.split('=')[1]
    except Exception as e:
        return f"Unknown_Path_{tty_dev}"

def test_servo(port, servo_id):
    """Returns True if servo_id responds on port"""
    if not FeetechDriver: return False
    try:
        driver = FeetechDriver(port, baudrate=1000000, timeout=0.1)
        driver.connect()
        res = driver.ping(servo_id)
        driver.disconnect()
        return res
    except:
        return False

def test_base_json(port):
    """Returns True if it looks like a Base Controller (JSON)"""
    try:
        ser = serial.Serial(port, 115200, timeout=1.5)
        # Flush
        ser.reset_input_buffer()
        # Send a JSON ping or status request
        # Command 1003 is often used for heartbeat or echo in these robots, or just ask for version
        ser.write(b'{"T":130}\n') 
        start = time.time()
        while time.time() - start < 1.5:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore')
                if line.strip().startswith('{') and '}' in line:
                    ser.close()
                    return True
        ser.close()
        return False
    except:
        return False

def main():
    print("Scanning /dev/ttyACM* devices...")
    ports = glob.glob('/dev/ttyACM*')
    
    mapping = {}
    
    for port in ports:
        print(f"\nChecking {port}...")
        path = get_device_path(port)
        print(f"  Path: {path}")
        
        identified = "Unknown"
        
        # 1. Check for Steer (Unique ID 13 or 15)
        # Steer has 11, 12, 13, 15. Gimbal has 11, 12.
        # If we find 13, it IS Steer.
        if test_servo(port, 13):
            print("  -> Found Servo ID 13 (Steer)")
            identified = "steer"
        
        # 2. If not Steer, check for Gimbal (ID 11)
        elif test_servo(port, 11):
            print("  -> Found Servo ID 11 (Gimbal)")
            identified = "gimbal"
            
        # 3. If neither, check for Base (JSON)
        elif test_base_json(port):
            print("  -> Responded to JSON (Base Controller)")
            # We need to distinguish Primary vs Secondary Base if possible.
            # Usually Primary is on a specific internal port or user knows.
            # For now, we label as base.
            identified = "base_candidate"
        
        mapping[port] = {"path": path, "type": identified}

    print("\n" + "="*50)
    print("RESULTS & SUGGESTED RULES")
    print("="*50)
    
    bases = [info for port, info in mapping.items() if info['type'] == 'base_candidate']
    
    # Heuristic for bases: 
    # If we have 2 bases, we might need user input, but we can list the paths.
    
    print("\nCopy these lines into your 99-ugv-sensors.rules file:\n")
    
    for port, info in mapping.items():
        if info['type'] == 'steer':
            print(f'# Steer Controller (Found on {port})')
            print(f'ENV{{ID_PATH}}=="{info["path"]}", SYMLINK+="steer", MODE:="0777"')
            print("")
        elif info['type'] == 'gimbal':
            print(f'# Gimbal Controller (Found on {port})')
            print(f'ENV{{ID_PATH}}=="{info["path"]}", SYMLINK+="gimbal", MODE:="0777"')
            print("")
            
    if len(bases) > 0:
        print("# Base Controllers (Please verify which is Primary/Secondary)")
        for i, info in enumerate(bases):
            # Assuming first one found might be primary, but let's just print
            print(f'# Base Candidate {i+1} (Found on {port})')
            print(f'ENV{{ID_PATH}}=="{info["path"]}", SYMLINK+="base_candidate_{i+1}", MODE:="0777"')
            print("")
            
    print("="*50)

if __name__ == "__main__":
    main()

