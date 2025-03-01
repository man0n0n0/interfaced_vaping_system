#####
#auto vape system controller - 2025
#manoahcamporini.com special commision for lukelukeluke
#####
from machine import *
import random
import network
import asyncio
import ssd1306
import framebuf
from microdot import Microdot, redirect, send_file

# default settings
vaping_time = 5
chilling_time = 30
vaping_time_random = (2,5)
chilling_time_random = (60,90)

mode = 'random_selection'

#to manage task re
vape_reboot = False

# using default address 0x3C
i2c = SoftI2C(sda=Pin(5), scl=Pin(3))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up acces point values
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='v4p3r', password='123456789')
while ap.active() == False:
  pass

def screen_init():
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.line(2, 2, 16, 28, 1)
    display.line(16, 28, 28, 2, 1)
    display.text('H1P3RV4P3R', 40, 0, 1)
    display.text(f"{vaping_time}-{chilling_time} : {mode}", 40, 12, 1)
    display.text(f'{ap.ifconfig()[0]}:5000', 0, 40, 1)
    
async def screen_counter(t, msg):
    global vape_reboot
    dotstr = ""
    
    for t in range(t):
        if not vape_reboot :
            dotstr+="."
            #drawing waiting time
            fbuf = framebuf.FrameBuffer(bytearray(128 * 64 * 1), 128, 64, framebuf.MONO_VLSB)
            fbuf.text(msg, 40, 24, 1)
            if len(dotstr) <= 15 :
                fbuf.text(dotstr, 0, 30, 1) 
            elif len(dotstr) > 15 :
                fbuf.text("...............", 0, 30, 1)
                fbuf.text(dotstr[15:], 0, 50, 1)            
            elif len(dotstr) > 30 :
                dotstr = ''
                screen_init()            
            display.blit(fbuf, 0, 0, 0)   
            display.show()       
            await asyncio.sleep(1)
            
        elif vape_reboot :
            vape_reboot = False
            break
        
    screen_init()
        
async def vape_control():
    global vaping_time, chilling_time, mode
    while True:
        mosfet0 = Pin(39, Pin.OUT)
        
        if mode == 'fixed':
            pass
        elif mode == 'random_fluctuation':
            vaping_time = random.randint(vaping_time-2,vaping_time+2)
            chilling_time = random.randint(chilling_time-20,vaping_time+20)
        elif mode == 'random_selection':
            vaping_time = random.randint(vaping_time_random[0],vaping_time_random[1])
            chilling_time = random.randint(chilling_time_random[0],chilling_time_random[1])
            screen_init() #to update time variable values
            
        #vaping state
        mosfet0.value(1)
        asyncio.run(screen_counter(vaping_time, "vaping"))
            
        #chilling state
        mosfet0.value(0)           
        asyncio.run(screen_counter(chilling_time, "chilling"))

app = Microdot()

@app.route('/', methods=['GET', 'POST'])
async def index(request):
    global vaping_time, chilling_time, mode, vape_reboot
    form_cookie = None
    message_cookie = None
    
    if request.method == 'POST':
        form_cookie = '{vaping_time},{chilling_time}'.format(vaping_time=request.form['vaping_time'],chilling_time=request.form['chilling_time'])
        print(form_cookie)
      
        if 'set' in request.form:
            pull = None
            #attribute the returning value from the forms to variable
            mode = request.form['mode']        
            vaping_time = int(request.form['vaping_time'])
            chilling_time = int(request.form['chilling_time'])
            
            vape_reboot = True
            
            message_cookie = "current mode is {mode} <br> timing is {vaping_time} - {chilling_time} ".format(mode=request.form['mode'], vaping_time = vaping_time  if not mode == 'random_selection' else 'random', chilling_time=chilling_time if not mode == 'random_selection' else '' )   
        
        response = redirect('/')
        
    else:
        if 'message' not in request.cookies:
            message_cookie = 'machine is load with default preset'
        response = send_file('V4P3R.html')
        
    if form_cookie:
        response.set_cookie('form', form_cookie)
        
    if message_cookie:
        response.set_cookie('message', message_cookie)
        
    return response

screen_init()

# Define the main function to run the event loop
async def main():
    global vape_task
    vape_task = asyncio.create_task(vape_control())
    app.run(debug=True)

# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
loop.run_forever()  # Run the event loop indefinitely