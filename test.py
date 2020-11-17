import random

import machine
import st7789py as st7789
import time

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

sck = machine.Pin(18, machine.Pin.OUT)
mosi = machine.Pin(19, machine.Pin.OUT)

LEDK = machine.Pin(4, machine.Pin.OUT)
LEDK.on()


spi = machine.SPI(1, baudrate=27000000, polarity=1, sck = sck, mosi = mosi)
display = st7789.ST7789(
    spi, 135, 240,
    reset=machine.Pin(23, machine.Pin.OUT),
    dc=machine.Pin(16, machine.Pin.OUT),
    cs=machine.Pin(5, machine.Pin.OUT)
)

display.init()
print("starting while loop")
while True:
    display.fill(0xffffff)
    display.line(1,1,120,120,0x0)
    # display.fill_rect(0, 0, 135, 240,
    #     st7789.color565(
    #         random.getrandbits(8),
    #         random.getrandbits(8),
    #         random.getrandbits(8),
    #     ),
    # )
    time.sleep(1)
