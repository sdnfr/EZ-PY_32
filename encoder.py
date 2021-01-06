from machine import Pin
from machine import Timer
import machine
import time

#define Pins
POTTI_S = const(25)
POTTI_L = const(35)
POTTI_R = const(34)
ENC_RED = const(33)
ENC_GREEN = const(26)
ENC_BLUE = const(27)

redLED = None
greenLED = None
blueLED = None
r_int = 0
g_int = 0
b_int = 0
PWMEncoder = False
onClick_cb = None
onLeftScroll_cb = None
onRightScroll_cb = None
leftFirst = 0
rightFirst = 0
ticks = 4


@micropython.viper
def left_scrolled(p):
	regL = 0x3FF44088 + 0x4* int(POTTI_L)
	regR = 0x3FF44088 + 0x4* int(POTTI_R)


	GPIO_L = ptr32(regL) 
	GPIO_R = ptr32(regR) 

	en_L = GPIO_L[0]
	en_R = GPIO_R[0]

	GPIO_L[0] &= ~(0xF<<13)
	GPIO_L[0] &= ~(0x2<<7)
	GPIO_R[0] &= ~(0xF<<13)
	GPIO_R[0] &= ~(0x2<<7)

	for i in range(1000):
		for b in range(1500):
			d = i +b

	global onLeftScroll_cb
	onLeftScroll_cb()

	GPIO_L[0] ^= en_L
	GPIO_R[0] ^= en_R

@micropython.viper
def right_scrolled(p):

	regL = 0x3FF44088 + 0x4* int(POTTI_L)
	regR = 0x3FF44088 + 0x4* int(POTTI_R)

	GPIO_L = ptr32(regL) 
	GPIO_R = ptr32(regR) 

	en_L = GPIO_L[0]
	en_R = GPIO_R[0]

	GPIO_L[0] &= ~(0xF<<13)
	GPIO_L[0] &= ~(0x2<<7)
	GPIO_R[0] &= ~(0xF<<13)
	GPIO_R[0] &= ~(0x2<<7)

	for i in range(1000):
		for b in range(1500):
			d = i +b

	global onRightScroll_cb
	onRightScroll_cb()	
	
	GPIO_L[0] ^= en_L
	GPIO_R[0] ^= en_R


@micropython.viper
def clicked(p):
	print("clicked")
	reg = 0x3FF44088 + 0x4* int(POTTI_S)
	print(hex(reg))

	GPIO_PINn_REG = ptr32(reg) #GPIO_PINn_REG Register

	enable = GPIO_PINn_REG[0]
	GPIO_PINn_REG[0] &= ~(0xF<<13)
	GPIO_PINn_REG[0] &= ~(0x1<<7)

	for i in range(1000):
		for b in range(1500):
				d = i +b
	global onClick_cb
	onClick_cb()
	GPIO_PINn_REG[0] ^= enable



def setEncoderColorBin(data):
	data &= 0x7
	global redLED
	global greenLED
	global blueLED

	d = bin(data)[2:]
	while len(d)<3:
		d = "0" +d
	if d[0] == '1':
		redLED.on()
	else:
		redLED.off()

	if d[1] == '1':
		greenLED.on()
	else:
		greenLED.off()

	if d[2] == '1':
		blueLED.on()
	else:
		blueLED.off()

def setEncoderColor(r,g,b):
	global r_int
	global g_int
	global b_int
	global ticks
	global redLED
	global greenLED
	global blueLED
	redLED.off()
	greenLED.off()
	blueLED.off()

	ticks = 4

	r_int=r
	g_int=g
	b_int=b


def setEncoderMode(mode):
	global PWMEncoder
	if PWMEncoder:
		if mode == 0:
			setEncoderColor(4,2,0)
		elif mode == 1:
			setEncoderColor(0, 2, 4)
		elif mode == 2:
			setEncoderColor(1, 0, 4)
		else:
			setEncoderColor(0,0,0)
	else:
		if mode == 0:
			setEncoderColorBin(0b110)
		elif mode == 1:
			setEncoderColorBin(0b101)
		elif mode == 2:
			setEncoderColorBin(0b011)
		else:
			setEncoderColorBin(0b000)


def tick_cb(timer):
	global ticks
	
	global redLED
	global greenLED
	global blueLED
	global r_int
	global g_int
	global b_int

	if (ticks == r_int):
		redLED.value(1-redLED.value())

	if (ticks == g_int):
		greenLED.value(1-greenLED.value())

	if (ticks == b_int):
		blueLED.value(1-blueLED.value())

	
	if ticks == 0:
		ticks = 4
	ticks -=1

def init(onClick,onLeft,onRight):
	global onClick_cb
	onClick_cb = onClick
	global onLeftScroll_cb
	onLeftScroll_cb = onLeft
	global onRightScroll_cb
	onRightScroll_cb = onRight

	click=machine.Pin(POTTI_S, machine.Pin.IN)
	left = machine.Pin(POTTI_L, machine.Pin.IN)
	right = machine.Pin(POTTI_R, machine.Pin.IN)

	click.irq(trigger=Pin.IRQ_RISING, handler=clicked)

	left.irq(trigger=Pin.IRQ_FALLING, handler=left_scrolled)
	right.irq(trigger=Pin.IRQ_FALLING, handler=right_scrolled)

	global redLED
	global greenLED
	global blueLED

	redLED = machine.Pin(ENC_RED, machine.Pin.OUT)
	greenLED = machine.Pin(ENC_GREEN, machine.Pin.OUT)
	blueLED = machine.Pin(ENC_BLUE, machine.Pin.OUT)

	redLED.on()
	greenLED.on()
	blueLED.on()

	global PWMEncoder
	if PWMEncoder:
		timer = machine.Timer(0)
		timer.init(period=1, mode=machine.Timer.PERIODIC, callback=tick_cb) #1ms
