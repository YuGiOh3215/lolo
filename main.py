import weatherbit
import microbit

from microbit import *
from logging import *


class TimeAndDate:
#    Year = 2023
#    Month = 5
#    Day = 20
    _refHours = 0
    _refMinutes = 0
    _refSeconds = 0
#    Hours = 21
#    Minutes = 20
    Seconds = 0
    _referenceCount = 0

    def __init__(self):
        self.Count = 0
        self._referenceCount = 0

    def start(self):
        self._referenceCount = input.running_time()
        self.Count = 0
 
    def getTime(self):
        self.Count = (input.running_time() - self._referenceCount)/1000
        compare = self.Count - ((self._refHours * 3600) + \
        (self._refMinutes * 60))

        if (compare >= 60):
            self.Seconds = Math.round_with_precision((compare - 60),0)
            self._refMinutes = self._refMinutes + 1
        else:
            self.Seconds = Math.round_with_precision(compare,0)

        if (self._refMinutes >= 60):
            self._refMinutes = self._refMinutes - 60
            self._refHours = self._refHours + 1

        if (self._refHours >= 24):
            self._refHours = self._refHours - 24

        szLine = self.Count + "\t"+ self._refHours + \
         ':' + self._refMinutes + ':' + self.Seconds
        return szLine


class LoggingParams:
    idefaultLogInterv = 2000
    _iLogInterval = 0
    
    def __init__(self):

        self._iLogInterval = self.idefaultLogInterv

    def getLogInterval(self):
        return (self._iLogInterval)


def showLoggingLED():
    basic.show_leds("""
        . . . . .
        . . . . #
        . . . # .
        # . # . .
        . # . . .
    """)


def showNotLoggingLED():
    basic.show_leds("""
        # . . . #
        . # . # .
        . . # . .
        . # . # .
        # . . . #
    """)

def showQMarkLED():
    basic.show_leds("""
        . # # # .
        . # # #.
        . . # . .
        . . . . .
        . . # . .
    """)

   
class dataOutput:
    def __init__(self):
        self.szLine = ""

    def writeHeader(self):
        self.szLine = 'Time\tTiC\tHUM\tPRESS\tRAIN\tWSP\tCWD'
        serial.write_line(self.szLine)

    def writeData(self,TTime, TiC, HUM, PRESS, RAIN, WSP, CWD):
        self.szLine = TTime + '\t' + \
            TiC + '\t' + \
            HUM + '\t' + \
            PRESS + '\t' + \
            RAIN + '\t' + \
            WSP + '\t' + \
            CWD

        serial.write_line(self.szLine)


def on_button_pressed_a():
    global LoggingIsOn
    LoggingIsOn = not (LoggingIsOn)
    
    if (LoggingIsOn == True):
        showLoggingLED()
    else:
        showNotLoggingLED()
        
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    
    showQMarkLED()
        
input.on_button_pressed(Button.B, on_button_pressed_b)



p1 = LoggingParams()
dataLog = dataOutput()
td = TimeAndDate()

LoggingIsOn = False

weatherbit.start_wind_monitoring()
weatherbit.start_weather_monitoring()

serial.redirect(SerialPin.P15, SerialPin.P14, BaudRate.BAUD_RATE9600)
#serial.redirect_to_usb()

"""

Note: If "???" is displayed, direction is unknown!

"""


def on_forever():
    global p1, dataLog, td
     
    tempC = 0
    current_WindSpeed = 0.0
    current_WindDirection_List = ""
  
    if LoggingIsOn == True:
        # -------- wind --------
        current_WindSpeed = Math.round_with_precision(weatherbit.wind_speed() * 3600 / 1000,2)
        
        current_WindDirection_List = weatherbit.wind_direction()

#        soilTemperature = Math.round_with_precision(weatherbit.soil_temperature(),1)
#        soilHumid = Math.round_with_precision(weatherbit.soil_moisture(),1)
#        altitude = Math.round_with_precision(weatherbit.altitude(),1)
        rain = Math.round_with_precision(weatherbit.rain(),1)

        # -------- temperature --------
        tempC = Math.round_with_precision((weatherbit.temperature()/ 100),0)
        # -------- humidity --------

        humid = Math.round_with_precision((weatherbit.humidity()/ 1024),1)
        # -------- pressure --------
        pressure = Math.round_with_precision(weatherbit.pressure()/ 25600,1)

        dataLog.writeData(td.getTime(),
                        tempC, humid,
                        pressure, rain,
                        current_WindSpeed,
                        current_WindDirection_List,) # altitude, soilHumid, soilTemperature)
    else:
        showNotLoggingLED()
        
    basic.pause(p1.getLogInterval())

td.start()
dataLog.writeHeader()
while True:
    on_forever()

