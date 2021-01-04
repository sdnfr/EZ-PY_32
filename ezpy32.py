import ili9486py as display
import network
import ubinascii
import password
import utime
import urequests as requests
import ujson
import machine
from machine import Pin

#flashing micropython: 
# esptool.py --chip esp32 --port COM4 erase_flash
# esptool.py --chip esp32 --port COM4 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin
#copying files via ampy:
# ampy --port COM4 put test.py

BLACK=const(0x0000)
WHITE=const(0xFFFF)
BLUE=const(0x001F)
RED=const(0xF800)
GREEN=const(0x07E0)
CYAN=const(0x07FF)
MAGENTA=const(0xF81F)
YELLOW=const(0xFFE0)


def drawMain():
	#print some information
	size1_longstring = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. But what happens if the displayed text is actually longer than expected? will there be an answer? Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quisque non tellus orci ac auctor. Ut consequat semper viverra nam libero justo. Risus in hendrerit gravida rutrum quisque non tellus orci. Est ultricies integer quis auctor elit sed vulputate mi. Gravida rutrum quisque non tellus orci ac. Habitasse platea dictumst quisque sagittis purus. Dictum varius duis at consectetur lorem donec. Adipiscing at in tellus integer feugiat scelerisque varius. Integer feugiat scelerisque varius morbi enim. Morbi tincidunt augue interdum velit euismod in. Auctor augue mauris augue neque gravida in. Ut lectus arcu bibendum at varius vel pharetra vel. Aliquam malesuada bibendum arcu vitae elementum curabitur vitae nunc. Vel orci porta non pulvinar neque laoreet suspendisse interdum. In fermentum et sollicitudin ac orci. Porttitor rhoncus dolor purus non enim praesent elementum facilisis. Commodo ullamcorper a lacus vestibulum. Pulvinar elementum integer enim neque volutpat. Amet risus nullam eget felis eget nunc lobortis. Adipiscing elit pellentesque habitant morbi tristique senectus et. Tristique magna sit amet purus. Malesuada nunc vel risus commodo viverra maecenas accumsan lacus vel. Metus dictum at tempor commodo ullamcorper a lacus vestibulum. Cras fermentum odio eu feugiat pretium nibh ipsum consequat. Velit aliquet sagittis id consectetur purus. Semper feugiat nibh sed pulvinar proin. Tortor consequat id porta nibh venenatis cras. Massa enim nec dui nunc mattis enim ut tellus. Velit ut tortor pretium viverra. Pellentesque elit eget gravida cum sociis natoque penatibus. Nam aliquam sem et tortor consequat id porta. Id diam vel quam elementum pulvinar etiam. Nisl purus in mollis nunc sed id semper risus in. In fermentum et sollicitudin ac orci phasellus. Now this time we are trying it againg: what happens if the displayed Text at size 1 is longer than expected? Will it still print?'
	global wlannetworks
	display.Draw_Info_Box_Text(x=20,y=20,w=250,h=200,heading="Weather data",body=size1_longstring)
	display.Draw_Info_Box_List(x=290,y=20,w=170,h=200,heading="Networks",body=wlannetworks)
	display.Draw_Info_Box_Text(x=20,y=240,w=250,h=60,heading="Logo",body="")


def drawWlan():
	global wlannetworks
	display.Draw_Info_Box_List(x=20,y=20,w=250,h=200,heading="Networks",body=wlannetworks)

def drawText():
	size1_longstring = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. But what happens if the displayed text is actually longer than expected? will there be an answer? Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quisque non tellus orci ac auctor. Ut consequat semper viverra nam libero justo. Risus in hendrerit gravida rutrum quisque non tellus orci. Est ultricies integer quis auctor elit sed vulputate mi. Gravida rutrum quisque non tellus orci ac. Habitasse platea dictumst quisque sagittis purus. Dictum varius duis at consectetur lorem donec. Adipiscing at in tellus integer feugiat scelerisque varius. Integer feugiat scelerisque varius morbi enim. Morbi tincidunt augue interdum velit euismod in. Auctor augue mauris augue neque gravida in. Ut lectus arcu bibendum at varius vel pharetra vel. Aliquam malesuada bibendum arcu vitae elementum curabitur vitae nunc. Vel orci porta non pulvinar neque laoreet suspendisse interdum. In fermentum et sollicitudin ac orci. Porttitor rhoncus dolor purus non enim praesent elementum facilisis. Commodo ullamcorper a lacus vestibulum. Pulvinar elementum integer enim neque volutpat. Amet risus nullam eget felis eget nunc lobortis. Adipiscing elit pellentesque habitant morbi tristique senectus et. Tristique magna sit amet purus. Malesuada nunc vel risus commodo viverra maecenas accumsan lacus vel. Metus dictum at tempor commodo ullamcorper a lacus vestibulum. Cras fermentum odio eu feugiat pretium nibh ipsum consequat. Velit aliquet sagittis id consectetur purus. Semper feugiat nibh sed pulvinar proin. Tortor consequat id porta nibh venenatis cras. Massa enim nec dui nunc mattis enim ut tellus. Velit ut tortor pretium viverra. Pellentesque elit eget gravida cum sociis natoque penatibus. Nam aliquam sem et tortor consequat id porta. Id diam vel quam elementum pulvinar etiam. Nisl purus in mollis nunc sed id semper risus in. In fermentum et sollicitudin ac orci phasellus. Now this time we are trying it againg: what happens if the displayed Text at size 1 is longer than expected? Will it still print?'
	display.Draw_Info_Box_Text(x=20,y=20,w=250,h=200,heading="Weather data",body=size1_longstring)

def drawLogo():
	display.printBild()



def select(old,new):
	if old is not None:
		display.Draw_Rect(old[0]-2,old[1]-2,old[2]+4,old[3]+4,WHITE)
	display.Draw_Rect(new[0]-2,new[1]-2,new[2]+4,new[3]+4,RED)




mainSelectors = [[20,20,250,200],[290,20,170,200],[20,240,250,60],[450,290,20,20]]
wlanSelectors = [[450,290,20,20]]
textSelectors = [[450,290,20,20]]
logoSelectors = [[450,290,20,20]]


wlan = {"name":"wlan", "displays":[], "selectors":wlanSelectors, "draw":drawWlan}
text = {"name":"text","displays":[], "selectors":textSelectors,"draw":drawText}
logo = {"name":"logo","displays":[], "selectors":logoSelectors,"draw":drawLogo}
main = {"name":"main","displays":[text,wlan,logo], "selectors":mainSelectors,"draw":drawMain}
wlan["displays"].append(main)
text["displays"].append(main)
logo["displays"].append(main)


selector = -1
currentDisplay = main
selectedDisplay = None
oldSelectedDisplay = None
drawNewDisplay = False
selectNewDisplay = False


def select_pressed(p):
	#TODO proper debounce
	print('select pressed ')
	utime.sleep_ms(300)
	global drawNewDisplay
	drawNewDisplay = True



@micropython.viper
def choose_pressed(p):
	GPIO_PIN26_REG = ptr32(0x3FF440F0) #GPIO_PIN26_REG Register
	GPIO_PIN26_REG[0] &= ~0xF<<13

	max = int(len(currentDisplay["displays"]))
	global selector
	selector_ = int(selector)
	global selectNewDisplay

	if selector_<max-1:
		selector_ +=1
	else:
		selector_=0


	selector = selector_
	selectNewDisplay = True
	print('now selected screen' + str(selector_))

	#TODO fix this ugly disabling
	#wait loop, enable irq did not work, utime also is broken since interrupt is turned off
	for i in range(1000):
		for b in range(10000):
				d = i +b
	p=machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
	p.irq(trigger=Pin.IRQ_FALLING, handler=choose_pressed)


@micropython.viper
def disableIRQ():
	#GPIO_PIN27_REG = ptr32(0x3FF440F4) #GPIO_PIN27_REG Register
	GPIO_PIN26_REG = ptr32(0x3FF440F0) #GPIO_PIN26_REG Register

	GPIO_PIN26_REG[0] &= ~0xF<<13

@micropython.viper
def enableIRQ():
	GPIO_PIN27_REG = ptr32(0x3FF440F4) #GPIO_PIN27_REG Register
	GPIO_PIN27_REG[0] ^= 0xF<<13


#pinout
CS_pin = 21
RD_pin = 2
WR_pin = 0
RST_pin = 4
CDRS_pin = 5


# def http_get(url):
#	 import socket
#	 _, _, host, path = url.split('/', 3)
#	 addr = socket.getaddrinfo(host, 3000)[0][-1]

#	 s = socket.socket()
#	 s.connect(addr)
#	 #print('reqesting: ' + ('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
#	 s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
#	 while True:
#		 data = s.recv(100)
#		 if data:
#			 print(str(data, 'utf8'), end='')
#		 else:
#			 break
#	 s.close()


# print('main.py')


# #init display

# #TODO this is still fake init and hardcoded pins
display.init(RST_pin,CS_pin,CDRS_pin,WR_pin,RD_pin)


# #get wlan networks
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)	   # activate the interface

nets = wlan.scan()
wlannetworks = []
for net in nets:
	wlannetworks.append(net[0].decode("utf-8")) 

# wlan.connect(password.essid, password.pw)

# utime.sleep_ms(5000)


# #print(http_get('http://192.168.2.102/data'))


# res = requests.get(url='http://192.168.2.102:3000/data')
# print(res.text)




down=machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
up=machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)

up.irq(trigger=Pin.IRQ_FALLING, handler=select_pressed)
down.irq(trigger=Pin.IRQ_FALLING, handler=choose_pressed)



drawMain()
while True:
	if drawNewDisplay:
		currentDisplay = currentDisplay["displays"][selector]
		display.clear_Screen()
		currentDisplay["draw"]()
		selector = -1
		drawNewDisplay = False
		oldSelectedDisplay = None
		selectedDisplay = None
	if selectNewDisplay:
		oldSelectedDisplay = selectedDisplay
		selectedDisplay = currentDisplay["selectors"][selector]
		select(oldSelectedDisplay,selectedDisplay)
		selectNewDisplay = False
	utime.sleep_ms(10)

