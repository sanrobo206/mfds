import sys
import time
from feetech_driver import FeetechDriver, ADDR_PRESENT_POSITION, ADDR_HOMING_OFFSET, ADDR_TORQUE_ENABLE, ADDR_LOCK

PORT = "/dev/ttyACM1"
BAUDRATE = 1000000
MIDPOINT_VAL = 2048 

def main():
    driver = FeetechDriver(PORT, BAUDRATE)
    try:
        driver.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    motor_id = int(input("Enter motor ID to set midpoint: ").strip())
    
    if not driver.ping(motor_id):
        print("Motor not found.")
        return

    print("Unlocking and disabling torque...")
    driver.write_byte(motor_id, ADDR_LOCK, 0)
    driver.write_byte(motor_id, ADDR_TORQUE_ENABLE, 0)

    input("\n>>> Move the motor to the desired MIDPOINT/HOME position manually.\n>>> Press ENTER when ready...")

    print("Clearing old Homing Offset to 0 to read TRUE RAW position...")
    driver.write_word(motor_id, ADDR_HOMING_OFFSET, 0)
    time.sleep(0.5) # Wait for write to take effect and position to update

    # Read raw position
    raw_pos = driver.read_word_raw(motor_id, ADDR_PRESENT_POSITION)
    if raw_pos is None:
        print("Failed to read position.")
        return
    
    print(f"True Raw Position: {raw_pos}")
    
    # Logic Correction (Reverted):
    # If the motor uses Present = Raw - Offset (Standard Feetech/Dynamixel behavior)
    # We want Present = 2048
    # 2048 = Raw - Offset
    # Offset = Raw - 2048
    
    new_offset = raw_pos - MIDPOINT_VAL
    print(f"Calculated New Offset (Raw - 2048): {new_offset}")
    
    # Write new offset
    # Note: write_word handles negative numbers by using 2's complement logic in Python (value & 0xFF)
    driver.write_word(motor_id, ADDR_HOMING_OFFSET, new_offset)
    
    # Re-lock
    driver.write_byte(motor_id, ADDR_LOCK, 1)
    time.sleep(0.5)

    # Verify
    check_pos = driver.read_word_raw(motor_id, ADDR_PRESENT_POSITION)
    print(f"New Reported Position (should be ~{MIDPOINT_VAL}): {check_pos}")
    
    print("Disabling Torque...")
    driver.write_byte(motor_id, ADDR_TORQUE_ENABLE, 0)
    
    print("Done.")

    driver.disconnect()

if __name__ == "__main__":
    main()
