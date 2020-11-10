from machine import Pin

p0 = Pin(2, Pin.OUT)    # create output pin on GPIO0
p0.on()                 # set pin to "on" (high) level