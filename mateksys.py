import serial
import time

# This function reads the velocity voltage from the Matek optical flow lidar sensor board.

def read_velocity():
    data = [0,0,0]
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.flush()
    ser.write(b'\x55')
    # Wait for 3 bytes from the lidar sensor
    while ser.in_waiting < 3:
        time.sleep(0.01)
    # Read the 3 bytes of data from the lidar sensor
    data = ser.read(3)
    # Check if the data is valid
    if data[0] == 0x59 and data[1] == 0x59:
        # Convert the data to a 16 bit integer
        velocity = data[2]
        if velocity & 0x80:
            velocity = velocity - 256
        return velocity
    else:
        return 0

if __name__ == '__main__':
    while True:
        velocity = read_velocity()
        print(velocity)
        time.sleep(0.1)

    