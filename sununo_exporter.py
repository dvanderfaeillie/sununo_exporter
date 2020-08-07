#!/usr/bin/env python

from prometheus_client import start_http_server, Info, Summary, Enum, Counter, Gauge, Histogram
import requests
from requests.auth import HTTPBasicAuth
import signal
import sys

# Input local SAJ IP, username and password here
SAJ = 'http://IP'
SAJURL = SAJ + '/status/status.php'
SAJ_LOGIN = 'admin'
SAJ_PW = 'admin'

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

def process_saj():
    states = {0: 'Undefined', 1: 'Waiting', 2: 'Normal',-1: 'Error'}
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
        DEVICE_STATE.set(int(list[22]))
    except requests.exceptions.RequestException as e:
        DEVICE_STATE.set(-1)

def signal_handler(signal, frame):
        print('Pressed Ctrl+C')
        sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    # Start up the server to expose the metrics.
    start_http_server(9200)
    # Generate some requests.
    while True:
        process_saj()
