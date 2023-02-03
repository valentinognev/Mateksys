import serial
import time
import numpy as np
import threading
import matplotlib.pyplot as plt

###################################################################


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
        self.serial_read_data = line
        self.finished = True
###################################################################


def crc8_dvb_s2(crc, a):
    crc ^= np.uint8(a)
    for ii in range(0, 8):
        if np.uint8(crc & 0x80):
            crc = np.uint8(np.uint8(crc << 1) ^ 0xD5)
        else:
            crc = np.uint8(crc << 1)
    return crc
###################################################################


def checkSum(data):
    sum = np.uint8(0)
    for i in range(0, len(data)):
        sum = crc8_dvb_s2(sum, data[i])

    return sum
###################################################################


serial_portF4 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)

# serial_portF4.write([0, 1, 2])

vhex = np.vectorize(hex)


while True:
    readSerialThread = SerialThread(serial_portF4, 2000)
    readSerialThread.start()
    while not readSerialThread.isFinished():
        pass

    data = readSerialThread.getSerialData()

    if len(data) < 20:
        continue
    datac = ''.join(map(chr, data))
    delimiter = ''.join(map(chr, [0x24, 0x58]))
    splitted = datac.split(delimiter)
    uint8list = []
    uint8DataList = []
    floatDataList = []
    for strin in splitted:
        if len(strin) > 10:
            uint8array = np.array([ord(c) for c in strin], dtype=np.uint8)
            uint8list.append(uint8array)
            uint8DataList.append(uint8array[6:-1])
            floatDataList.append(uint8array[6:10].view(dtype=np.float32))
    #        uint8DataList.append(uint8array[2:-1].view(dtype=np.uint16))

    # # CRC Test
    # for uintArr in uint8list:
    #     print(uintArr[-1]-checkSum(uintArr[2:-1]))

 # Print uint8DataList
 
    longarrs=[]
    zarrs=[]

    for arr in uint8DataList:
      if len(arr)==9: 
        longarrs.append(arr)
      else:
        zarrs.append(arr)

    z = np.zeros((len(zarrs)))
    for i in range(len(zarrs)):
        z[i] = zarrs[i][1]

    x = np.zeros((len(longarrs)))
    y = np.zeros((len(longarrs)))
    for i in range(len(longarrs)):
        x[i] = longarrs[i][1:3].view(dtype=np.int16)
        y[i] = longarrs[i][5:7].view(dtype=np.int16)

    plt.plot(x-np.mean(x))
    # plt.plot(y-np.mean(y))
    plt.plot(z[0:-1:4]-np.mean(z))
    plt.show()

    for uintArr in xarrs:
        print(uintArr)

    time.sleep(.1)
