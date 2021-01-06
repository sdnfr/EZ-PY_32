import drivers.ili9486py as display
import drivers.encoder as enc
import machine
import view as view
import model as model


def select(old,new):
	WHITE=const(0xFFFF)
	RED=const(0xF800)
	if old is not None:
		display.Draw_Rect(old[0]-2,old[1]-2,old[2]+4,old[3]+4,WHITE)
	display.Draw_Rect(new[0]-2,new[1]-2,new[2]+4,new[3]+4,RED)


network = {"name":"network", "displays":[], "selectors":view.getNetworkSelectors, "draw":view.drawNetwork, "args": [model.fetchNetwork()]}
server = {"name":"server", "displays":[], "selectors":view.getServerSelectors, "draw":view.drawServer, "args": [model.fetchServer()], "refresh":model.fetchNew}
text = {"name":"text","displays":[], "selectors":view.getTextSelectors,"draw":view.drawText, "args":[]}
logo = {"name":"logo","displays":[], "selectors":view.getLogoSelectors,"draw":view.drawLogo, "args":[]}
main = {"name":"main","displays":[text,network,logo,server], "selectors":view.getMainSelectors,"draw":view.drawMain, "args":[]}
network["displays"].append(network)
network["displays"].append(main)

server["displays"].append(server)
server["displays"].append(main)

text["displays"].append(text)
text["displays"].append(main)

logo["displays"].append(logo)
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
	global drawNewDisplay
	global selectedDisplay
	global selectNewDisplay
	global oldSelectedDisplay
	global selector
	global currentDisplay
	if drawNewDisplay:
		currentDisplay = currentDisplay["displays"][selector]
		display.fill_Screen(WHITE) #loading screen maybe
		if 'refresh' in currentDisplay.keys():
			print("refreshing")
			currentDisplay["args"][0] = currentDisplay["refresh"]()
		currentDisplay["draw"](currentDisplay["args"])
		selector = -1
		drawNewDisplay = False
		oldSelectedDisplay = None
		selectedDisplay = None
	if selectNewDisplay:
		oldSelectedDisplay = selectedDisplay
		selectedDisplay = currentDisplay["selectors"]()[selector]
		select(oldSelectedDisplay,selectedDisplay)
		selectNewDisplay = False
		if currentDisplay == main:
			enc.setEncoderMode(selector)

def init():
	view.drawMain([])