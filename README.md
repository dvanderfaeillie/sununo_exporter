# SAJ Sununo exporter #
A small Python script to export statistics of a SAJ Sununo solar inverter to a Prometheus server. 
Tested with a SAJ Sununo Plus 2K inverter and an attached WiFi module. Data is also exported to SAJ's [eSolar portal](https://fop.saj-electric.com) which kinda sucks... Using the following script takes back command of the data. Logging the date using Prometheus and graphing it using Grafana turns out to be easy!

The script outputs some metrics with the `saj` prefix (for easy retrieval) on port `9200`. The port can easily be changed in the python script. Note that `saj_device_running_state`-metric returns the following values:

    -1: Error        inverter is down (not enough light)
    0:  Undefined    'new' unknown state
    1:  Waiting      inverter is booting up/shutting down due to insufficient light
    2:  Normal       inverter is working normally
    
When the inverter is down all metrics but `saj_ac_output_power` are set to `NaN` to prevent `0` values from being graphed. The `saj_ac_output_power`-metric is set to `0` since that seems usefull for graphing and calculating averages and so on...

## Installation as systemd service ##
One needs `python3` (Although python2 would probably work as well) with the `requests` (installed by default) and `prometheus_client` libraries. 

To have it installed as root:
`sudo pip3 install prometheus_client`
Then clone the repo somewhere using
`git clone https://github.com/dvanderfaeillie/sununo_exporter.git`

You can test the script for errors using `/usr/bin/python3 INSTALL_DIR/sununo_exporter/sununo_exporter.py`. Use <kbd>CTRL</kbd>+<kbd>C</kbd> to end the script.

#### Systemd setup ####
I already had a node_exporter user which handles the other Prometheus exports on my system. The same user handles this script.
To add this user run: `sudo useradd --no-create-home --shell /bin/false node_exporter`.

Next make a `systemd` unit file
`sudo touch /etc/systemd/system/sununo-exporter.service`
and add the following:

    [Unit]
    Description=SAJ Sununo Exporter
    After=network-online.target

    [Service]
    User=node_exporter
    Group=node_exporter
    Type=simple
    ExecStart=/usr/bin/python3 INSTALL_DIR/sununo_exporter/sununo_exporter.py

    [Install]
    WantedBy=multi-user.target

If needed reload the `systemd-daemon` using `sudo systemctl daemon-reload`. All what is needed now is to start and enable the service using:
`sudo systemctl start sununo-exporter`. Check for errors using `sudo service sununo-exporter status`, and if all is well enable the service for auto-start using: `sudo systemctl enable sununo-exporter`.


## Prometheus setup ##
Add the following to your `prometheus.yaml` configuration file:

    - job_name: 'sununo'
      scrape_interval: 5s
      static_configs:
        - targets: ['ip:9200']

### status/status.php configuration ###
If a value is `65535` (which is the maximum of a `unsigned short int`) then this implies not applicable (N/A)

An example export might be the following:

    0   1,        Doesn't seem to mean anything...
    1   424257,   Total generated: 4242.57 kWh
    2   155335,   Total running time: 15533.5 h
    3   26,       Today generated:  0.26 kWh
    4   59,       Today running time: 5.9 h
    
    DC INPUT
    5   1008,     PV1 Voltage: 100.8V
    6   65535,    PV1 Current
    7   0,        PV2 Voltage
    8   65535,    PV2 Current
    9   65535,    PV3 Voltage
    10  65535,    PV3 Current
    
    AC OUTPUT
    11  638,      Grid-connected Power: 638W
    12  5000,     Grid-connected Frequency: 50.00Hz
    13  2369,     Line 1 Voltage: 236.9 V
    14  272,      Line 1 Current: 2.72A
    15  65535,    Line 2 Voltage
    16  65535,    Line 2 Current
    17  65535,    Line 3 Voltage
    18  65535,    Line 3 Current
    
    OTHER STATUS
    19  3675,     Bus Voltage: 367.5V
    20  344,      Device temperature: 34.4°C
    21  33304,    CO2 emission reduction: 3330.4 kg
    22  2         Running state, 1: Waiting, 2: Normal

## TODO ##
There are more statistics to be gathered from the solar inverters WiFi module. For example, the page `ip/info.php` containing firmware info can also be scraped.


### License ###
This project is licensed under the terms of the GNU General Public License v3.0.
