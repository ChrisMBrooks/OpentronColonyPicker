import serial
import time
ser=serial.Serial('/dev/ttyACM0',9800, timeout=1)
time.sleep(2)
ser.write(b'H')

time.sleep(5)
ser.write(b'L')
ser.close()