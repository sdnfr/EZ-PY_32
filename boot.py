import drivers.ili9486py as disp
import drivers.encoder as enc
import network
import ubinascii
import password
import utime
import time
import urequests as requests
import ujson
import machine
from machine import Pin
from machine import Timer
import controller as con

#flashing micropython: 
# esptool.py --chip esp32 --port COM4 erase_flash
# esptool.py --chip esp32 --port COM4 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
#copying files via ampy:
# ampy --port COM4 put boot.py
# ampy --port COM4 put controller.py
# ampy --port COM4 put view.py
# ampy --port COM4 put logic.py
# ampy --port COM4 put drivers



disp.init()
con.init()
enc.init(con.onClick,con.onLeft,con.onRight)
while True:
	con.update()
	utime.sleep_ms(10)

