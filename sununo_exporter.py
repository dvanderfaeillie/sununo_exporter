#!/usr/bin/env python

from prometheus_client import start_http_server, Info, Summary, Enum, Counter, Gauge, Histogram
import requests
from requests.auth import HTTPBasicAuth
import signal
import sys
import time

# Input local SAJ IP, username and password here
SAJ = 'http://IP'
SAJURL = SAJ + '/status/status.php'
SAJ_LOGIN = 'admin'
SAJ_PW = 'admin'
PORT = 9200

# Creating metrics
TOTAL_GENERATED = Gauge('saj_total_generated', 'Total amount of energy generated (kWh)')
TOTAL_RUNNING_TIME = Gauge('saj_total_running_time', 'Total uptime of the inverter (h)')
TODAY_GENERATED = Gauge('saj_today_generated', 'Daily amount of energy generated (kWh)')
TODAY_RUNNING_TIME = Gauge('saj_today_running_time', 'Daily uptime of the inverter (h)')
DC_INPUT_VOLTAGE = Gauge('saj_dc_input_voltage', 'Current voltage generated on DC input (V)')
AC_OUTPUT_POWER = Gauge('saj_ac_output_power', 'Current grid-connected power output (W)')
AC_OUTPUT_VOLTAGE = Gauge('saj_ac_output_voltage', 'Current voltage generated on AC output (V)')
AC_OUTPUT_CURRENT = Gauge('saj_ac_output_current', 'Current current :) generated on AC output (A)')
DEVICE_TEMP = Gauge('saj_device_temperature', 'Device temperature (°C)')
DEVICE_STATE = Gauge('saj_device_running_state', 'Device running state')

def represents_int(string):
    """Returns whether a string contains an integer using try - except."""
    try: 
        int(string)
        return True
    except ValueError:
        return False

def process_saj():
    """Main script which processes the SAJ status.php into Prometheus metrics."""
    states = {0: 'Undefined', 1: 'Waiting', 2: 'Normal', -1: 'Error'}
    try:
        file = requests.get(SAJURL, auth=HTTPBasicAuth(SAJ_LOGIN, SAJ_PW)) 
        text = file.text
        list = text.split(',')

        TOTAL_GENERATED.set(int(list[1])/100)
        TOTAL_RUNNING_TIME.set(int(list[2])/10)
        TODAY_GENERATED.set(int(list[3])/100)
        TODAY_RUNNING_TIME.set(int(list[4])/10)
        DC_INPUT_VOLTAGE.set(int(list[5])/10)
        AC_OUTPUT_POWER.set(int(list[11]))
        AC_OUTPUT_VOLTAGE.set(int(list[13])/10)
        AC_OUTPUT_CURRENT.set(int(list[14])/100)
        DEVICE_TEMP.set(int(list[20])/10)
        if represents_int(list[22]) and int(list[22]) in states:
            DEVICE_STATE.set(int(list[22]))
        else:
            DEVICE_STATE.set(0)
    except requests.exceptions.RequestException as e:
        TOTAL_GENERATED.set('NaN')
        TOTAL_RUNNING_TIME.set('NaN')
        TODAY_GENERATED.set('NaN')
        TODAY_RUNNING_TIME.set('NaN')
        DC_INPUT_VOLTAGE.set('NaN')
        AC_OUTPUT_POWER.set(0)
        AC_OUTPUT_VOLTAGE.set('NaN')
        AC_OUTPUT_CURRENT.set('NaN')
        DEVICE_TEMP.set('NaN')
        DEVICE_STATE.set(-1)

def signal_handler(signal, frame):
    """Handles the input of console interrupt."""
    print('Pressed Ctrl+C')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    # Start up the server to expose the metrics.
    start_http_server(PORT)
    # Generate some requests.
    while True:
        process_saj()
        time.sleep(5)
