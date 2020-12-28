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


@micropython.viper
def reset():
    SET = ptr32(0x3FF44008) #Set Register
    CLR = ptr32(0x3FF4400C) #Clear Register

    CS = const(0x01<<15)
    RD = const(0x01<<2)
    WR = const(0x01<<0)
    RST = const(0x01<<4)
    CDRS = const(0x01<<5)
    DATA = const(6)

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


    #W Strobe    
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

cs	= machine.Pin(15, machine.Pin.OUT) #chip select
rd	= machine.Pin(2, machine.Pin.OUT) #read change this pin
wr	= machine.Pin(0, machine.Pin.OUT) #write
rst	= machine.Pin(4, machine.Pin.OUT) #reset, low level reset
cdrs= machine.Pin(5, machine.Pin.OUT) #command or data, low or high also called cd


cs.on()
rd.on()
wr.on()
rst.on()
cdrs.on()

utime.sleep_ms(2000)



reset()
#reset()
utime.sleep_ms(200)

#init()





