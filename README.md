# MFDS UGV Robot Control System

A comprehensive control system for a six-wheeled Unmanned Ground Vehicle (UGV) robot built on Raspberry Pi, featuring advanced sensor integration, computer vision, and web-based remote control.

![Rover CAD Model](docs/rover-cad.png)

## Overview

The MFDS (Multi-Function Detection System) UGV is an autonomous rover platform designed for exploration, monitoring, and detection tasks. The system integrates multiple sensors, actuators, and AI capabilities to provide a robust robotic platform.

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
- **Rocker-Bogie Suspension**: Lightweight, robust suspension for uneven terrain
- **Dual Motor Controllers**: Primary and secondary base controllers for wheel control
- **Steering Servos**: 4 serial bus servos (SCS-series) for steering control

### Sensors
- **RPLidar A1M8**: 360° 2D scanning LiDAR (12-meter range)
- **IR Temperature Sensor**: MLX90614 or similar for ambient/object temperature
- **Camera**: USB camera for computer vision and streaming
- **CPU Temperature**: On-board Raspberry Pi temperature monitoring

### Actuators
- **Gimbal Servos**: 2x Feetech STS3215 servos (Pan ID: 11, Tilt ID: 12)
- **Steering Servos**: 4x SCS-series servos for wheel steering

### Computing
- **Raspberry Pi**: Main control unit (Pi 4 or Pi 5)
- **ESP32**: Lower-level motor/sensor control via UART

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

