import sys
import time
from feetech_driver import FeetechDriver, ADDR_GOAL_POSITION, ADDR_TORQUE_ENABLE, ADDR_LOCK

PORT = "/dev/ttyACM1"
BAUDRATE = 1000000
MIDPOINT_VAL = 2048
AMPLITUDE = 500 # Move +/- 500 steps from center

def main():
    driver = FeetechDriver(PORT, BAUDRATE)
    try:
        driver.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    motor_id = int(input("Enter motor ID to test: ").strip())
    
    if not driver.ping(motor_id):
        print(f"Motor {motor_id} not found.")
        return

    print(f"Enabling Torque on Motor {motor_id}...")
    # Ensure torque is enabled so it can move
    driver.write_byte(motor_id, ADDR_TORQUE_ENABLE, 1)

    print(f"Moving to +{AMPLITUDE} steps (Right/Up)...")
    target = MIDPOINT_VAL + AMPLITUDE
    driver.write_word(motor_id, ADDR_GOAL_POSITION, target)
    time.sleep(1.5) # Wait for move

    print(f"Moving to -{AMPLITUDE} steps (Left/Down)...")
    target = MIDPOINT_VAL - AMPLITUDE
    driver.write_word(motor_id, ADDR_GOAL_POSITION, target)
    time.sleep(1.5) # Wait for move

    print("Returning to MIDPOINT (Home)...")
    driver.write_word(motor_id, ADDR_GOAL_POSITION, MIDPOINT_VAL)
    time.sleep(1.0)

    print("Test Complete. Motor should be centered.")
    
    print("Disabling Torque...")
    driver.write_byte(motor_id, ADDR_TORQUE_ENABLE, 0)
    
    driver.disconnect()

if __name__ == "__main__":
    main()

