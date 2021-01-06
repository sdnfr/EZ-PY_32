import drivers.ili9486py as display
import machine
import mainview as mv

wlannetworks = ["a","b"]


def select(old,new):
	WHITE=const(0xFFFF)
	RED=const(0xF800)
	if old is not None:
		display.Draw_Rect(old[0]-2,old[1]-2,old[2]+4,old[3]+4,WHITE)
	display.Draw_Rect(new[0]-2,new[1]-2,new[2]+4,new[3]+4,RED)




mainSelectors = [[20,20,250,200],[290,20,170,200],[20,240,250,60],[450,290,20,20]]
wlanSelectors = [[450,290,20,20]]
textSelectors = [[450,290,20,20]]
logoSelectors = [[450,290,20,20]]


wlan = {"name":"wlan", "displays":[], "selectors":wlanSelectors, "draw":mv.drawWlan}
text = {"name":"text","displays":[], "selectors":textSelectors,"draw":mv.drawText}
logo = {"name":"logo","displays":[], "selectors":logoSelectors,"draw":mv.drawLogo}
main = {"name":"main","displays":[text,wlan,logo], "selectors":mainSelectors,"draw":mv.drawMain}
wlan["displays"].append(main)
text["displays"].append(main)
logo["displays"].append(main)


selector = -1
currentDisplay = main
selectedDisplay = None
oldSelectedDisplay = None
drawNewDisplay = False
selectNewDisplay = False


def onClick():
	global drawNewDisplay
	drawNewDisplay = True


def onLeft():
	max = int(len(currentDisplay["displays"]))
	global selector
	selector_ = int(selector)
	global selectNewDisplay

	if selector_>0:
		selector_ -= 1
	else:
		selector_=max-1


	selector = selector_
	selectNewDisplay = True
	print('now selected screen' + str(selector_))


def onRight():
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

def update():
	if drawNewDisplay:
		currentDisplay = currentDisplay["displays"][selector]
		display.fill_Screen(WHITE)
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
		if currentDisplay == main:
			encoder.setEncoderMode(selector)

def init():
	drawMain()