import ili9486py as display
import machine
import views.mainview as mv


BLACK=const(0x0000)
WHITE=const(0xFFFF)
BLUE=const(0x001F)
RED=const(0xF800)
GREEN=const(0x07E0)
CYAN=const(0x07FF)
MAGENTA=const(0xF81F)
YELLOW=const(0xFFE0)
wlannetworks = ["a","b"]


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
text = {"name":"text","displays":[], "selectors":textSelectors,"draw":mv.drawText}
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