import serial
import time
import struct

# Instructions
INST_PING = 1
INST_READ = 2
INST_WRITE = 3
INST_REG_WRITE = 4
INST_ACTION = 5
INST_SYNC_READ = 130
INST_SYNC_WRITE = 131

# Addresses (STS3215 / STS Series)
ADDR_ID = 5
ADDR_BAUD_RATE = 6
ADDR_MIN_POSITION = 9
ADDR_MAX_POSITION = 11
ADDR_HOMING_OFFSET = 31
ADDR_TORQUE_ENABLE = 40
ADDR_GOAL_POSITION = 42
ADDR_LOCK = 55
ADDR_PRESENT_POSITION = 56

class FeetechDriver:
    def __init__(self, port, baudrate=1000000, timeout=0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        if self.ser is None:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

    def disconnect(self):
        if self.ser:
            self.ser.close()
            self.ser = None

    def _calc_checksum(self, data):
        return (~sum(data)) & 0xFF

    def _write_packet(self, motor_id, instruction, params):
        length = len(params) + 2
        packet = [0xFF, 0xFF, motor_id, length, instruction] + params
        checksum = self._calc_checksum(packet[2:])
        packet.append(checksum)
        
        # Clear buffer
        self.ser.reset_input_buffer()
        self.ser.write(bytearray(packet))

    def _read_packet(self, expected_id, expected_length):
        # Header + ID + Len + Error + Params + Checksum
        # Response length = expected_length + 6
        # Wait for header
        start = time.time()
        while time.time() - start < self.timeout:
            if self.ser.in_waiting >= 4:
                header = self.ser.read(4)
                if header[0] == 0xFF and header[1] == 0xFF:
                    id_ = header[2]
                    length = header[3]
                    if id_ != expected_id:
                        continue
                    
                    # Read rest of packet
                    to_read = length
                    body = self.ser.read(to_read)
                    if len(body) < to_read:
                        return None, None # Incomplete
                    
                    error = body[0]
                    params = body[1:-1]
                    checksum = body[-1]
                    
                    # Verify checksum
                    calc_sum = self._calc_checksum([id_, length] + list(body[:-1]))
                    if calc_sum != checksum:
                        print("Checksum error")
                        return None, None
                        
                    return error, params
        return None, None

    def write_byte(self, motor_id, address, value):
        self._write_packet(motor_id, INST_WRITE, [address, value])
        err, _ = self._read_packet(motor_id, 0)
        return err

    def write_word(self, motor_id, address, value):
        low = value & 0xFF
        high = (value >> 8) & 0xFF
        self._write_packet(motor_id, INST_WRITE, [address, low, high])
        err, _ = self._read_packet(motor_id, 0)
        return err

    def read_byte(self, motor_id, address):
        self._write_packet(motor_id, INST_READ, [address, 1])
        err, params = self._read_packet(motor_id, 1)
        if err is not None and len(params) == 1:
            return params[0]
        return None

    def read_word(self, motor_id, address):
        self._write_packet(motor_id, INST_READ, [address, 2])
        err, params = self._read_packet(motor_id, 2)
        if err is not None and len(params) == 2:
            val = params[0] | (params[1] << 8)
            # Handle signed 16-bit
            if val > 32767:
                val -= 65536
            return val
        return None
    
    def read_word_raw(self, motor_id, address):
         # Unsigned read
        self._write_packet(motor_id, INST_READ, [address, 2])
        err, params = self._read_packet(motor_id, 2)
        if err is not None and len(params) == 2:
            val = params[0] | (params[1] << 8)
            return val
        return None

    def ping(self, motor_id):
        self._write_packet(motor_id, INST_PING, [])
        err, _ = self._read_packet(motor_id, 0)
        return err is not None

    def scan(self, start_id=0, end_id=253):
        found = []
        for i in range(start_id, end_id + 1):
            if self.ping(i):
                found.append(i)
                print(f"Found ID {i}")
        return found

