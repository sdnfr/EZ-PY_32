import random

import machine
# import st7789py as st7789
import time
import ili9486py as ili9486


#uaed command: ampy --port COM3 put test.py




# p0 = Pin(2, Pin.OUT)    # create output pin on GPIO0
# p0.on()                 # set pin to "on" (high) level
# utime.sleep_ms(3000)
# p0.off()

# wlan = network.WLAN(network.STA_IF) # create station interface
# wlan.active(True)       # activate the interface
# networks = wlan.scan()             # scan for access points

# for network in networks:
#     print(network)
# esp32.raw_temperature()

# sck = machine.Pin(18, machine.Pin.OUT)
# mosi = machine.Pin(19, machine.Pin.OUT)

# LEDK = machine.Pin(4, machine.Pin.OUT)
# LEDK.on()

# d0	= machine.Pin(26, machine.Pin.OUT)
# d1	= machine.Pin(25, machine.Pin.OUT)
# d2	= machine.Pin(33, machine.Pin.OUT)
# d3	= machine.Pin(25, machine.Pin.OUT)
# d4	= machine.Pin(26, machine.Pin.OUT)
# d5	= machine.Pin(22, machine.Pin.OUT)
# d6	= machine.Pin(21, machine.Pin.OUT)
# d7	= machine.Pin(27, machine.Pin.OUT)

# time.sleep(1)
# d0.on()
# time.sleep(1)
# d0.off()
# d1.on()
# time.sleep(1)
# d1.off()
# d2.on()
# time.sleep(1)
# d2.off()
# d3.on()
# time.sleep(1)
# d3.off()
# d4.on()
# time.sleep(1)
# d4.off()
# d5.on()
# time.sleep(1)
# d5.off()
# d6.on()
# time.sleep(1)
# d6.off()
# d7.on()
# time.sleep(1)
# d7.off()


print("test")
paralellDriver = ili9486.parallell8bitDriver(
    rst	= machine.Pin(26, machine.Pin.OUT), #reset, low level reset
 	cs	= machine.Pin(26, machine.Pin.OUT), #chip select
 	rs	= machine.Pin(25, machine.Pin.OUT), #command or data, low or high also called cd
	wr	= machine.Pin(33, machine.Pin.OUT), #write
	rd	= machine.Pin(5, machine.Pin.OUT), #read change this pin
	d0	= machine.Pin(12, machine.Pin.OUT),
	d1	= machine.Pin(13, machine.Pin.OUT),
	d2	= machine.Pin(15, machine.Pin.OUT),
	d3	= machine.Pin(2, machine.Pin.OUT),
	d4	= machine.Pin(17, machine.Pin.OUT),
	d5	= machine.Pin(22, machine.Pin.OUT),
	d6	= machine.Pin(21, machine.Pin.OUT),
	d7	= machine.Pin(27, machine.Pin.OUT))

display = ili9486.ILI9486(paralellDriver,240,240,0)
display.initDisplay()
display.fill_rect(10, 150, 205, 205)





# for i in range(10):
#     display.initDisplay()
#     time.sleep(1)



# spi = machine.SPI(1, baudrate=27000000, polarity=1, sck = sck, mosi = mosi)
# display = st7789.ST7789(
#     spi, 135, 240,
#     reset=machine.Pin(23, machine.Pin.OUT),
#     dc=machine.Pin(16, machine.Pin.OUT),
#     cs=machine.Pin(5, machine.Pin.OUT)
# )

# display.init()
# print("starting while loop")
# while True:
#     display.fill(0xffffff)
#     display.line(1,1,120,120,0x0)
#     # display.fill_rect(0, 0, 135, 240,
#     #     st7789.color565(
#     #         random.getrandbits(8),
#     #         random.getrandbits(8),
#     #         random.getrandbits(8),
#     #     ),
#     # )
#     time.sleep(1)
