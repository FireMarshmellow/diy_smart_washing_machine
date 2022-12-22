import machine
from machine import I2C, Pin
import ssd1306
from time import sleep

Motor = Pin(3, Pin.OUT)

i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(14))

pin = machine.Pin(16, machine.Pin.OUT)
pin.value(0) #set GPIO16 low to reset OLED
pin.value(1) #while OLED is running, must set GPIO16 in high

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# define the menu options
menu_options = ["20ML", "25ML", "30ML","Purge",]

# initialize the menu state
menu_index = 0

# initialize the button pins
left_button = Pin(18, Pin.IN, Pin.PULL_DOWN)
right_button = Pin(16, Pin.IN, Pin.PULL_DOWN)
select_button = Pin(17, Pin.IN, Pin.PULL_DOWN)

def go_motor(x):
    for i in range(x,0, -1):
        minutes, seconds = divmod(i, 60)
        oled.fill(0)
        oled.text(menu_options[menu_index], 0, 0)
        oled.text('Dispensing...', 0, 10)
        oled.text(f"{minutes}m {seconds}s", 0, 20)
        oled.show()
        Motor.on()
        sleep(1)
        Motor.off()

def purge():
    while right_button.value()== 0:
        print('purgeing...')
        oled.fill(0)
        oled.text('purgeing...', 0, 10)
        oled.show()
        Motor.on()
        sleep(0.1)
    

while True:
    # display the current menu option
    oled.fill(0)
    oled.text(menu_options[menu_index], 2, 10)
    oled.show()

    # check if the left button is pressed
    if left_button.value():
        # decrement the menu index and wrap around if necessary
        menu_index = (menu_index - 1) % len(menu_options)

    # check if the right button is pressed
    if right_button.value():
        # increment the menu index and wrap around if necessary
        menu_index = (menu_index + 1) % len(menu_options)

    # check if the select button is pressed
    if select_button.value():
        # handle the selected menu option
        if menu_index == 0:
            # do something for option 1
            go_motor(138)
            print("138")
            pass
        elif menu_index == 1:
            # do something for option 2
            go_motor(192)
            print("192")
            pass
        elif menu_index == 2:
            go_motor(264)
            # do something for option 3
            print("264")
            pass
        
        elif menu_index == 3:
            # do something for option 4
            print("purge")
            purge()
            Motor.off()
            pass

    # add a delay to prevent button bouncing
    sleep(0.1)
    Motor.off()

