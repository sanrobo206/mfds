import sys
from feetech_driver import FeetechDriver, ADDR_HOMING_OFFSET, ADDR_MIN_POSITION, ADDR_MAX_POSITION, ADDR_TORQUE_ENABLE, ADDR_LOCK

PORT = "/dev/ttyACM1"
BAUDRATE = 1000000

def main():
    driver = FeetechDriver(PORT, BAUDRATE)
    try:
        driver.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    motor_id = int(input("Enter motor ID to RESET calibration: ").strip())
    
    if not driver.ping(motor_id):
        print("Motor not found.")
        return

    print(f"Resetting Motor {motor_id}...")
    print(" - Homing Offset -> 0")
    print(" - Min Limit -> 0")
    print(" - Max Limit -> 4095")
    
    driver.write_byte(motor_id, ADDR_LOCK, 0)
    driver.write_byte(motor_id, ADDR_TORQUE_ENABLE, 0)
    
    # Reset Offset
    driver.write_word(motor_id, ADDR_HOMING_OFFSET, 0)
    
    # Reset Limits
    driver.write_word(motor_id, ADDR_MIN_POSITION, 0)
    driver.write_word(motor_id, ADDR_MAX_POSITION, 4095)
    
    driver.write_byte(motor_id, ADDR_LOCK, 1)
    
    print("Reset Complete.")
    driver.disconnect()

if __name__ == "__main__":
    main()

