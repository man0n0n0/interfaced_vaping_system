#####
#auto vape system controller - 2025
#manoahcamporini.com special commision for lukelukeluke
#####
from machine import *
import time
import ssd1306
import framebuf

# using default address 0x3C
i2c = SoftI2C(sda=Pin(5), scl=Pin(3))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

vaping_time = 5
chilling_time = 30

def screen_init():
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.line(2, 2, 16, 28, 1)
    display.line(16, 28, 28, 2, 1)
    display.text('H1P3RV4P3R', 40, 0, 1)
    display.text(f"{vaping_time}-{chilling_time}", 40, 12, 1)
    display.text('lukelukeluke', 0, 40, 1)
    

def counter(t, msg):
    dotstr = ""
    for t in range(t):
        dotstr+="."
        
        #drawing waiting time
        fbuf = framebuf.FrameBuffer(bytearray(128 * 64 * 1), 128, 64, framebuf.MONO_VLSB)
        fbuf.text(msg, 40, 24, 1)
        if len(dotstr) > 15 :
            fbuf.text("...............", 0, 30, 1)
            fbuf.text(dotstr[15:], 0, 50, 1)
        else :
            fbuf.text(dotstr, 0, 30, 1)
        display.blit(fbuf, 0, 0, 0)   
        display.show()
        
        time.sleep(1)
        
    screen_init()
        
        
def vape_control():
    mosfet0 = Pin(39, Pin.OUT)
    
    mosfet0.value(1)
    dotstr = ""
    counter(vaping_time, "vaping")
    
    mosfet0.value(0)
    dotstr = ""
    counter(chilling_time, "chilling")


def web_interface():
    pass


screen_init()
while True:
    vape_control()
