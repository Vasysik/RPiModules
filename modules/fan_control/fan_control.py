import RPi.GPIO as GPIO
import sys, traceback, json
from time import sleep
from re import findall
from subprocess import check_output
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def get_temp():
    temp = check_output(["vcgencmd", "measure_temp"]).decode()
    temp = float(findall(r'\d+\.\d+', temp)[0])
    return temp

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

config = read_json("config.json")
influxdb_config = read_json(config['influxdb_config_path'])
client = InfluxDBClient(url=influxdb_config['influxdb_url'], token=influxdb_config['influxdb_token'])
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_current_data(temp, pinState):
    fan_state = "On" if pinState else "Off"
    point = Point("fan_status").tag("location", "raspberry_pi").field("temperature", temp).field("fan_state", fan_state)
    write_api.write(bucket=config['influxdb_bucket'], org=config['influxdb_org'], record=point)

try:
    settings = read_json("settings.json")
    tempOn = settings['tempOn']
    tempOff = settings['tempOff']
    mode = settings['mode']
    
    controlPin = 14
    pinState = False
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(controlPin, GPIO.OUT, initial=0)

    while True:
        settings = read_json("settings.json")
        tempOn = int(settings['tempOn'])
        tempOff = int(settings['tempOff'])
        mode = settings['mode']

        temp = get_temp()

        if mode == 'smart':
            if temp > tempOn and not pinState or temp < tempOff and pinState:
                pinState = not pinState
                GPIO.output(controlPin, pinState)
        elif mode == 'normal':
            if temp > tempOn:
                pinState = True
                GPIO.output(controlPin, pinState)
            elif temp < tempOff:
                pinState = False
                GPIO.output(controlPin, pinState)
        else:
            pinState = True
            GPIO.output(controlPin, pinState)

        write_current_data(temp, pinState)
        print(f"Temperature: {temp}°C, Fan State: {'On' if pinState else 'Off'}, Mode: {mode}")
        sleep(1)

except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except Exception as e:
    print("Other Exception")
    print("--- Start Exception Data:")
    traceback.print_exc(limit=2, file=sys.stdout)
    print("--- End Exception Data:")
finally:
    print("CleanUp")
    GPIO.cleanup()
    print("End of program")
