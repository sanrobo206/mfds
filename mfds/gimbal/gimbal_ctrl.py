import time
import os
import sys

# Ensure we can import the driver from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from feetech_driver import FeetechDriver, ADDR_GOAL_POSITION, ADDR_TORQUE_ENABLE
except ImportError:
    print("Error importing FeetechDriver in gimbal_ctrl")
    FeetechDriver = None

class GimbalController:
    def __init__(self, port="/dev/gimbal", baudrate=1000000, pan_id=11, tilt_id=12):
        self.port = port
        self.baudrate = baudrate
        self.pan_id = pan_id
        self.tilt_id = tilt_id
        self.driver = None
        
        # Center positions (STS3215 is 0-4096)
        self.pan_center = 2048
        self.tilt_center = 2048
        self.steps_per_deg = 4096 / 360.0
        
        # Limits
        self.pan_min = 0
        self.pan_max = 4096
        self.tilt_min = 1500 # Physical limit guess
        self.tilt_max = 3000 # Physical limit guess

        if FeetechDriver:
            try:
                self.driver = FeetechDriver(port, baudrate)
                self.driver.connect()
                print(f"Gimbal connected on {port}")
                self.enable_torque()
            except Exception as e:
                print(f"Failed to connect to Gimbal on {port}: {e}")
                self.driver = None

    def enable_torque(self):
        if not self.driver: return
        try:
            self.driver.write_byte(self.pan_id, ADDR_TORQUE_ENABLE, 1)
            self.driver.write_byte(self.tilt_id, ADDR_TORQUE_ENABLE, 1)
        except Exception as e:
            print(f"Error enabling gimbal torque: {e}")

    def disable_torque(self):
        if not self.driver: return
        try:
            self.driver.write_byte(self.pan_id, ADDR_TORQUE_ENABLE, 0)
            self.driver.write_byte(self.tilt_id, ADDR_TORQUE_ENABLE, 0)
        except:
            pass

    def set_angles(self, pan_deg, tilt_deg):
        """
        Sets pan and tilt angles in degrees.
        0 is center.
        Range approx -180 to 180 for Pan.
        Range approx -90 to 90 for Tilt (clamped).
        """
        if not self.driver: return
        
        # Convert degrees to raw steps
        # Pan: +deg -> increase steps (or decrease depending on mounting)
        # Assuming +deg is CCW 
        pan_raw = int(self.pan_center + (pan_deg * self.steps_per_deg))
        tilt_raw = int(self.tilt_center + (tilt_deg * self.steps_per_deg))
        
        self.set_pan_raw(pan_raw)
        self.set_tilt_raw(tilt_raw)

    def set_pan_raw(self, raw_val):
        if not self.driver: return
        raw_val = max(self.pan_min, min(self.pan_max, int(raw_val)))
        try:
            self.driver.write_word(self.pan_id, ADDR_GOAL_POSITION, raw_val)
        except Exception as e:
            print(f"Gimbal write error: {e}")

    def set_tilt_raw(self, raw_val):
        if not self.driver: return
        raw_val = max(self.tilt_min, min(self.tilt_max, int(raw_val)))
        try:
            self.driver.write_word(self.tilt_id, ADDR_GOAL_POSITION, raw_val)
        except Exception as e:
            print(f"Gimbal write error: {e}")

    def home(self):
        self.set_pan_raw(self.pan_center)
        self.set_tilt_raw(self.tilt_center)

if __name__ == '__main__':
    # Test
    gc = GimbalController()
    if gc.driver:
        print("Centering...")
        gc.home()
        time.sleep(1)
        print("Pan +45")
        gc.set_angles(45, 0)
        time.sleep(1)
        print("Tilt +20")
        gc.set_angles(45, 20)
        time.sleep(1)
        print("Home")
        gc.home()

