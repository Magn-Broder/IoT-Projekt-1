import umqtt_robust2 as mqtt
import _thread as thread
import gps_funktion
import neopixel
from machine import Pin, ADC
from hcsr04 import HCSR04
from time import sleep

# Variabler til neopixel ring
n = 12
p = 15
np = neopixel.NeoPixel(Pin(p), n)

# Variabler til Batterimåler
analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)

# Off og on Funktioner til Neopixel led ring
def np_on():
    for i in range(12):
        np[i] = (50, 0, 0)
        np.write()
     
def np_off():
    for i in range(12):
        np[i] = (0, 0, 0)
        np.write()

# Funtion til GPS og Batterimåler
def gps_batterimaaler_func():
    while True:
        try:
            # ****** HER BEGYNDER GPS ******
            # Denne variabel vil have GPS data når den har fået kontakt til sattellitterne ellers vil den være None
            gps_data = gps_funktion.gps_to_adafruit
            print(f"\ngps_data er: {gps_data}")
            
            #For at vise lokationsdata på adafruit dashboard skal det sendes til feed med /csv til sidst
            mqtt.web_print(gps_data, '_Magn_/feeds/mapfeed/csv')        
            sleep(4) # vent mere end 3 sekunder mellem hver besked der sendes til adafruit
                  
            if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
                mqtt.besked = ""            
            mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
            print(".", end = '') # printer et punktum til shell, uden et enter
            
            # ***** HER BEGYNDER BATTERI MÅLER ******
            analog_val = analog_pin.read()
            volts = (analog_val * 0.000902)*5 #Konvertere fra binær værdi til volt
            battery_percentage = int((volts / 2)*100 - 320)  #Rough batteri procent omregning
            print("Battery procenten er:", battery_percentage, "%")
        
            mqtt.web_print(battery_percentage,'_Magn_/feeds/Batterifeed')
            sleep(4)
        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            mqtt.c.disconnect()
            mqtt.sys.exit()
            
# Funktion til ultrasonsisk-afstandsmåler og Neopixel led ring
def afstand_neopixel_func():
    while True:
        sensor = HCSR04(trigger_pin=18, echo_pin=22, echo_timeout_us=10000000)

        distance = sensor.distance_cm()
    
        if distance <= 7:
            np_on()
            sleep(0.1)
        else:
            np_off()
            sleep(0.1)
        
# Starter to tråde en til gps_batterimaaler_func & en til afstand_neopixel_func
thread.start_new_thread(gps_batterimaaler_func,())
thread.start_new_thread(afstand_neopixel_func,())