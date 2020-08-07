# sununo_exporter
Prometheus exporter for SAJ Sununo inverters


### SAJ Sununo

65535 = unsigned short int range which implies N/A 

    0   1,        Unknown
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
