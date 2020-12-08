#!/usr/bin/env python3

import subprocess

import psutil
from PIL import Image
import ST7735
from bme280 import BME280
from ltr559 import LTR559
from pms5003 import PMS5003
from pms5003 import ReadTimeoutError as pmsReadTimeoutError

from enviroplus import gas
from fastapi import FastAPI

app = FastAPI()
pms5003 = PMS5003()
ltr559 = LTR559()
bme280 = BME280()


# Taken from all-in-one example on enviroplus
def get_cpu_temperature():
    process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


@app.get("/")
def get_root():
    return {"status": 200}


@app.get("/particles")
def get_pms():
    try:
        data = pms5003.read()
    except pmsReadTimeoutError:
        return {
            "status": 500,
            "message": "Failed to read PMS5003",
        }
    try:
        return {
            "status": 200,
            "unit": "ug/m3",
            "1.0": float(data.pm_ug_per_m3(1.0)),
            "2.5": float(data.pm_ug_per_m3(2.5)),
            "10": float(data.pm_ug_per_m3(10)),
            "raw_data": str(data),
        }
    except Exception as e:
        return {
            "status": 500,
            "message": e,
        }


@app.get("/light")
def get_ltr():
    unit = "N/A"
    try:
        return {
            "status": 200,
            "unit": unit,
            "proximity": str(ltr559.get_proximity()),
            "light": str(ltr559.get_lux()),
        }
    except Exception as e:
        return {
            "status": 500,
            "message": e,
        }


@app.get("/temperature")
def get_bme():
    unit = "?"
    try:
        return {
            "status": 200,
            "unit": unit,
            "temperature": {
                "measurement": str(bme280.get_temperature()),
                "unit": "C",
            },
            "pressure": {
                "mesurement": str(bme280.get_pressure()),
                "unit": "hPa",
            },
            "humidity": {
                "measurement": str(bme280.get_humidity()),
                "unit": "%",
            },
            # Will need this to calibrate the relationship between cpu and ambient.
            'cpu_temp': {
                "measurement": psutil.sensors_temperatures()['cpu_thermal'][0].current,
                "unit": "C",
            },
        }
    except Exception as e:
        return {
            "status": 500,
            "message": e,
        }

@app.get("/gas")
def get_gas():
    unit = "kO"
    data = gas.read_all()
    try:
        return {
            "status": 200,
            "unit": unit,
            "oxidising": data.oxidising / 1000,
            "reducing": data.reducing / 1000,
            "nh3": data.nh3 / 1000,
        }
    except Exception as e:
        return {
            "status": 500,
            "message": e,
        }


# Display

# Create ST7735 LCD display class
st7735 = ST7735.ST7735(port=0, cs=1, dc=9, backlight=12, rotation=270, spi_speed_hz=10000000)

# Initialize display
st7735.begin()
try:
    st7735.display(Image.open('background.jpg'))
except Exception as e:
    pass
