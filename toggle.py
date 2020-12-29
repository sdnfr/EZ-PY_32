import random
import machine
import time
import utime
from machine import Pin
from micropython import const

#flashing micropython: 
# esptool.py --chip esp32 --port COM4 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
#copying files via ampy:
# ampy --port COM3 put test.py
CS = const(0x01<<21)
RD = const(0x01<<2)
WR = const(0x01<<0)
RST = const(0x01<<4)
CDRS = const(0x01<<5)
DATA = const(12)
col = const(0xf800)

@micropython.viper
def reset():
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register



    SET[0] ^= CS    
    SET[0] ^= RD    
    SET[0] ^= WR   
    SET[0] ^= CDRS

    CLR[0] ^= RST    

    utime.sleep_ms(3)


    SET[0] ^= RST    
    CLR[0] ^= CS
    CLR[0] ^= CDRS
    #CLR[0] ^= 0xFF < DATA


    #W Strobe 4 low    
    CLR[0] ^= WR
    SET[0] ^= WR
    CLR[0] ^= WR
    SET[0] ^= WR
    CLR[0] ^= WR
    SET[0] ^= WR
    CLR[0] ^= WR
    SET[0] ^= WR


    SET[0] ^= CS    
    CLR[0] ^= RST


@micropython.viper
def init():
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register


    initTable = [
        [0xF1,0x36,0x04,0x00,0x3C,0x0F,0x8F],
        [0xF2,0x18,0xA3,0x12,0x02,0xB2,0x12,0xFF,0x10,0x00],
        [0xF8,0x21,0x04],
        [0xF9,0x00,0x08],
        [0x36,0x08],
        [0xB4,0x00],
        [0xC1,0x41],
        [0xC5,0x00,0x91,0x80,0x00],
        [0xE0,0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x00],
        [0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00],
        [0x3A,0x55],
        [0x11],
        [0x36,0x28],
        #delay
        [0x29]
    ]

    SET[0] ^= CS
    SET[0] ^= RD
    SET[0] ^= WR

    for e in initTable:        
        l = len(e)
        x = range(1,l)
        cmd = int(e[0])
        CLR[0] ^= CS
        CLR[0] ^= CDRS


        #first command 0x00
        CLR[0] ^= 0xFF << DATA
        SET[0] ^= 0x00 << DATA
        #W Strobe    
        CLR[0] ^= WR
        SET[0] ^= WR

        #second command e[0]
        SET[0] ^= cmd << DATA
        #W Strobe    
        CLR[0] ^= WR
        SET[0] ^= WR

        #sending data now
        CLR[0] ^= 0xFF << DATA

        SET[0] ^= CDRS
        for n in x:
            data = int(e[n])
            SET[0] ^= data << DATA
            #W Strobe    
            CLR[0] ^= WR
            SET[0] ^= WR
            CLR[0] ^= 0xFF << DATA
        SET[0] ^= CS




@micropython.viper
def Address_set(x_1,y_1,x_2,y_2):
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register
    x1 = int(x_1)
    y1 = int(y_1)
    x2 = int(x_2)
    y2 = int(y_2)

    CLR[0] ^= CS

    #sending command now
    CLR[0] ^= CDRS

    #first command 0x00
    CLR[0] ^= 0xFF << DATA
    SET[0] ^= 0x00 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    #second command 0x2a
    SET[0] ^= 0x2a << DATA
    CLR[0] ^= WR
    SET[0] ^= WR


    #sending data now
    SET[0] ^= CDRS

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= x1>>8 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= x1 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= x2>>8 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= x2 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA

    #sending command now
    CLR[0] ^= CDRS

    #first command 0x00
    CLR[0] ^= 0xFF << DATA
    SET[0] ^= 0x00 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    #second command 0x2b
    SET[0] ^= 0x2b << DATA
    CLR[0] ^= WR
    SET[0] ^= WR


    #sending data now
    SET[0] ^= CDRS

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= y1>>8 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= y1 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= y2>>8 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA
    SET[0] ^= y2 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    CLR[0] ^= 0xFF << DATA

    #sending command now
    CLR[0] ^= CDRS

    #first command 0x00
    CLR[0] ^= 0xFF << DATA
    SET[0] ^= 0x00 << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    #second command 0x2b
    SET[0] ^= 0x2c << DATA
    CLR[0] ^= WR
    SET[0] ^= WR

    #sending data now
    SET[0] ^= CDRS

    for i in range(320):
        for m in range(480):
            CLR[0] ^= 0xFF << DATA
            SET[0] ^= col>>8 << DATA
            CLR[0] ^= WR
            SET[0] ^= WR

            CLR[0] ^= 0xFF << DATA
            SET[0] ^= col << DATA
            CLR[0] ^= WR
            SET[0] ^= WR

    
    SET[0] ^= CS




@micropython.viper
def toggle():
    GPIO_SET = ptr32(0x3FF44008) # GPIO base register
    GPIO_CLEAR = ptr32(0x3FF4400C) # GPIO base register
    GPIO = ptr32(0x3FF44004) # GPIO base register

    for i in range(100):
        GPIO_SET[0] ^= 0x10 # set bit 2    
        GPIO_CLEAR[0] ^= 0x10 # set bit 2
        GPIO_SET[0] ^= 0x10 # set bit 2    
        GPIO_CLEAR[0] ^= 0x10 # set bit 2





print('toggle test')

cs	= machine.Pin(21, machine.Pin.OUT) #chip select
rd	= machine.Pin(2, machine.Pin.OUT) #read change this pin
wr	= machine.Pin(0, machine.Pin.OUT) #write
rst	= machine.Pin(4, machine.Pin.OUT) #reset, low level reset
cdrs= machine.Pin(5, machine.Pin.OUT) #command or data, low or high also called cd

d0	= machine.Pin(12, machine.Pin.OUT)
d1	= machine.Pin(13, machine.Pin.OUT)
d2	= machine.Pin(14, machine.Pin.OUT)
d3	= machine.Pin(15, machine.Pin.OUT)
d4	= machine.Pin(16, machine.Pin.OUT)
d5	= machine.Pin(17, machine.Pin.OUT)
d6	= machine.Pin(18, machine.Pin.OUT)
d7	= machine.Pin(19, machine.Pin.OUT)


cs.on()
rd.on()
wr.on()
rst.on()
cdrs.on()

utime.sleep_ms(2000)



reset()
reset()
utime.sleep_ms(200)

init()
utime.sleep_ms(200)
Address_set(0,0,320,480)





