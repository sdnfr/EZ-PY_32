import random
import machine
import time
import utime
from machine import Pin
from micropython import const

#flashing micropython: 
# esptool.py --chip esp32 --port COM4 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
#copying files via ampy:
# ampy --port COM4 put test.py
CS = const(0x01<<21)
RD = const(0x01<<2)
WR = const(0x01<<0)
RST = const(0x01<<4)
CDRS = const(0x01<<5)
DATA = const(12)
col = const(0xf800)



@micropython.viper
def clear(x_1,y_1,x_2,y_2):
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register

    CLR[0] ^= CS
    x1 = int(x_1)
    y1 = int(y_1)
    x2 = int(x_2)
    y2 = int(y_2)
    SendCMD(0x2a)
    SendD(x1>>8)
    SendD(x1)
    SendD(x2>>8)
    SendD(x2)
    SendCMD(0x2b)
    SendD(y1>>8)
    SendD(y1)
    SendD(y2>>8)
    SendD(y2)
    SendCMD(0x2c)						 

    for i in range(320):
        for m in range(480):
            SendD(col>>8)
            SendD(col)

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


@micropython.viper
def SendCMD(c):
    cmd = int(c)
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register
    CLR[0] ^= CDRS

    # CLR[0] ^= 0xFF << DATA
    SET[0] ^= cmd << DATA
    WStrobe() 

    CLR[0] ^= 0xFF << DATA

@micropython.viper
def WStrobe():
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register
    CLR[0] ^= WR
    SET[0] ^= WR


@micropython.viper
def SendD(c):
    data = int(c)
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register

    SET[0] ^= CDRS

    # CLR[0] ^= 0xFF << DATA
    SET[0] ^= data << DATA
    WStrobe() 
    CLR[0] ^= 0xFF << DATA



@micropython.viper
def Reset():
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register


    #Reset part
    SET[0] ^= RST    
    utime.sleep_ms(5)
    CLR[0] ^= RST
    utime.sleep_ms(15)
    SET[0] ^= RST    
    utime.sleep_ms(15)




@micropython.viper
def Lcd_Init():
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register


    SET[0] ^= CS    
    SET[0] ^= WR   
    CLR[0] ^= CS

    SendCMD(0xF9)
    SendD(0x00)
    SendD(0x08)
    SendCMD(0xC0)
    SendD(0x19)
    SendD(0x1A)
    SendCMD(0xC1)
    SendD(0x45)
    SendD(0X00)
    SendCMD(0xC2)
    SendD(0x33)
    SendCMD(0xC5)
    SendD(0x00)
    SendD(0x28)
    SendCMD(0xB1)
    SendD(0x90)
    SendD(0x11)
    SendCMD(0xB4)
    SendD(0x02)
    SendCMD(0xB6)
    SendD(0x00)
    SendD(0x42)
    SendD(0x3B)
    SendCMD(0xB7)
    SendD(0x07)
    SendCMD(0xE0)
    SendD(0x1F)
    SendD(0x25)
    SendD(0x22)
    SendD(0x0B)
    SendD(0x06)
    SendD(0x0A)
    SendD(0x4E)
    SendD(0xC6)
    SendD(0x39)
    SendD(0x00)
    SendD(0x00)
    SendD(0x00)
    SendD(0x00)
    SendD(0x00)
    SendD(0x00)
    SendCMD(0xE1)
    SendD(0x1F)
    SendD(0x3F)
    SendD(0x3F)
    SendD(0x0F)
    SendD(0x1F)
    SendD(0x0F)
    SendD(0x46)
    SendD(0x49)
    SendD(0x31)
    SendD(0x05)
    SendD(0x09)
    SendD(0x03)
    SendD(0x1C)
    SendD(0x1A)
    SendD(0x00)
    SendCMD(0xF1)
    SendD(0x36)
    SendD(0x04)
    SendD(0x00)
    SendD(0x3C)
    SendD(0x0F)
    SendD(0x0F)
    SendD(0xA4)
    SendD(0x02)
    SendCMD(0xF2)
    SendD(0x18)
    SendD(0xA3)
    SendD(0x12)
    SendD(0x02)
    SendD(0x32)
    SendD(0x12)
    SendD(0xFF)
    SendD(0x32)
    SendD(0x00)
    SendCMD(0xF4)
    SendD(0x40)
    SendD(0x00)
    SendD(0x08)
    SendD(0x91)
    SendD(0x04)
    SendCMD(0xF8)
    SendD(0x21)
    SendD(0x04)
    SendCMD(0x36)
    SendD(0x48)
    SendCMD(0x3A)
    SendD(0x55)
    SendCMD(0x11)

    utime.sleep_ms(120)
    SendCMD(0x29)    



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

Reset()
Lcd_Init()
clear(0,0,320,480)
# reset()
# utime.sleep_ms(200)

# init()
# utime.sleep_ms(200)
# Address_set(0,0,320,480)





