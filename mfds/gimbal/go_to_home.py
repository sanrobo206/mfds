import sys
import time
from feetech_driver import FeetechDriver, ADDR_GOAL_POSITION, ADDR_TORQUE_ENABLE

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

    motor_id_str = input("Enter motor ID (or 'all'): ").strip()
    
    ids_to_move = []
    if motor_id_str.lower() == 'all':
        print("Scanning for all motors...")
        ids_to_move = driver.scan()
        if not ids_to_move:
            print("No motors found.")
            return
    elif motor_id_str.isdigit():
        ids_to_move = [int(motor_id_str)]
    else:
        print("Invalid input.")
        return

    print(f"Moving ID(s) {ids_to_move} to MIDPOINT ({MIDPOINT_VAL})...")

    for mid in ids_to_move:
        # Enable Torque
        driver.write_byte(mid, ADDR_TORQUE_ENABLE, 1)
        # Send Goal
        driver.write_word(mid, ADDR_GOAL_POSITION, MIDPOINT_VAL)
        print(f" -> Sent ID {mid}")

    print("Done. Disabling torque in 2 seconds...")
    time.sleep(2.0)
    
    for mid in ids_to_move:
        driver.write_byte(mid, ADDR_TORQUE_ENABLE, 0)
    
    driver.disconnect()

if __name__ == "__main__":
    main()

