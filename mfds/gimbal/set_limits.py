import sys
from feetech_driver import FeetechDriver, ADDR_PRESENT_POSITION, ADDR_MIN_POSITION, ADDR_MAX_POSITION, ADDR_TORQUE_ENABLE, ADDR_LOCK

PORT = "/dev/ttyACM1"
BAUDRATE = 1000000

def main():
    driver = FeetechDriver(PORT, BAUDRATE)
    try:
        driver.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    motor_id = int(input("Enter motor ID to set limits: ").strip())
    
    if not driver.ping(motor_id):
        print("Motor not found.")
        return

    print("\nDisabling torque for manual movement...")
    driver.write_byte(motor_id, ADDR_TORQUE_ENABLE, 0)
    
    print("Move motor to MINIMUM position and press ENTER.")
    input()
    min_val = driver.read_word_raw(motor_id, ADDR_PRESENT_POSITION)
    print(f"Read Min: {min_val}")
    
    print("Move motor to MAXIMUM position and press ENTER.")
    input()
    max_val = driver.read_word_raw(motor_id, ADDR_PRESENT_POSITION)
    print(f"Read Max: {max_val}")
    
    if min_val is None or max_val is None:
        print("Error reading positions.")
        return

    # Ensure min < max
    if min_val > max_val:
        print("Swapping min/max values...")
        min_val, max_val = max_val, min_val

    print(f"Limits to write -> Min: {min_val}, Max: {max_val}")
    
    confirm = input("Write limits? (y/n): ").strip().lower()
    if confirm == 'y':
        driver.write_byte(motor_id, ADDR_LOCK, 0)
        driver.write_word(motor_id, ADDR_MIN_POSITION, min_val)
        driver.write_word(motor_id, ADDR_MAX_POSITION, max_val)
        driver.write_byte(motor_id, ADDR_LOCK, 1)
        print("Limits written.")
    
    driver.disconnect()

if __name__ == "__main__":
    main()
