# solaredge-modbus-collector
SolarEdge Modbus TCP data collector

Adapted from: [binsentsu/home-assistant-solaredge-modbus](https://github.com/binsentsu/home-assistant-solaredge-modbus)

Collects data from a SolarEdge inverter, formats the data and writes to an InfluxDB time series database.

## Enabling Modbus TCP on a SolarEdge Inverter
1. Enable wifi direct on the inverter by switching the red toggle switch on the inverter to "P" position for less than 5 seconds.
2. Connect to the inverter access point like you would for a normal wifi network. The wifi password is published at the right side of the inverter. 
3. Open up a browser and go to http://172.16.0.1 > Site Communication. From this webpage you can enable modbus TCP without setApp or installer account.

## Running Using Docker
See ["README_DOCKER.md"](README_DOCKER.md)
or [DockerHub](https://hub.docker.com/repository/docker/ben0p/solaredge-modbus-collector/general)
## Prerequisites
### Common
1. Ensure Modbus TCP is enabled on your inverter as above.
2. Have an InfluxDB v2 instance running and a bucket set up with an API key.
3. The SolarEdge inverter is connected to a network and accessible from where you are running the script, either docker or locally.
4. Install Python, working on v3.10.6 as of writing this
5. Install Python requirements
```
pip install -r requirements.txt
```

## Setting the Environment
NOTE: This has only been tested on a single phase  with one battery.
### Mandatory Environment Fields

- INVERTER_IP: The IP address of your inverter
- INFLUX_BUCKET: Your InfluxDB bucket
- INFLUX_ORG: Your InfluxDB organization
- INFLUX_TOKEN: Your InfluxDB API token
- INFLUX_URL: Your InfluxDB URL

### Optional Fields
- POLLING_INTERVAL: Polling interval in seconds (Default 5)
- LOGGING_LEVEL: The logging level, either DEBUG, INFO, WARNING, ERROR, CRITICAL (Default INFO)
- MODBUS_PORT: 1502 # Default 1502
- SLAVE: Modbus Slave number (Default 1)
- THREE_PHASE: If the inverter is three phase (default False)
- METER_1: If meter 1 is installed (Default True)
- METER_2: If meter 2 is installed (Default False)
- METER_3: If meter 3 is installed (Default False)
- BATT_1: If battery 1 is installed (Default True - Set to False if you don't have a battery)
- BATT_2: If battery 2 is installed (Default False)
- BATT_3: If battery 3 is installed (Default False)

### Environment File
1. Rename "example.env.test" to ".env.test" or ".env.whatever"
2. Enter the required variables in that file

## Running
1. Ensure prerequisites are met
2. Set the variables in the environment file as above
4. Run the "main.py" file with the environment file param, uses a .env.test file by default.
```
python main.py
```
4. If your file is called something other than .env.test, define the environment as a parameter, it will look for ".env.yourenvironment"
```
python main.py --env yourenvironment
```