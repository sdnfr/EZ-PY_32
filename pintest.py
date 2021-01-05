import random
import machine
import time
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


#const pins
CS1 = const(0x01<<19)
RD1 = const(0x01<<32)
WR1 = const(0x01<<22)
RST1 = const(0x01<<21)
CDRS1 = const(0x01<<23)
dmask1 = const(0x3F014)


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

@micropython.viper
def SendCMD(c):

	cmd = int(c) & 0xFF
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register
	CLR[0] ^= int(CDRS)

	setd = 0x0000
	setd ^= ((cmd & 0x01) >> 0 )<< DO
	setd ^= ((cmd & 0x02) >> 1 )<< D1
	setd ^= ((cmd & 0x04) >> 2 )<< D2
	setd ^= ((cmd & 0x08) >> 3 )<< D3
	setd ^= ((cmd & 0x10) >> 4 )<< D4
	setd ^= ((cmd & 0x20) >> 5 )<< D5
	setd ^= ((cmd & 0x40) >> 6 )<< D6
	setd ^= ((cmd & 0x80) >> 7 )<< D7
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
	setd ^= ((data & 0x01) >> 0 )<< DO
	setd ^= ((data & 0x02) >> 1 )<< D1
	setd ^= ((data & 0x04) >> 2 )<< D2
	setd ^= ((data & 0x08) >> 3 )<< D3
	setd ^= ((data & 0x10) >> 4 )<< D4
	setd ^= ((data & 0x20) >> 5 )<< D5
	setd ^= ((data & 0x40) >> 6 )<< D6
	setd ^= ((data & 0x80) >> 7 )<< D7
	setd &= int(dmask)
	SET[0] ^= setd
	CLR[0] ^= int(WR)
	SET[0] ^= int(WR)
	CLR[0] ^= int(dmask)

@micropython.viper
def clear_Screen1():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	Set_Addr_Window(0,0,scr_wdth,scr_hght)
	for i in range(scr_hght):
		for m in range(scr_wdth):
			data = int(0xFF) & 0xFF
			SET = ptr32(0x3FF44008) #Set Register
			CLR = ptr32(0x3FF4400C) #Clear Register

			SET[0] ^= int(CDRS)

			setd = 0x0000
			setd ^= ((data & 0x01) >> 0 )<< DO
			setd ^= ((data & 0x02) >> 1 )<< D1
			setd ^= ((data & 0x04) >> 2 )<< D2
			setd ^= ((data & 0x08) >> 3 )<< D3
			setd ^= ((data & 0x10) >> 4 )<< D4
			setd ^= ((data & 0x20) >> 5 )<< D5
			setd ^= ((data & 0x40) >> 6 )<< D6
			setd ^= ((data & 0x80) >> 7 )<< D7
			setd &= dmask1
			SET[0] ^= setd
			CLR[0] ^= int(WR)
			SET[0] ^= int(WR)
			CLR[0] ^= int(dmask)

			data = int(0x00) & 0xFF
			SET = ptr32(0x3FF44008) #Set Register
			CLR = ptr32(0x3FF4400C) #Clear Register

			SET[0] ^= int(CDRS)

			setd = 0x0000
			setd ^= ((data & 0x01) >> 0 )<< DO
			setd ^= ((data & 0x02) >> 1 )<< D1
			setd ^= ((data & 0x04) >> 2 )<< D2
			setd ^= ((data & 0x08) >> 3 )<< D3
			setd ^= ((data & 0x10) >> 4 )<< D4
			setd ^= ((data & 0x20) >> 5 )<< D5
			setd ^= ((data & 0x40) >> 6 )<< D6
			setd ^= ((data & 0x80) >> 7 )<< D7
			setd &= dmask1
			SET[0] ^= setd
			CLR[0] ^= int(WR)
			SET[0] ^= int(WR)
			CLR[0] ^= int(dmask)

	SET[0] ^= int(CS)

@micropython.viper
def clear_Screen2():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	Set_Addr_Window(0,0,scr_wdth,scr_hght)
	for i in range(320):
		for m in range(scr_wdth):
			data = int(0xFF) & 0xFF

			SET[0] ^= CDRS1
			setd = dmask1
			SET[0] ^= data << 8
			CLR[0] ^= WR1
			SET[0] ^= WR1
			CLR[0] ^= dmask1

			data = int(0x00) & 0xFF
			
			SET[0] ^= CDRS1
			setd = dmask1
			SET[0] ^= data << 8
			CLR[0] ^= WR1
			SET[0] ^= WR1
			CLR[0] ^= dmask1

	SET[0] ^= int(CS)

@micropython.viper
def clear_Screen3():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	Set_Addr_Window(0,0,scr_wdth,scr_hght)
	for i in range(160*480):
		data = int(0xFF) & 0xFF

		SET[0] ^= CDRS1
		setd = dmask1
		SET[0] ^= data << 8
		CLR[0] ^= WR1
		SET[0] ^= WR1
		CLR[0] ^= dmask1

		data = int(0x00) & 0xFF
		
		SET[0] ^= CDRS1
		setd = dmask1
		SET[0] ^= data << 8
		CLR[0] ^= WR1
		SET[0] ^= WR1
		CLR[0] ^= dmask1

		data = int(0xFF) & 0xFF

		SET[0] ^= CDRS1
		setd = dmask1
		SET[0] ^= data << 8
		CLR[0] ^= WR1
		SET[0] ^= WR1
		CLR[0] ^= dmask1

		data = int(0x00) & 0xFF
		
		SET[0] ^= CDRS1
		setd = dmask1
		SET[0] ^= data << 8
		CLR[0] ^= WR1
		SET[0] ^= WR1
		CLR[0] ^= dmask1


	SET[0] ^= int(CS)



@micropython.viper
def Reset():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	before_us = time.ticks_ms()
	clear_Screen1()
	after_us = time.ticks_ms()
	print('1 us from ' + str(before_us) + " to " + str(after_us))
	before_us = time.ticks_ms()
	clear_Screen2()
	after_us = time.ticks_ms()
	print('2 us from ' + str(before_us) + " to " + str(after_us))
	before_us = time.ticks_ms()
	clear_Screen3()
	after_us = time.ticks_ms()
	print('3 us from ' + str(before_us) + " to " + str(after_us))
print("pin test")


init()
Reset()