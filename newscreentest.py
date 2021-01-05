import random
import machine
import time
import utime
from machine import Pin
from micropython import const
import json 
import math



#define pins
CS_pin = const(19)
RD_pin = const(32)
WR_pin = const(22)
RST_pin = const(21)
CDRS_pin = const(23)

DO_pin = const(12)
D1_pin = const(14)
D2_pin = const(2)
D3_pin = const(15)
D4_pin = const(4)
D5_pin = const(16)
D6_pin = const(17)
D7_pin = const(13)



CS = const(0x01<<CS_pin)
RD = const(0x01<<RD_pin)
WR = const(0x01<<WR_pin)
RST = const(0x01<<RST_pin)
CDRS = const(0x01<<CDRS_pin)
DO = const(0x01<<DO_pin)
D1 = const(0x01<<D1_pin)
D2 = const(0x01<<D2_pin)
D3 = const(0x01<<D3_pin) 
D4 = const(0x01<<D4_pin)
D5 = const(0x01<<D5_pin)
D6 = const(0x01<<D6_pin)
D7 = const(0x01<<D7_pin)
dmask = const(0x01<< DO_pin ^ 0x01<< D1_pin ^0x01<< D2_pin ^ 0x01<< D3_pin ^ 0x01<< D4_pin ^ 0x01<< D5_pin ^ 0x01<< D6_pin ^ 0x01<< D7_pin)


#Constants
ch_wdth = const(6)
ch_hght = const(8)
scr_wdth = const(480)
scr_hght = const(320)

BLACK=const(0x0000)
WHITE=const(0xFFFF)
BLUE=const(0x001F)
RED=const(0xF800)
GREEN=const(0x07E0)
CYAN=const(0x07FF)
MAGENTA=const(0xF81F)
YELLOW=const(0xFFE0)


@micropython.viper
def Set_Addr_Window(x_1,y_1,x_2,y_2):
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	CLR[0] ^= int(CS)
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


@micropython.viper
def clear_Screen():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	c1 = int(col) &0xFF
	Set_Addr_Window(0,0,scr_wdth,scr_hght)

	setd = 0x0000
	setd ^= int(c1 & 0x01 > 0) << DO_pin
	setd ^= int(c1 & 0x02 > 0) << D1_pin
	setd ^= int(c1 & 0x04 > 0) << D2_pin
	setd ^= int(c1 & 0x08 > 0) << D3_pin
	setd ^= int(c1 & 0x10 > 0) << D4_pin
	setd ^= int(c1 & 0x20 > 0) << D5_pin
	setd ^= int(c1 & 0x40 > 0) << D6_pin
	setd ^= int(c1 & 0x80 > 0) << D7_pin
	c1_d = setd &int(dmask)
	for i in range(scr_hght):
		for m in range(scr_wdth):
		SET[0] ^= c1_d
		CLR[0] ^= int(WR)
		SET[0] ^= int(WR)
		CLR[0] ^= int(dmask)
		
		SET[0] ^= c1_d
		CLR[0] ^= int(WR)
		SET[0] ^= int(WR)
		CLR[0] ^= int(dmask)
	SET[0] ^= int(CS)

@micropython.viper
def fill_Screen(color):
	col  =int(color)
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	c1 = int(col>>8) &0xFF
	c2 = int(col) &0xFF
	Set_Addr_Window(0,0,scr_wdth,scr_hght)

	setd = 0x0000
	setd ^= int(c1 & 0x01 > 0) << DO_pin
	setd ^= int(c1 & 0x02 > 0) << D1_pin
	setd ^= int(c1 & 0x04 > 0) << D2_pin
	setd ^= int(c1 & 0x08 > 0) << D3_pin
	setd ^= int(c1 & 0x10 > 0) << D4_pin
	setd ^= int(c1 & 0x20 > 0) << D5_pin
	setd ^= int(c1 & 0x40 > 0) << D6_pin
	setd ^= int(c1 & 0x80 > 0) << D7_pin
	c1_d = setd &int(dmask)

	setd = 0x0000
	setd ^= int(c2 & 0x01 > 0) << DO_pin
	setd ^= int(c2 & 0x02 > 0) << D1_pin
	setd ^= int(c2 & 0x04 > 0) << D2_pin
	setd ^= int(c2 & 0x08 > 0) << D3_pin
	setd ^= int(c2 & 0x10 > 0) << D4_pin
	setd ^= int(c2 & 0x20 > 0) << D5_pin
	setd ^= int(c2 & 0x40 > 0) << D6_pin
	setd ^= int(c2 & 0x80 > 0) << D7_pin
	c2_d = setd &int(dmask)

	SET[0] ^= int(CDRS)
	for i in range(scr_hght*scr_wdth):
		SET[0] ^= c1_d
		CLR[0] ^= int(WR)
		SET[0] ^= int(WR)
		CLR[0] ^= int(dmask)

		SET[0] ^= c2_d
		CLR[0] ^= int(WR)
		SET[0] ^= int(WR)
		CLR[0] ^= int(dmask)

	SET[0] ^= int(CS)

@micropython.viper
def SendCMD(c):

	cmd = int(c) & 0xFF
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register
	CLR[0] ^= int(CDRS)

	setd = 0x0000

	setd ^= int(cmd & 0x01 > 0) << DO_pin
	setd ^= int(cmd & 0x02 > 0) << D1_pin
	setd ^= int(cmd & 0x04 > 0) << D2_pin
	setd ^= int(cmd & 0x08 > 0) << D3_pin
	setd ^= int(cmd & 0x10 > 0) << D4_pin
	setd ^= int(cmd & 0x20 > 0) << D5_pin
	setd ^= int(cmd & 0x40 > 0) << D6_pin
	setd ^= int(cmd & 0x80 > 0) << D7_pin
	setd &= int(dmask)
	SET[0] ^= setd
	CLR[0] ^= int(WR)
	SET[0] ^= int(WR)
	CLR[0] ^= int(dmask)

@micropython.viper
def SendD(c):
	data = int(c) & 0xFF
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	SET[0] ^= int(CDRS)

	setd = 0x0000

	setd ^= int(data & 0x01 > 0) << DO_pin
	setd ^= int(data & 0x02 > 0) << D1_pin
	setd ^= int(data & 0x04 > 0) << D2_pin
	setd ^= int(data & 0x08 > 0) << D3_pin
	setd ^= int(data & 0x10 > 0) << D4_pin
	setd ^= int(data & 0x20 > 0) << D5_pin
	setd ^= int(data & 0x40 > 0) << D6_pin
	setd ^= int(data & 0x80 > 0) << D7_pin
	setd &= int(dmask)
	SET[0] ^= setd
	CLR[0] ^= int(WR)
	SET[0] ^= int(WR)
	CLR[0] ^= int(dmask)




@micropython.viper
def Reset():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	#Reset part
	SET[0] ^= int(RST)
	utime.sleep_ms(5)
	CLR[0] ^= int(RST)
	utime.sleep_ms(15)
	SET[0] ^= int(RST)
	utime.sleep_ms(15)

@micropython.viper
def Lcd_Init():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register


	SET[0] ^= int(CS)
	SET[0] ^= int(WR)
	CLR[0] ^= int(CS)

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
	SendD(0x78) #rotate 270 degrees horizontal
	SendCMD(0x3A)
	SendD(0x55)
	SendCMD(0x11)

	utime.sleep_ms(120)
	SendCMD(0x29)

def init():
	machine.Pin(CS_pin, machine.Pin.OUT).on() #chip select
	machine.Pin(RD_pin, machine.Pin.OUT).on() #read change this pin
	machine.Pin(WR_pin, machine.Pin.OUT).on() #write
	machine.Pin(RST_pin, machine.Pin.OUT).on() #reset, low level reset
	machine.Pin(CDRS_pin, machine.Pin.OUT).on() #command or data, low or high also called cd

	d0	= machine.Pin(DO_pin, machine.Pin.OUT)
	d1	= machine.Pin(D1_pin, machine.Pin.OUT)
	d2	= machine.Pin(D2_pin, machine.Pin.OUT)
	d3	= machine.Pin(D3_pin, machine.Pin.OUT)
	d4	= machine.Pin(D4_pin, machine.Pin.OUT)
	d5	= machine.Pin(D5_pin, machine.Pin.OUT)
	d6	= machine.Pin(D6_pin, machine.Pin.OUT)
	d7	= machine.Pin(D7_pin, machine.Pin.OUT)



	Reset()
	Lcd_Init()
	clear_Screen()


init()

before_us = time.ticks_ms()
fill_Screen(MAGENTA)
after_us = time.ticks_ms()
print('1 us from ' + str(before_us) + " to " + str(after_us))
before_us = time.ticks_ms()
fill_Screen(CYAN)
after_us = time.ticks_ms()
print('2 us from ' + str(before_us) + " to " + str(after_us))