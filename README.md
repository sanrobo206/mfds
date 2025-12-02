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

### Prerequisites

```bash
# Python 3.8+ required
python3 --version

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libopencv-dev
```

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanrobo206/mfds.git
   cd mfds
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv ugv_env
   source ugv_env/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure udev rules for USB devices**
   ```bash
   sudo cp 99-ugv-sensors.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

5. **Configure the system**
   - Edit `config.yaml` to match your hardware configuration
   - Set robot name, sensor options, and command codes

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the web interface**
   - Open browser to `http://<raspberry-pi-ip>:5000`
   - Or `http://localhost:5000` if running locally

## Project Structure

```
ugv_rpi/
├── app.py                 # Main Flask application
├── base_ctrl.py           # Base controller communication
├── cv_ctrl.py             # Computer vision functions
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── 99-ugv-sensors.rules   # USB device udev rules
├── mfds/
│   ├── steer/            # Steering servo control
│   ├── gimbal/           # Gimbal pan/tilt control
│   ├── lidar/            # RPLidar control and scanning
│   ├── irtemp/           # IR temperature sensor
│   └── yolo/             # YOLOv8 fire/smoke detection
├── templates/            # Web UI templates
│   ├── index.html        # Main control interface
│   └── control.js        # Frontend JavaScript
└── media/                # Images and media files
```

## Usage

### Web Interface Features

1. **Movement Control**: Joystick-style movement with speed control
2. **Steering Control**: Left/Right buttons for cumulative 5° steering adjustments
3. **Lidar Control**: ON/OFF buttons to start/stop 360° scanning
4. **Gimbal Control**: Pan and tilt sliders for camera positioning
5. **Temperature Display**: Real-time ambient and object temperatures (Celsius & Fahrenheit)
6. **Video Streaming**: Live camera feed with LiDAR point overlay
7. **Virtual Keyboard**: On-screen keyboard for touchscreen devices

### Command Line Testing

Individual modules can be tested independently:

```bash
# Test steering
python -m mfds.steer.steer_ctrl

# Test gimbal
python -m mfds.gimbal.gimbal_ctrl

# Test LiDAR
python -m mfds.lidar.rplidar_ctrl

# Test IR temperature
python -m mfds.irtemp.irtemp_read
```

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
- `audio_config`: Audio output settings

## Development

### Adding New Sensors

1. Create a new module in `mfds/<sensor_name>/`
2. Implement controller class with initialization and read methods
3. Add to `app.py` initialization
4. Update `config.yaml` with command codes
5. Add UI controls in `templates/index.html`
6. Update `templates/control.js` for frontend handling

### Adding New Actuators

1. Create controller module in `mfds/<actuator_name>/`
2. Implement control methods
3. Add command handlers in `app.py`
4. Update UI with control buttons/sliders

## Troubleshooting

### USB Devices Not Found

- Check udev rules: `ls -l /dev/base_secondary /dev/steer /dev/gimbal /dev/rplidar /dev/irtemp`
- Verify device paths: `ls -l /dev/serial/by-path/`
- Reload udev: `sudo udevadm control --reload-rules && sudo udevadm trigger`

### Sensor Values Showing Zero

- Check JavaScript console for errors
- Verify serial connections
- Check device permissions: `ls -l /dev/<device>`

### LiDAR Not Rotating

- Verify power supply (LiDAR requires adequate current)
- Check serial connection on `/dev/rplidar`
- Review terminal output for error messages

## License

This project is based on the Waveshare UGV Rover codebase and has been extended for MFDS applications.

## Contributors

- **Sanatan Sinha** (sanrobo206) - Main developer and maintainer

## Acknowledgments

- Based on [Waveshare UGV Rover](https://github.com/waveshareteam/ugv_rpi) project
- Uses [YOLOv8](https://github.com/ultralytics/ultralytics) for fire/smoke detection
- Uses [rplidar-roboticia](https://github.com/roboticia/rplidar-roboticia) for LiDAR integration

## Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

**Note**: Make sure to save the CAD image as `docs/rover-cad.png` or update the image path in this README to match your file location.

