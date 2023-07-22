import network
import time
import machine

led = machine.Pin("LED", machine.Pin.OUT)

# WIFI SETTINGS

WIFI_SSID = ''
WIFI_PASSWORD = ''

# Set up a wireless hotspot with WIFI_SSID/WIFI_PASSWORD above, useful for testing
WIFI_AP_MODE = False


def wait_wlan(wlan):
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('[WIFI] waiting for connection...')
        
        time.sleep(1)

    if wlan.status() != 3:
        print("[WIFI] Failed setting up wifi, will restart in 1 second")
        
        led.on()
        time.sleep(1)
        led.off()
        
        machine.reset()

def setup_ap():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=WIFI_SSID, password=WIFI_PASSWORD) 
    wlan.active(True)
    wait_wlan(wlan)
    
    print('set up access point:', WIFI_SSID, 'with ip = ', wlan.ifconfig()[0])
    return wlan

def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.disconnect()
    
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    wait_wlan(wlan)
    
    print('[WIFI] connected to wifi:', WIFI_SSID, 'with ip = ', wlan.ifconfig()[0])
    
    led.on()
    return wlan

def run():
    wlan = connect_wlan() if not WIFI_AP_MODE else setup_ap()	
