from machine import UART
from micropyGPS import MicropyGPS
import _thread

# denne variabel opdateres til at holde gps data
gps_to_adafruit = None
# instans af gps klassen opdateres her
gps = None
def gps_main():
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    global gps
    gps = MicropyGPS()
    while True:
        buf = uart.readline()
        if buf:
            for char in buf:
                gps.update(chr(char)) # Note the conversion to to chr, UART outputs ints normally
        
        #different gps methods that can be used:
        
        #print('UTC Timestamp:', gps.timestamp)
        #print('Date:', gps.date_string('long'))
        #print('Satellites:', gps.satellites_in_use)
        #print('Altitude:', gps.altitude)
        #print('Latitude:', gps.latitude_string())
        #print('Longitude:', gps.longitude_string())
        #print('Horizontal Dilution of Precision:', gps.hdop)
        #print('Compas direction: ', gps.compass_direction())
        
        formattedLat = gps.latitude_string()
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]
        formattedAlt = str(gps.altitude)
        formattedSpd = gps.speed_string()
        formattedSpd = formattedSpd[:-5]
        #print(gps.speed_string())
        gps_ada = formattedSpd+","+formattedLat+","+formattedLon+","+formattedAlt
        
        if formattedLat != "0.0" and formattedLon != "0.0":
            #print("gps_ada: ",gps_ada)
            global gps_to_adafruit
            gps_to_adafruit = gps_ada

_thread.start_new_thread(gps_main, ())

