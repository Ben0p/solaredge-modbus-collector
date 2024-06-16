import env
import pymodbus
import time
import struct

from utils import influx, modbus
from modules import inverter, meter, battery, status



'''
SolarEdge Modbus TCP Collector
Collects metrics from SolarEdge Home Energy Hub inverters
Modbus must be enabled on inverter
'''



def run():

    while True:
        # Initialize modbus connection
        modbus_client = modbus.connect(env.INVERTER_IP, env.MODBUS_PORT)
        print("Connected to Inverter Modbus TCP")


        # Initialize InfluxDB connection
        influx_write_api = influx.connect(
            env.INFLUX_URL, env.INFLUX_TOKEN, env.INFLUX_ORG)
        print("Connected to InfluxDB")


        while True:
            print("-"*50)

            #==========#
            # Inverter #
            #==========#
            try:
                # Collect and convert inverter data
                inverter_data = inverter.read_modbus_data(
                    client=modbus_client,
                    address=40071,
                    count=38,
                    slave=env.SLAVE
                )
                print("Retrived inverter data")
            except pymodbus.exceptions.ConnectionException:
                break
            
            if inverter_data:
                influx.write(
                    write_api=influx_write_api,
                    bucket=env.INFLUX_BUCKET,
                    org=env.INFLUX_ORG,
                    measurement='solaredge',
                    tag='inverter',
                    data=inverter_data
                )
                print("Written inverter data to InfluxDB")
            else:
                print("Error retrieving inverter data")


            time.sleep(0.5)

            #=========#
            # Meter 1 #
            #=========#
            try:
                # Collect and convert meter 1 data
                m1_data = meter.read_modbus_data(
                    client=modbus_client,
                    address=40190,
                    count=103,
                    slave=env.SLAVE,
                    prefix="m1_"
                )
                print("Retrived meter 1 data")
            except pymodbus.exceptions.ConnectionException:
                break
            except struct.error:
                pass


            if m1_data:
                influx.write(
                    write_api=influx_write_api,
                    bucket=env.INFLUX_BUCKET,
                    org=env.INFLUX_ORG,
                    measurement='solaredge',
                    tag='m1',
                    data=m1_data
                )
                print("Written meter 1 data to InfluxDB")
            else:
                print("Error retrieving meter 1 data")

            time.sleep(0.5)

            #==========+#
            # Battery 1 #
            #==========+#
            try:
                # Collect and convert battery 1 data
                b1_data = battery.read_modbus_data(
                    client=modbus_client,
                    address=0xE100,
                    count=0x4C,
                    slave=env.SLAVE,
                    prefix="b1_"
                )
                print("Retrived battery 1 data")
            except pymodbus.exceptions.ConnectionException:
                break

            if b1_data:
                influx.write(
                    write_api=influx_write_api,
                    bucket=env.INFLUX_BUCKET,
                    org=env.INFLUX_ORG,
                    measurement='solaredge',
                    tag='b1',
                    data=b1_data
                )
                print("Written battery 1 data to InfluxDB")
            else:
                print("Error retrieving battery 1 data")

            time.sleep(0.5)

            #========#
            # Status #
            #========#
            try:
                status_data = status.read_modbus_data(
                    client=modbus_client,
                    address=0xE000,
                    slave=env.SLAVE,
                )
            except pymodbus.exceptions.ConnectionException:
                break

            if status_data:
                influx.write(
                    write_api=influx_write_api,
                    bucket=env.INFLUX_BUCKET,
                    org=env.INFLUX_ORG,
                    measurement='solaredge',
                    tag='status',
                    data=status_data
                )
                print("Written status data to InfluxDB")
            else:
                print("Error retrieving status data")


            print(f"Sleeping for {env.POLLING_INTERVAL}s")
            print("-"*50)
            time.sleep(env.POLLING_INTERVAL)
        print("Modbus connection error")
        time.sleep(10)
		

if __name__ == "__main__":
    run()
