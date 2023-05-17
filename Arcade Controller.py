from msvcrt import kbhit

# for simulating key presses
from pynput.keyboard import Key, Controller
keyboard = Controller()

# for usb controllers
import pywinusb.hid as hid

all_devices = hid.HidDeviceFilter(vendor_id = 0x2a94).get_devices()

def sample_handler_red(data):
    # print("Raw data: {0}".format(data))
    buttons_sum = data[7]
    a = str(bin(buttons_sum))[2:].zfill(6)
    
    
    # yel, blu, gre, red
    pressed_buttons = []
    for i in reversed(a):
        pressed_buttons.append(int(i))

    #-1,0,1
    x = data[1] // 127 - 1                                                                                                                                               
    y = data[2] // 127 - 1
    
    keys = [Key.up, Key.left, Key.down, Key.right]

    #left to right, L1 to ST
    button_code = ['x','c','v','b','n','m']

    for button, value in enumerate(pressed_buttons):
        if value:
            keyboard.press(  button_code[button])
            keyboard.release(button_code[button])

    if   x == -1:
        keyboard.press(keys[1])
        keyboard.release(keys[3])

    elif x ==  1:
        keyboard.press(keys[3])
        keyboard.release(keys[1])
        
    else:
        keyboard.release(keys[1])
        keyboard.release(keys[3])

    if   y == -1:
        keyboard.press(keys[0])
        keyboard.release(keys[2])

    elif y ==  1:
        keyboard.press(keys[2])
        keyboard.release(keys[0])
        
    else:
        keyboard.release(keys[2])
        keyboard.release(keys[0])
    # sleep(.05)

def sample_handler_blue(data):
    # print("Raw data: {0}".format(data))
    buttons_sum = data[7]
    a = str(bin(buttons_sum))[2:].zfill(4)

    # yel, blu, gre, red
    pressed_buttons = []
    for i in reversed(a):
        pressed_buttons.append(int(i))
    
    x = data[1] // 127 - 1 
    y = data[2] // 127 - 1
    
    keys = ['w', 'a', 's', 'd']
    button_code = ['t','y','u','i','o','p']
    for button, value in enumerate(pressed_buttons):
        if value:
            keyboard.press(button_code[button])
            keyboard.release(button_code[button])
    if   x == -1:
        keyboard.press(keys[1])
        keyboard.release(keys[3])

    elif x ==  1:
        keyboard.press(keys[3])
        keyboard.release(keys[1])
    else:
        keyboard.release(keys[1])
        keyboard.release(keys[3])

    if   y == -1:
        keyboard.press(keys[0])
        keyboard.release(keys[2])

    elif y ==  1:
        keyboard.press(keys[2])
        keyboard.release(keys[0])
        
    else:
        keyboard.release(keys[2])
        keyboard.release(keys[0])
    # sleep(.05)
def raw_test():
    # simple test
    # browse devices...
    all_hids = hid.find_all_hid_devices()
    red_index = -1 
    blue_index = -1
    if all_hids:
        
        print("Choose a device to monitor raw input reports:\n")
        print("0 => Exit")
        for index, device in enumerate(all_hids):
            
            device_name = unicode("{0.vendor_name} {0.product_name}" \
                    "(vID=0x{1:04x}, pID=0x{2:04x})"\
                    "".format(device, device.vendor_id, device.product_id))
            print("{0} => {1}".format(index+1, device_name))
            if device.vendor_name[:6] ==  'Dragon':
                if red_index == -1:
                    red_index = index
                else:
                    blue_index = index                
        print("\n\tDevice ('0' to '%d', '0' to exit?) " \
                "[press enter after number]:" % len(all_hids))

              
            
        
        def red_helper():
            device = all_hids[red_index]
            try:
                device.open()

                device.set_raw_data_handler(sample_handler_red)
                print('player 1')
                while not kbhit() and device.is_plugged():
                    #just keep the device opened to receive events
                    pass
            finally:
                device.close()
        def blue_helper():
            device = all_hids[blue_index]
            
            try:
                device.open()

                print('player 2')
                device.set_raw_data_handler(sample_handler_blue)
                
                while not kbhit() and device.is_plugged():
                    pass
            finally:
                device.close()
        
        import threading
        print("starting red")

        red  = threading.Thread(target=red_helper )
        red.start()
        print("running red")

        if blue_index != -1:
            blue = threading.Thread(target=blue_helper)
            blue.start()
        

if __name__ == '__main__':
    # first be kind with local encodings
    import sys
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    raw_test()
