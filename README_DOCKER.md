# solaredge-modbus-collector
SolarEdge Modbus TCP data collector

Adapted from: [binsentsu/home-assistant-solaredge-modbus](https://github.com/binsentsu/home-assistant-solaredge-modbus)

Collects data from a SolarEdge inverter, formats the data and writes to an InfluxDB time series database.

GitHub: [Ben0p/solaredge-modbus-collector](https://github.com/Ben0p/solaredge-modbus-collector)


## Enabling Modbus TCP on a SolarEdge Inverter
1. Enable wifi direct on the inverter by switching the red toggle switch on the inverter to "P" position for less than 5 seconds.
2. Connect to the inverter access point like you would for a normal wifi network. The wifi password is published at the right side of the inverter. 
3. Open up a browser and go to http://172.16.0.1 > Site Communication. From this webpage you can enable modbus TCP without setApp or installer account.

## Prerequisites

1. Ensure Modbus TCP is enabled on your inverter as above.
2. Have an InfluxDB v2 instance running and a bucket set up with an API key.
3. The SolarEdge inverter is connected to a network and accessible from where you are running the script, either docker or locally.

### Docker
1. Docker is installed (obviously)
2. docker compose plugin if using a docker-compose.yml file

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


### Running Using Docker run
1. Pull the image to ensure you have the latest
```bash
docker pull ben0p/solaredge-modbus-collector
```
2. Run the image (Windows)
```bash
docker run -d ^
-e INVERTER_IP='10.0.0.10' ^
-e INFLUX_BUCKET='my_bucket' ^
-e INFLUX_ORG='my_org' ^
-e INFLUX_TOKEN='my_api_token' ^
-e INFLUX_URL='http://10.0.0.11:8086/' ^
--name solaredge_modbus_collector ^
ben0p/solaredge-modbus-collector
```
3. Run the image (Linux)
```bash
docker run -d \
-e INVERTER_IP='10.0.0.10' \
-e INFLUX_BUCKET='my_bucket' \
-e INFLUX_ORG='my_org' \
-e INFLUX_TOKEN='my_api_token' \
-e INFLUX_URL='http://10.0.0.11:8086/' \
--name solaredge_modbus_collector \
ben0p/solaredge-modbus-collector
```

### Running using docker compose
1. Create a docker-compose.yml file (see examples)
2. Set your environment variables in the docker-compose.yml file
3. Run docker compose
```bash
docker compose -p "solaredge_modbus" up -d
```
#### With InfluxDB
If you want persistant data, bind mount the volume as in the example. Modify as necessary
```yaml
services:
  influxdb:
    image: influxdb
    ports:
      - "8086:8086"
    volumes:
      - ./influxdb/data:/var/lib/influxdb2

  solaredge-mudbus-collector:
    image: ben0p/solaredge-modbus-collector
    container_name: solaredge_modbus_collector
    environment:
        - INVERTER_IP=10.0.0.10
        - INFLUX_BUCKET=my_bucket
        - INFLUX_ORG=my_org
        - INFLUX_TOKEN=my_api_token
        - INFLUX_URL=http://influxdb:8086/
```

#### Without InfluxDB
```yaml
services:
  solaredge-mudbus-collector:
    image: ben0p/solaredge-modbus-collector
    container_name: solaredge_modbus_collector
    environment:
        - INVERTER_IP=10.0.0.10
        - INFLUX_BUCKET=my_bucket
        - INFLUX_ORG=my_org
        - INFLUX_TOKEN=my_api_token
        - INFLUX_URL=http://10.0.0.11:8086/
```