import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS



'''
Data services functions
'''



def connect(
    url: str,
    token: str,
    org: str
) -> influxdb_client.InfluxDBClient:
    ''' Connect to InfluxDB and return the write API client
    '''

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return (write_api)


def write(
    write_api,
    bucket: str,
    org: str,
    measurement: str,
    tag: str,
    data: dict,
) -> None:
    ''' Write data to InfluxDB
    '''

    p = influxdb_client.Point(measurement).tag("module", tag)
    for key, value in data.items():
        p.field(key, value)

    write_api.write(bucket=bucket, org=org, record=p)
