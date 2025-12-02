import time
import numpy as np

try:
    from rustypot import Scs0009PyController
except ImportError:
    print("rustypot not found, steer control will not work")
    Scs0009PyController = None

class SteerController:
    def __init__(self, port="/dev/steer", baudrate=1000000):
        self.ID_1 = 11 
        self.ID_2 = 12 
        self.ID_3 = 13 
        self.ID_4 = 15
        self.controller = None
        self.current_angle = 0
        
        if Scs0009PyController:
            try:
                self.controller = Scs0009PyController(
                    serial_port=port,
                    baudrate=baudrate,
                    timeout=0.5,
                )
                print(f"Steer controller connected on {port}")
                self.enable_torque()
            except Exception as e:
                print(f"Failed to connect to steer controller: {e}")

    def enable_torque(self):
        if not self.controller: return
        try:
            self.controller.write_torque_enable(self.ID_1, 1) 
            self.controller.write_torque_enable(self.ID_2, 1)
            self.controller.write_torque_enable(self.ID_3, 1) 
            self.controller.write_torque_enable(self.ID_4, 1)
        except Exception as e:
            print(f"Error enabling torque: {e}")

    def turn(self, angle: int):
        if not self.controller: return
        
        try:
            self.current_angle = angle
            self.controller.write_goal_speed(self.ID_1, 6)
            self.controller.write_goal_speed(self.ID_2, 6)
            self.controller.write_goal_speed(self.ID_3, 6)
            self.controller.write_goal_speed(self.ID_4, 6)
            
            Pos_1 = np.deg2rad(angle)
            Pos_2 = np.deg2rad(angle/2)
            
            self.controller.write_goal_position(self.ID_1, Pos_1)
            self.controller.write_goal_position(self.ID_2, Pos_1)
            self.controller.write_goal_position(self.ID_3, Pos_2)
            self.controller.write_goal_position(self.ID_4, Pos_2)
            time.sleep(0.01)
        except Exception as e:
            print(f"Error turning steer: {e}")

    def step_left(self, step=5):
        new_angle = self.current_angle + step
        # Optional: Add limits if necessary, e.g. -45 to 45
        self.turn(new_angle)

    def step_right(self, step=5):
        new_angle = self.current_angle - step
        self.turn(new_angle)

if __name__ == '__main__':
    sc = SteerController()
    while True:
        try:
            user_input_string = input("Please enter Angle: ")
            angle = int(user_input_string)
            sc.turn(angle)
        except ValueError:
            print("Invalid input")
