import ili9486py as display
import network
import ubinascii

#pinout
CS_pin = 21
RD_pin = 2
WR_pin = 0
RST_pin = 4
CDRS_pin = 5


print('main.py')


#init display

#TODO this is still fake init and hardcoded pins
display.init(RST_pin,CS_pin,CDRS_pin,WR_pin,RD_pin)


#get wlan networks
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface

nets = wlan.scan()
wlannetworks = []
for net in nets:
	wlannetworks.append(net[0].decode("utf-8")) 


#print some information
size1_longstring = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. But what happens if the displayed text is actually longer than expected? will there be an answer? Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quisque non tellus orci ac auctor. Ut consequat semper viverra nam libero justo. Risus in hendrerit gravida rutrum quisque non tellus orci. Est ultricies integer quis auctor elit sed vulputate mi. Gravida rutrum quisque non tellus orci ac. Habitasse platea dictumst quisque sagittis purus. Dictum varius duis at consectetur lorem donec. Adipiscing at in tellus integer feugiat scelerisque varius. Integer feugiat scelerisque varius morbi enim. Morbi tincidunt augue interdum velit euismod in. Auctor augue mauris augue neque gravida in. Ut lectus arcu bibendum at varius vel pharetra vel. Aliquam malesuada bibendum arcu vitae elementum curabitur vitae nunc. Vel orci porta non pulvinar neque laoreet suspendisse interdum. In fermentum et sollicitudin ac orci. Porttitor rhoncus dolor purus non enim praesent elementum facilisis. Commodo ullamcorper a lacus vestibulum. Pulvinar elementum integer enim neque volutpat. Amet risus nullam eget felis eget nunc lobortis. Adipiscing elit pellentesque habitant morbi tristique senectus et. Tristique magna sit amet purus. Malesuada nunc vel risus commodo viverra maecenas accumsan lacus vel. Metus dictum at tempor commodo ullamcorper a lacus vestibulum. Cras fermentum odio eu feugiat pretium nibh ipsum consequat. Velit aliquet sagittis id consectetur purus. Semper feugiat nibh sed pulvinar proin. Tortor consequat id porta nibh venenatis cras. Massa enim nec dui nunc mattis enim ut tellus. Velit ut tortor pretium viverra. Pellentesque elit eget gravida cum sociis natoque penatibus. Nam aliquam sem et tortor consequat id porta. Id diam vel quam elementum pulvinar etiam. Nisl purus in mollis nunc sed id semper risus in. In fermentum et sollicitudin ac orci phasellus. Now this time we are trying it againg: what happens if the displayed Text at size 1 is longer than expected? Will it still print?'

display.Draw_Info_Box_Text(x=20,y=20,w=250,h=200,heading="Weather data",body=size1_longstring)
display.Draw_Info_Box_List(x=290,y=20,w=170,h=200,heading="Networks",body=wlannetworks)
