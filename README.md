# Mobile Fire Detection System

A comprehensive control system for a six-wheeled Unmanned Ground Vehicle (UGV) robot built on Raspberry Pi, featuring advanced sensor integration, computer vision, and web-based remote control.

![Rover CAD Model](docs/rover-cad.png)

## Overview

The project investigated how making a mobile fire detection system could be a big improvement in response time than the conventional fire alarm system. The goal of the project was to make a mobile fire detection system which could not only detect the fire or signs of fire but also give the status of the house and can be remotely controlled, even when away. There was a web browser based website which would constantly give the status of the house when there was no fire, but if there was fire or any sign of fire, there would be a notification. The testing first occurred in the house, then if the majority of the time the system was able to detect the fire and then give the notification, the testing occurred in the forest. The rover (the part that made the system mobile) was capable of climbing up and down the stairs and had 6 wheels. Not only was the ability to detect and give a notification of the fire going to be tested, but also the rover's ability to climb the stairs was going to be assessed. Both of the factors determined if this system passed or didn't pass. Because the rover might be limited to being terrestrial, a further improvement that could be made so every area in the forest could be monitored, was making a drone that could get launched from the rover (which would be improved so that it could be used as a launchpad for the drone), and then do surveillance over the forest. For further improvement, a drone would be added so it could reach every part of the forest in which the rover cannot reach.
Keywords: Mobile fire detection system, rover, drone, fire alarm, surveillance


Mobile Fire Detection System
	As of now, the majority of the fires tend to occur in the kitchen and in dry forests which is a really big hazard. More than 40 percent of the fires occur due to leaving the kitchen unattended, and can lead to many devastating effects that are hard to recover (NFPA, 2025).
	When the house is unattended, a fire alarm is ineffective. Even though the fire alarm is really loud, there is no notification system in order to notify the person if they are away, which makes it really hard to get an immediate response to the situation. Also fire alarms are not mobile and are not vision based, so the fire alarms may not be able to get to every single area giving the risk of the fire continuing to the fire alarm, which is when every object in its path is destroyed. A solution is to make a mobile fire detection system that includes a stair-climbing rover and one robot arm that has multiple fire detection sensors and has a camera. Unlike fire alarms, this approach can use computer vision including a YOLO model to detect the fire or any signs of fire, so that it can be dealt with before the situation gets worse. (Florida Atlantic University, 2025). 
Most importantly, the fire alarms cannot send a notification to the person and only the people near the house can hear the alarm, so, a website will be made, which gives the video clip of the fire and then gives a notification. Then for quick action the website will automatically call the fire station. 


### Key Features

- **Dual Base Controllers**: Primary and secondary motor controllers for six-wheel drive system
- **Rocker-Bogie Suspension**: Advanced suspension system for rough terrain navigation
- **360° LiDAR Scanning**: Slamtec RPLidar A1M8 for real-time 360-degree mapping
- **Computer Vision**: OpenCV-based object detection, face tracking, and on-screen display
- **Fire & Smoke Detection**: YOLOv8-based AI model for early fire and smoke detection
- **Gimbal Control**: Two-axis pan/tilt gimbal with Feetech STS3215 servos
- **Steering System**: Four servo motors for precise steering control
- **IR Temperature Sensor**: Ambient and object temperature monitoring
- **Web-Based Control**: Flask/SocketIO web interface for remote operation
- **Real-Time Video Streaming**: Live camera feed with OSD overlay

## Hardware Components

### Chassis & Mobility
- **6-Wheel Drive System**: Three wheels per side with independent control
- **Steering Servos**: 4 serial bus servos (SCS-series) for steering control
- **etc.**

### Sensors
- **RPLidar A1M8**: 360° 2D scanning LiDAR (12-meter range)
- **IR Temperature Sensor**: MLX90614 or similar for ambient/object temperature
- **Camera**: USB camera for computer vision and streaming
- **CPU Temperature**: On-board Raspberry Pi temperature monitoring

### Actuators
- **Gimbal Servos**: 2x Feetech STS3215 servos (Pan ID: 11, Tilt ID: 12)
- **Steering Servos**: 6x SCS-series servos for wheel steering

### Computing
- **Raspberry Pi**: Main control unit (Pi 4 or Pi 5)
- **2x ESP32**: Lower-level motor/sensor control via UART

## Software Architecture

### Upper Computer (Raspberry Pi)
- **Flask Web Server**: Web-based control interface
- **SocketIO**: Real-time bidirectional communication
- **OpenCV**: Computer vision and image processing
- **YOLOv8**: Fire and smoke detection
- **Serial Communication**: UART communication with lower computer

### Lower Computer (ESP32)
- Motor control
- Sensor data collection
- Low-level hardware interface

## Installation


### Web Interface Features

1. **Movement Control**: Joystick-style movement with speed control
2. **Steering Control**: Left/Right buttons for cumulative 5° steering adjustments
3. **Lidar Control**: ON/OFF buttons to start/stop 360° scanning
4. **Gimbal Control**: Pan and tilt sliders for camera positioning
5. **Temperature Display**: Real-time ambient and object temperatures (Celsius & Fahrenheit)
6. **Video Streaming**: Live camera feed with LiDAR point overlay
7. **Virtual Keyboard**: On-screen keyboard for touchscreen devices


## Configuration

### USB Device Mapping

The system uses udev rules to create persistent device symlinks:

- `/dev/base_secondary` - Secondary base controller
- `/dev/steer` - Steering servo controller
- `/dev/gimbal` - Gimbal servo controller
- `/dev/rplidar` - RPLidar sensor
- `/dev/irtemp` - IR temperature sensor

### Config.yaml

Key configuration options:

- `base_config`: Robot name, version, sensor options
- `cmd_config`: Command codes for various functions
- `args_config`: Speed and rate limits



## License

This project is based on the Waveshare UGV Rover codebase and has been extended for MFDS applications.

## Contributors

- **Sanatan Sinha** (sanrobo206) - Main developer and maintainer

## Acknowledgments

- Based on [Waveshare UGV Rover](https://github.com/waveshareteam/ugv_rpi) project
- Uses [YOLOv8](https://github.com/ultralytics/ultralytics) for fire/smoke detection
- Uses [rplidar-roboticia](https://github.com/roboticia/rplidar-roboticia) for LiDAR integration
- Selvam, R., Kumar, K. N., Vignesh, A. V., Vishva, R. and Surendaranand, P. Selvam, R., Kumar, K. N., Vignesh, A. V., Vishva, R., & Surendaranand, P. (2023). Cell Phone Controlled Robot With Fire Detection &Fire Fighting. Retrieved from https://www.ijert.org/cell-phone-controlled-robot-with-fire-detection-fire-fighting. Accessed 1 Oct. 2025.

- “Mobile Fire Extinguishing RobotTeam.” Florida Atlantic University, www.fau.edu/engineering/senior-design/projects/fall2022/mobile-fire-extinguishing-robotteam/. Accessed 2 Oct. 2025.

- “‘Home Cooking Fires’ Report: NFPA.” Nfpa.Org, www.nfpa.org/education-and-research/research/nfpa-research/fire-statistical-reports/home-cooking-fires. Accessed 3 Oct. 2025.

- Stair Climbing Rover. (n.d.). Retrieved from https://www.printables.com/model/194299-stair-climbing-rover?lang=en. Accessed 13 Nov. 2025.

- “State-of-the-Art Computer Vision Model.” YOLOv8, yolov8.com/. Accessed 30 Nov. 2025.

- Pollen-Robotics. “Pollen-Robotics/Rustypot: Communication with Dynamixel like Devices.” GitHub, github.com/pollen-robotics/rustypot. Accessed 30 Nov. 2025.

- Waveshareteam. “Waveshareteam/Ugv_rpi: Raspberry Pi Example for the WaveShare UGV Robots: WAVE ROVER, UGV Rover, UGV Beast, RaspRover, UGV01, UGV02.” GitHub, github.com/waveshareteam/ugv_rpi. Accessed 30 Nov. 2025.

- Adam-Software. (n.d.). Adam-Software/Feetech-Servo-SDK: Feetech Servo Python SDK. Copy official repository. Retrieved from https://github.com/Adam-Software/Feetech-Servo-SDK. Accessed 30 Nov. 2025.

- electronicsworkshop111, & Instructables. (2023). MLX90614 Non-Contact Infrared Temperature Sensor With Arduino. Retrieved from https://www.instructables.com/MLX90614-Non-Contact-Infrared-Temperature-Sensor-W/. Accessed 30 Nov. 2025.

- Opencv. “Opencv/Opencv: Open Source Computer Vision Library.” GitHub, github.com/opencv/opencv. Accessed 30 Nov. 2025.

- Ultralytics. “Quick Start Guide: Raspberry Pi with Ultralytics YOLO11.” Home - Ultralytics YOLO Docs, 16 Nov. 2025, docs.ultralytics.com/guides/raspberry-pi/. Accessed 30 Nov. 2025.


## Contact

For questions, issues, or contributions, please open an issue on GitHub.


