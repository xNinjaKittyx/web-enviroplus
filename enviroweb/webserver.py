#!/usr/bin/env python3

import ST7735
from bme280 import BME280
from ltr559 import LTR559
from pms5003 import PMS5003
from pms5003 import ReadTimeoutError as pmsReadTimeoutError

from enviroplus import gas

pms5003 = PMS5003()

unit = "ug/m3"
try:
    data = pms5003.read()
except pmsReadTimeoutError:
    print("Failed to read PMS5003")
else:
    data = float(data.pm_ug_per_m3(1.0))
    print(data, unit)

ltr559 = LTR559()
print(ltr559.get_proximity())
print(ltr559.get_lux())

# Display

# Create ST7735 LCD display class
st7735 = ST7735.ST7735(port=0, cs=1, dc=9, backlight=12, rotation=270, spi_speed_hz=10000000)

# Initialize display
st7735.begin()

WIDTH = st7735.width
HEIGHT = st7735.height


data = gas.read_all()
print(data.oxidising / 1000, "kO")
print(data.reducing / 1000, "kO")
print(data.nh3 / 1000, "kO")

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()
print(bme280.get_temperature())
print(bme280.get_pressure())
print(bme280.get_humidity())

def run():
    pass
