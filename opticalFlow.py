import serial
import time
import numpy as np 
import threading

class SerialThread(threading.Thread):
    def __init__(self, serial_port, length=4):
        threading.Thread.__init__(self)
        self.serial_port = serial_port
        self.serial_read_data = []
        self.length = length
        self.finished = False

    def isFinished(self):
        return self.finished

    def getSerialData(self):
        return self.serial_read_data

    def run(self):
        self.finished = False
        res = serial_portF4.read(self.length)
        line = []
        for c in res:
            line.append(c)
        self.serial_read_data = np.array(line, np.uint8)
        self.finished = True



serial_portF4 = serial.Serial(
port='/dev/ttyUSB0',
baudrate=115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=0.04)

serial_portF4.write([0,1,2])

vhex = np.vectorize(hex)


while True:
    readSerialThread = SerialThread(serial_portF4, 100)
    readSerialThread.start()
    while not readSerialThread.isFinished():
        pass

    data = readSerialThread.getSerialData()

    if data.size < 20:
        continue
    print("Data Length="+str(data.size))
    print("Data is")
    
    print(vhex(data))
    
    time.sleep(1)


