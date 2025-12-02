import sys
import os
from feetech_driver import FeetechDriver, ADDR_ID, ADDR_LOCK, ADDR_TORQUE_ENABLE

PORT = "/dev/ttyACM1"
BAUDRATE = 1000000

def main():
    driver = FeetechDriver(PORT, BAUDRATE)
    try:
        driver.connect()
    except Exception as e:
        print(f"Failed to connect to {PORT}: {e}")
        return

    print(f"Scanning port {PORT}...")
    
    # Use the driver's full scan capability
    # This might take ~10-15 seconds for 254 IDs
    print("Performing full bus scan (0-253)...")
    found_ids = driver.scan(0, 253)
    
    if not found_ids:
        print("No motors found on the bus.")
        # Try current ID input
        current_id_str = input("Enter current motor ID manually (if known): ").strip()
        if current_id_str.isdigit():
             found_ids.append(int(current_id_str))

    if not found_ids:
        return

    print("\nSelect a motor to change ID:")
    current_id = int(input(f"Enter ID from {found_ids}: ").strip())
    
    if not driver.ping(current_id):
        print(f"Cannot communicate with ID {current_id}")
        return

    new_id = int(input("Enter NEW ID (0-253): ").strip())
    
    print(f"Changing ID from {current_id} to {new_id}...")
    
    # Unlock EPROM (Lock = 0)
    driver.write_byte(current_id, ADDR_LOCK, 0)
    # Disable Torque (Torque_Enable = 0)
    driver.write_byte(current_id, ADDR_TORQUE_ENABLE, 0)
    # Write new ID
    err = driver.write_byte(current_id, ADDR_ID, new_id)
    
    if err == 0:
        print(f"Success! Motor ID changed to {new_id}")
        # Lock again? usually defaults to 1 on power cycle, but good practice
        driver.write_byte(new_id, ADDR_LOCK, 1)
    else:
        print("Failed to set ID (Communication error or NACK)")

    print("Disabling Torque...")
    # Torque was already disabled during ID set, but ensuring it here for safety on new ID
    driver.write_byte(new_id, ADDR_TORQUE_ENABLE, 0)

    driver.disconnect()

if __name__ == "__main__":
    main()
