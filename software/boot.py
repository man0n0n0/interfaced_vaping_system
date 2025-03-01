####
# BOOT FILE FOR ESP32S2Mini_wemos module
####

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# Use an interrupt function count the number of times a button has been pressed
from time import sleep
from machine import PWM, Pin

btn = Pin(0, Pin.IN, Pin.PULL_UP)

def blink():
    led = Pin(15, Pin.OUT)
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(0.1)

blink()
blink()
blink()

if btn.value() == 0:
    pass

else :
    import vape_lukelukeluke


