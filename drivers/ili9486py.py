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


lcd_font = [
	0x00, 0x00, 0x00, 0x00, 0x00,   
	0x3E, 0x5B, 0x4F, 0x5B, 0x3E, 	
	0x3E, 0x6B, 0x4F, 0x6B, 0x3E, 	
	0x1C, 0x3E, 0x7C, 0x3E, 0x1C, 
	0x18, 0x3C, 0x7E, 0x3C, 0x18, 
	0x1C, 0x57, 0x7D, 0x57, 0x1C, 
	0x1C, 0x5E, 0x7F, 0x5E, 0x1C, 
	0x00, 0x18, 0x3C, 0x18, 0x00, 
	0xFF, 0xE7, 0xC3, 0xE7, 0xFF, 
	0x00, 0x18, 0x24, 0x18, 0x00, 
	0xFF, 0xE7, 0xDB, 0xE7, 0xFF, 
	0x30, 0x48, 0x3A, 0x06, 0x0E, 
	0x26, 0x29, 0x79, 0x29, 0x26, 
	0x40, 0x7F, 0x05, 0x05, 0x07, 
	0x40, 0x7F, 0x05, 0x25, 0x3F, 
	0x5A, 0x3C, 0xE7, 0x3C, 0x5A, 
	0x7F, 0x3E, 0x1C, 0x1C, 0x08, 
	0x08, 0x1C, 0x1C, 0x3E, 0x7F, 
	0x14, 0x22, 0x7F, 0x22, 0x14, 
	0x5F, 0x5F, 0x00, 0x5F, 0x5F, 
	0x06, 0x09, 0x7F, 0x01, 0x7F, 
	0x00, 0x66, 0x89, 0x95, 0x6A, 
	0x60, 0x60, 0x60, 0x60, 0x60, 
	0x94, 0xA2, 0xFF, 0xA2, 0x94, 
	0x08, 0x04, 0x7E, 0x04, 0x08, 
	0x10, 0x20, 0x7E, 0x20, 0x10, 
	0x08, 0x08, 0x2A, 0x1C, 0x08, 
	0x08, 0x1C, 0x2A, 0x08, 0x08, 
	0x1E, 0x10, 0x10, 0x10, 0x10, 
	0x0C, 0x1E, 0x0C, 0x1E, 0x0C, 
	0x30, 0x38, 0x3E, 0x38, 0x30, 
	0x06, 0x0E, 0x3E, 0x0E, 0x06, 
	0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x5F, 0x00, 0x00, 
	0x00, 0x07, 0x00, 0x07, 0x00, 
	0x14, 0x7F, 0x14, 0x7F, 0x14, 
	0x24, 0x2A, 0x7F, 0x2A, 0x12, 
	0x23, 0x13, 0x08, 0x64, 0x62, 
	0x36, 0x49, 0x56, 0x20, 0x50, 
	0x00, 0x08, 0x07, 0x03, 0x00, 
	0x00, 0x1C, 0x22, 0x41, 0x00, 
	0x00, 0x41, 0x22, 0x1C, 0x00, 
	0x2A, 0x1C, 0x7F, 0x1C, 0x2A, 
	0x08, 0x08, 0x3E, 0x08, 0x08, 
	0x00, 0x80, 0x70, 0x30, 0x00, 
	0x08, 0x08, 0x08, 0x08, 0x08, 
	0x00, 0x00, 0x60, 0x60, 0x00, 
	0x20, 0x10, 0x08, 0x04, 0x02, 
	0x3E, 0x51, 0x49, 0x45, 0x3E, 
	0x00, 0x42, 0x7F, 0x40, 0x00, 
	0x72, 0x49, 0x49, 0x49, 0x46, 
	0x21, 0x41, 0x49, 0x4D, 0x33, 
	0x18, 0x14, 0x12, 0x7F, 0x10, 
	0x27, 0x45, 0x45, 0x45, 0x39, 
	0x3C, 0x4A, 0x49, 0x49, 0x31, 
	0x41, 0x21, 0x11, 0x09, 0x07, 
	0x36, 0x49, 0x49, 0x49, 0x36, 
	0x46, 0x49, 0x49, 0x29, 0x1E, 
	0x00, 0x00, 0x14, 0x00, 0x00, 
	0x00, 0x40, 0x34, 0x00, 0x00, 
	0x00, 0x08, 0x14, 0x22, 0x41, 
	0x14, 0x14, 0x14, 0x14, 0x14, 
	0x00, 0x41, 0x22, 0x14, 0x08, 
	0x02, 0x01, 0x59, 0x09, 0x06, 
	0x3E, 0x41, 0x5D, 0x59, 0x4E, 
	0x7C, 0x12, 0x11, 0x12, 0x7C, 
	0x7F, 0x49, 0x49, 0x49, 0x36, 
	0x3E, 0x41, 0x41, 0x41, 0x22, 
	0x7F, 0x41, 0x41, 0x41, 0x3E, 
	0x7F, 0x49, 0x49, 0x49, 0x41, 
	0x7F, 0x09, 0x09, 0x09, 0x01, 
	0x3E, 0x41, 0x41, 0x51, 0x73, 
	0x7F, 0x08, 0x08, 0x08, 0x7F, 
	0x00, 0x41, 0x7F, 0x41, 0x00, 
	0x20, 0x40, 0x41, 0x3F, 0x01, 
	0x7F, 0x08, 0x14, 0x22, 0x41, 
	0x7F, 0x40, 0x40, 0x40, 0x40, 
	0x7F, 0x02, 0x1C, 0x02, 0x7F, 
	0x7F, 0x04, 0x08, 0x10, 0x7F, 
	0x3E, 0x41, 0x41, 0x41, 0x3E, 
	0x7F, 0x09, 0x09, 0x09, 0x06, 
	0x3E, 0x41, 0x51, 0x21, 0x5E, 
	0x7F, 0x09, 0x19, 0x29, 0x46, 
	0x26, 0x49, 0x49, 0x49, 0x32, 
	0x03, 0x01, 0x7F, 0x01, 0x03, 
	0x3F, 0x40, 0x40, 0x40, 0x3F, 
	0x1F, 0x20, 0x40, 0x20, 0x1F, 
	0x3F, 0x40, 0x38, 0x40, 0x3F, 
	0x63, 0x14, 0x08, 0x14, 0x63, 
	0x03, 0x04, 0x78, 0x04, 0x03, 
	0x61, 0x59, 0x49, 0x4D, 0x43, 
	0x00, 0x7F, 0x41, 0x41, 0x41, 
	0x02, 0x04, 0x08, 0x10, 0x20, 
	0x00, 0x41, 0x41, 0x41, 0x7F, 
	0x04, 0x02, 0x01, 0x02, 0x04, 
	0x40, 0x40, 0x40, 0x40, 0x40, 
	0x00, 0x03, 0x07, 0x08, 0x00, 
	0x20, 0x54, 0x54, 0x78, 0x40, 
	0x7F, 0x28, 0x44, 0x44, 0x38, 
	0x38, 0x44, 0x44, 0x44, 0x28, 
	0x38, 0x44, 0x44, 0x28, 0x7F, 
	0x38, 0x54, 0x54, 0x54, 0x18, 
	0x00, 0x08, 0x7E, 0x09, 0x02, 
	0x18, 0xA4, 0xA4, 0x9C, 0x78, 
	0x7F, 0x08, 0x04, 0x04, 0x78, 
	0x00, 0x44, 0x7D, 0x40, 0x00, 
	0x20, 0x40, 0x40, 0x3D, 0x00, 
	0x7F, 0x10, 0x28, 0x44, 0x00, 
	0x00, 0x41, 0x7F, 0x40, 0x00, 
	0x7C, 0x04, 0x78, 0x04, 0x78, 
	0x7C, 0x08, 0x04, 0x04, 0x78, 
	0x38, 0x44, 0x44, 0x44, 0x38, 
	0xFC, 0x18, 0x24, 0x24, 0x18, 
	0x18, 0x24, 0x24, 0x18, 0xFC, 
	0x7C, 0x08, 0x04, 0x04, 0x08, 
	0x48, 0x54, 0x54, 0x54, 0x24, 
	0x04, 0x04, 0x3F, 0x44, 0x24, 
	0x3C, 0x40, 0x40, 0x20, 0x7C, 
	0x1C, 0x20, 0x40, 0x20, 0x1C, 
	0x3C, 0x40, 0x30, 0x40, 0x3C, 
	0x44, 0x28, 0x10, 0x28, 0x44, 
	0x4C, 0x90, 0x90, 0x90, 0x7C, 
	0x44, 0x64, 0x54, 0x4C, 0x44, 
	0x00, 0x08, 0x36, 0x41, 0x00, 
	0x00, 0x00, 0x77, 0x00, 0x00, 
	0x00, 0x41, 0x36, 0x08, 0x00, 
	0x02, 0x01, 0x02, 0x04, 0x02, 
	0x3C, 0x26, 0x23, 0x26, 0x3C, 
	0x1E, 0xA1, 0xA1, 0x61, 0x12, 
	0x3A, 0x40, 0x40, 0x20, 0x7A, 
	0x38, 0x54, 0x54, 0x55, 0x59, 
	0x21, 0x55, 0x55, 0x79, 0x41, 
	0x21, 0x54, 0x54, 0x78, 0x41, 
	0x21, 0x55, 0x54, 0x78, 0x40, 
	0x20, 0x54, 0x55, 0x79, 0x40, 
	0x0C, 0x1E, 0x52, 0x72, 0x12, 
	0x39, 0x55, 0x55, 0x55, 0x59, 
	0x39, 0x54, 0x54, 0x54, 0x59, 
	0x39, 0x55, 0x54, 0x54, 0x58, 
	0x00, 0x00, 0x45, 0x7C, 0x41, 
	0x00, 0x02, 0x45, 0x7D, 0x42, 
	0x00, 0x01, 0x45, 0x7C, 0x40, 
	0xF0, 0x29, 0x24, 0x29, 0xF0, 
	0xF0, 0x28, 0x25, 0x28, 0xF0, 
	0x7C, 0x54, 0x55, 0x45, 0x00, 
	0x20, 0x54, 0x54, 0x7C, 0x54, 
	0x7C, 0x0A, 0x09, 0x7F, 0x49, 
	0x32, 0x49, 0x49, 0x49, 0x32, 
	0x32, 0x48, 0x48, 0x48, 0x32, 
	0x32, 0x4A, 0x48, 0x48, 0x30, 
	0x3A, 0x41, 0x41, 0x21, 0x7A, 
	0x3A, 0x42, 0x40, 0x20, 0x78, 
	0x00, 0x9D, 0xA0, 0xA0, 0x7D, 
	0x39, 0x44, 0x44, 0x44, 0x39, 
	0x3D, 0x40, 0x40, 0x40, 0x3D, 
	0x3C, 0x24, 0xFF, 0x24, 0x24, 
	0x48, 0x7E, 0x49, 0x43, 0x66, 
	0x2B, 0x2F, 0xFC, 0x2F, 0x2B, 
	0xFF, 0x09, 0x29, 0xF6, 0x20, 
	0xC0, 0x88, 0x7E, 0x09, 0x03, 
	0x20, 0x54, 0x54, 0x79, 0x41, 
	0x00, 0x00, 0x44, 0x7D, 0x41, 
	0x30, 0x48, 0x48, 0x4A, 0x32, 
	0x38, 0x40, 0x40, 0x22, 0x7A, 
	0x00, 0x7A, 0x0A, 0x0A, 0x72, 
	0x7D, 0x0D, 0x19, 0x31, 0x7D, 
	0x26, 0x29, 0x29, 0x2F, 0x28, 
	0x26, 0x29, 0x29, 0x29, 0x26, 
	0x30, 0x48, 0x4D, 0x40, 0x20, 
	0x38, 0x08, 0x08, 0x08, 0x08, 
	0x08, 0x08, 0x08, 0x08, 0x38, 
	0x2F, 0x10, 0xC8, 0xAC, 0xBA, 
	0x2F, 0x10, 0x28, 0x34, 0xFA, 
	0x00, 0x00, 0x7B, 0x00, 0x00, 
	0x08, 0x14, 0x2A, 0x14, 0x22, 
	0x22, 0x14, 0x2A, 0x14, 0x08, 
	0xAA, 0x00, 0x55, 0x00, 0xAA, 
	0xAA, 0x55, 0xAA, 0x55, 0xAA, 
	0x00, 0x00, 0x00, 0xFF, 0x00, 
	0x10, 0x10, 0x10, 0xFF, 0x00, 
	0x14, 0x14, 0x14, 0xFF, 0x00, 
	0x10, 0x10, 0xFF, 0x00, 0xFF, 
	0x10, 0x10, 0xF0, 0x10, 0xF0, 
	0x14, 0x14, 0x14, 0xFC, 0x00, 
	0x14, 0x14, 0xF7, 0x00, 0xFF, 
	0x00, 0x00, 0xFF, 0x00, 0xFF, 
	0x14, 0x14, 0xF4, 0x04, 0xFC, 
	0x14, 0x14, 0x17, 0x10, 0x1F, 
	0x10, 0x10, 0x1F, 0x10, 0x1F, 
	0x14, 0x14, 0x14, 0x1F, 0x00, 
	0x10, 0x10, 0x10, 0xF0, 0x00, 
	0x00, 0x00, 0x00, 0x1F, 0x10, 
	0x10, 0x10, 0x10, 0x1F, 0x10, 
	0x10, 0x10, 0x10, 0xF0, 0x10, 
	0x00, 0x00, 0x00, 0xFF, 0x10, 
	0x10, 0x10, 0x10, 0x10, 0x10, 
	0x10, 0x10, 0x10, 0xFF, 0x10, 
	0x00, 0x00, 0x00, 0xFF, 0x14, 
	0x00, 0x00, 0xFF, 0x00, 0xFF, 
	0x00, 0x00, 0x1F, 0x10, 0x17, 
	0x00, 0x00, 0xFC, 0x04, 0xF4, 
	0x14, 0x14, 0x17, 0x10, 0x17, 
	0x14, 0x14, 0xF4, 0x04, 0xF4, 
	0x00, 0x00, 0xFF, 0x00, 0xF7, 
	0x14, 0x14, 0x14, 0x14, 0x14, 
	0x14, 0x14, 0xF7, 0x00, 0xF7, 
	0x14, 0x14, 0x14, 0x17, 0x14, 
	0x10, 0x10, 0x1F, 0x10, 0x1F, 
	0x14, 0x14, 0x14, 0xF4, 0x14, 
	0x10, 0x10, 0xF0, 0x10, 0xF0, 
	0x00, 0x00, 0x1F, 0x10, 0x1F, 
	0x00, 0x00, 0x00, 0x1F, 0x14, 
	0x00, 0x00, 0x00, 0xFC, 0x14, 
	0x00, 0x00, 0xF0, 0x10, 0xF0, 
	0x10, 0x10, 0xFF, 0x10, 0xFF, 
	0x14, 0x14, 0x14, 0xFF, 0x14, 
	0x10, 0x10, 0x10, 0x1F, 0x00, 
	0x00, 0x00, 0x00, 0xF0, 0x10, 
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
	0xF0, 0xF0, 0xF0, 0xF0, 0xF0, 
	0xFF, 0xFF, 0xFF, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0xFF, 0xFF, 
	0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 
	0x38, 0x44, 0x44, 0x38, 0x44, 
	0x7C, 0x2A, 0x2A, 0x3E, 0x14, 
	0x7E, 0x02, 0x02, 0x06, 0x06, 
	0x02, 0x7E, 0x02, 0x7E, 0x02, 
	0x63, 0x55, 0x49, 0x41, 0x63, 
	0x38, 0x44, 0x44, 0x3C, 0x04, 
	0x40, 0x7E, 0x20, 0x1E, 0x20, 
	0x06, 0x02, 0x7E, 0x02, 0x02, 
	0x99, 0xA5, 0xE7, 0xA5, 0x99, 
	0x1C, 0x2A, 0x49, 0x2A, 0x1C, 
	0x4C, 0x72, 0x01, 0x72, 0x4C, 
	0x30, 0x4A, 0x4D, 0x4D, 0x30, 
	0x30, 0x48, 0x78, 0x48, 0x30, 
	0xBC, 0x62, 0x5A, 0x46, 0x3D, 
	0x3E, 0x49, 0x49, 0x49, 0x00, 
	0x7E, 0x01, 0x01, 0x01, 0x7E, 
	0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 
	0x44, 0x44, 0x5F, 0x44, 0x44, 
	0x40, 0x51, 0x4A, 0x44, 0x40, 
	0x40, 0x44, 0x4A, 0x51, 0x40, 
	0x00, 0x00, 0xFF, 0x01, 0x03, 
	0xE0, 0x80, 0xFF, 0x00, 0x00, 
	0x08, 0x08, 0x6B, 0x6B, 0x08,
	0x36, 0x12, 0x36, 0x24, 0x36, 
	0x06, 0x0F, 0x09, 0x0F, 0x06, 
	0x00, 0x00, 0x18, 0x18, 0x00, 
	0x00, 0x00, 0x10, 0x10, 0x00, 
	0x30, 0x40, 0xFF, 0x01, 0x01, 
	0x00, 0x1F, 0x01, 0x01, 0x1E, 
	0x00, 0x19, 0x1D, 0x17, 0x12, 
	0x00, 0x3C, 0x3C, 0x3C, 0x3C, 
	0x00, 0x00, 0x00, 0x00, 0x00, 
]


@micropython.viper
def Draw_Pixe(x, y, c_):
	c = int(c_)
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	Set_Addr_Window(x, y, x, y)
	c1 = int(c>>8) &0xFF
	c2 = int(c) &0xFF

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
def Fill_Square(x_, y_, size, c_):
	#TODO catch error if y and x is taller than max
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	x = int(x_)
	y = int(y_)
	c = int(c_)
	s = int(size)
	Set_Addr_Window(x, y, x + s - 1, y + s - 1)#set area
	c1 = int(c>>8) &0xFF
	c2 = int(c) &0xFF

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
	for i in range(s*s):
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
def Fill_Rect(x_, y_, w_, h_, c_):
	#TODO catch error if y and x is taller than max
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register


	x = int(x_)
	y = int(y_)
	c = int(c_)
	w = int(w_)
	h = int(h_)

	Set_Addr_Window(x, y, x + w - 1, y + h - 1)#set area
	c1 = int(c>>8) &0xFF
	c2 = int(c) &0xFF

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
	for i in range(w*h):
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
def H_line(x_, y_, l_, c_):
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	x = int(x_)
	y = int(y_)
	c = int(c_)
	l = int(l_)
	Set_Addr_Window(x,y,l+x,y)
	c1 = int(c>>8) &0xFF
	c2 = int(c) &0xFF

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
	for i in range(l):
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
def V_line(x_, y_, l_, c_):
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	x = int(x_)
	y = int(y_)
	c = int(c_)
	l = int(l_)
	Set_Addr_Window(x,y,x,y+l)
	c1 = int(c>>8) &0xFF
	c2 = int(c) &0xFF

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
	for i in range(l):
		SET[0] ^= c1_d
		CLR[0] ^= int(WR)
		SET[0] ^= int(WR)
		CLR[0] ^= int(dmask)

		SET[0] ^= c2_d
		CLR[0] ^= int(WR)
		SET[0] ^= int(WR)
		CLR[0] ^= int(dmask)
	SET[0] ^= int(CS)

def Draw_Rect(x,y,w,h,c):
	H_line(x,y,w,c)
	H_line(x,y+h,w,c)
	V_line(x,y,h,c)
	V_line(x+w,y,h,c)


def Draw_Char(x_, y_, ch_, co_,si_):
	si = int(si_)
	ch = int(ch_)
	x = int(x_)
	y = int(y_)
	co = int(co_)
	for i in range(ch_wdth):
		line = 0
		if (int(i) == ch_wdth-1):
			line = 0x0
		else:
			line = int(lcd_font[(ch*5)+i])
		for j in range(ch_hght):
			if (int(line) & 0x1):
				if (si == 1):
					Draw_Pixe(x+i, y+j, co)
				else:
					Fill_Square(x+(i*si), y+(j*si), si, co)
			line >>= 1

def Draw_Dots(x_, y_,co_,si_):
	si = int(si_)
	x = int(x_)
	y = int(y_)
	co = int(co_)
	h = ch_hght-2
	if (si == 1):
		Draw_Pixe(x, y+h,co)
		Draw_Pixe(x+2*si, y+h,co)
		Draw_Pixe(x+4*si, y+h,co)
	else:
		Fill_Square(x, y+h*si, si, co)
		Fill_Square(x+2*si, y+h*si, si, co)
		Fill_Square(x+4*si, y+h*si, si, co)



def Draw_Info_Box_Text(x,y,w,h,heading="Heading",body="body",list = [],size=1,margin = 0,padding = 10,color = BLACK):
	Draw_Rect(x,y,w,h,BLACK)
	Draw_Text(x+padding,y+padding,heading,MAGENTA,size*2,x_limit=x+w-2*padding,y_limit=y+2*size*ch_hght)
	Draw_Text(x+padding,y+padding+2*size*ch_hght,body,color,size,x_limit=x+ w-padding,y_limit=y+h-padding-2*size*ch_hght)

def Draw_Info_Box_List(x,y,w,h,heading="Heading",body="body",list = [],size=1,margin = 0,padding = 10,color = BLACK):
	Draw_Rect(x,y,w,h,BLACK)
	Draw_Text(x+padding,y+padding,heading,MAGENTA,size*2,x_limit=x+w-2*padding,y_limit=y+2*size*ch_hght)
	Draw_List(x+padding,y+padding+2*size*ch_hght,body,color,size,x_limit=x+ w-padding,y_limit=y+h-padding-2*size*ch_hght)




def Draw_List(x_, y_, list, co_, si_, x_limit=scr_wdth,y_limit = scr_hght):
	si = int(si_)
	x = int(x_)
	y = int(y_)
	co = int(co_)
	ylim = int(y_limit) - si*ch_hght
	i = 0
	for item in list:
		st = str(item)
		ys = y + i*si*ch_hght
		if ys < ylim:
			Draw_Text(x,ys,st,co,si,x_limit,si*ch_hght)
		i += 1 




def Draw_Text(x_, y_, st_, co_, si_, x_limit=scr_wdth,y_limit = scr_hght):
	si = int(si_)
	st = str(st_)
	x = int(x_)
	y = int(y_)
	co = int(co_)
	xi = 0 #x counter
	yi = 0 #y line counter
	xlim = int(x_limit) - si * 6 - si*ch_wdth 
	max_digits = 8
	tablim = xlim - max_digits*si*ch_wdth
	ylim = int(y_limit)- si*ch_hght
	dots = True
	justify = True #this doesnt use linebreaks at end of line
	for ch in st:
		x_s = x+xi*si*ch_wdth
		y_s = y+yi*si*ch_hght
		if x_s < xlim:
			if justify: 
				Draw_Char(x_s, y_s, ord(ch), co, si)
			else: #break line at first space character in the last max_digits digits of a line
				if x_s < tablim or ord(ch) != 0x20:
					Draw_Char(x_s, y_s, ord(ch), co, si)
				else: 			
					if y_s < ylim:
						xi = -1
						yi += 1
		else:
			if y_s < ylim:
				xi = 0
				yi += 1
				x_s = x+xi*si*ch_wdth
				y_s = y+yi*si*ch_hght
				Draw_Char(x_s, y_s, ord(ch), co, si)
			else:
				if dots:
					Draw_Dots(x_s,y_s,co,si)
					dots = False
		xi +=1

#helper level 



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

#low level

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



@micropython.viper
def printBild():
	SET = ptr32(0x3FF44008) #Set Register
	CLR = ptr32(0x3FF4400C) #Clear Register

	# Opening JSON file 
	f = open('data.json','r')
	
	# returns JSON object as  
	# a dictionary 
	data = json.load(f) 
	
	Set_Addr_Window(0,0,scr_wdth,scr_hght)
	# Iterating through the json 
	# list 
	i_ = 0
	for r in range(40):
		for c in range(60):
			col = int(data[i_])
			Fill_Square(c*8,r*8,8,col)
			i_ += 1

	SET[0] ^= int(CS)
	
	# Closing file 
	f.close() 



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
	fill_Screen(WHITE)
