import time
import sys
import threading
import numpy as np
import os

try:
    from rplidar import RPLidar
except ImportError:
    print("rplidar module not found. Please install: pip install rplidar-roboticia")
    RPLidar = None

class LidarController:
    def __init__(self, port='/dev/rplidar', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.lidar = None
        self.scanning = False
        self.scan_thread = None
        # Shared buffer for the latest scan: [(quality, angle, distance), ...]
        self.latest_scan = []
        self.lock = threading.Lock()

        if RPLidar is None:
            print("Lidar library not available.")
            return

        try:
            self.lidar = RPLidar(self.port, baudrate=self.baudrate)
            # Try cleaning input buffer first
            # self.lidar.clear_input()
            info = self.lidar.get_info()
            print(f"LiDAR connected: {info}")
            health = self.lidar.get_health()
            print(f"LiDAR health: {health}")
        except Exception as e:
            print(f"Failed to connect to LiDAR on {self.port}: {e}")
            self.lidar = None

    def start_scan(self):
        if not self.lidar:
            print("Cannot start scan: LiDAR not connected or library missing.")
            return
        
        if self.scanning:
            print("Already scanning.")
            return

        self.scanning = True
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()
        print("LiDAR scanning started.")

    def stop_scan(self):
        if not self.scanning:
            return
        
        self.scanning = False
        if self.scan_thread:
            self.scan_thread.join(timeout=2.0)
        
        try:
            self.lidar.stop()
            self.lidar.stop_motor()
        except Exception as e:
            print(f"Error stopping LiDAR: {e}")
        print("LiDAR scanning stopped.")

    def _scan_loop(self):
        try:
            print("Starting scan loop...")
            # Try resetting lidar state before scanning
            try:
                self.lidar.reset()
                time.sleep(0.5)
            except:
                pass
            
            # iter_scans yields a list of tuples (quality, angle, distance)
            for scan in self.lidar.iter_scans(max_buf_meas=500):
                print(f"Got scan with {len(scan)} points")
                if not self.scanning:
                    print("Scanning flag is False, breaking loop")
                    break
                
                # Update the latest scan buffer
                with self.lock:
                    self.latest_scan = scan
                
                # Optional: Sleep slightly if needed, but iter_scans is usually blocking
                # time.sleep(0.01) 
        except Exception as e:
            print(f"LiDAR scan loop error: {e}")
            self.scanning = False

    def get_latest_scan(self):
        """Returns a copy of the latest scan data."""
        with self.lock:
            return list(self.latest_scan)

    def disconnect(self):
        self.stop_scan()
        if self.lidar:
            self.lidar.disconnect()
            self.lidar = None
            print("LiDAR disconnected.")

def simple_test():
    # Simple test routine
    lidar_ctrl = LidarController('/dev/ttyUSB0')
    if not lidar_ctrl.lidar:
        return

    try:
        lidar_ctrl.start_scan()
        start_time = time.time()
        
        while time.time() - start_time < 10:
            scan = lidar_ctrl.get_latest_scan()
            if scan:
                print(f"Scan received: {len(scan)} points")
                # Print first point as sample
                # Format: (quality, angle, distance)
                print(f"Sample point: {scan[0]}")
            else:
                print("Waiting for scan data...")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        lidar_ctrl.disconnect()

if __name__ == "__main__":
    simple_test()

