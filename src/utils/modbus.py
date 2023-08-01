from pymodbus.client import ModbusTcpClient


'''
Modbus functions
'''


def connect(
    host: str,
    port: int
):
    '''
    Connect to the Modbus TCP device
    '''
    client = ModbusTcpClient(host=host, port=port)
    client.connect()
    return (client)


def read_holding_registers(
    client: ModbusTcpClient,
    address: int,
    count: int,
    slave: int
):
    registers = client.read_holding_registers(
        address=address, count=count, slave=slave
    )
    return (registers)
