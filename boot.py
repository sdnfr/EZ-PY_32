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
import maincontroller as con

#flashing micropython: 
# esptool.py --chip esp32 --port COM4 erase_flash
# esptool.py --chip esp32 --port COM4 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
#copying files via ampy:
# ampy --port COM4 put test.py



# def http_get(url):
#	 import socket
#	 _, _, host, path = url.split('/', 3)
#	 addr = socket.getaddrinfo(host, 3000)[0][-1]

#	 s = socket.socket()
#	 s.connect(addr)
#	 s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
#	 while True:
#		 data = s.recv(100)
#		 if data:
#			 print(str(data, 'utf8'), end='')
#		 else:
#			 break
#	 s.close()



#get wlan networks
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)	   # activate the interface

nets = wlan.scan()
wlannetworks = []
for net in nets:
	wlannetworks.append(net[0].decode("utf-8")) 

# wlan.connect(password.essid, password.pw)
#print(http_get('http://192.168.2.102/data'))
# res = requests.get(url='http://192.168.2.102:3000/data')
# print(res.text)


disp.init()
con.init()
enc.init(con.onClick,con.onLeft,con.onRight)
while True:
	con.update()
	utime.sleep_ms(10)

