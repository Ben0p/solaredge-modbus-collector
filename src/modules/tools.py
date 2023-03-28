import operator

from pymodbus.client import ModbusTcpClient


'''
Various function tools
'''


def connect(
          host: str,
          port: int
	):
	'''
	Connect to the SolarEdge Energy Hub Inverter
	'''
	client = ModbusTcpClient(host="10.1.1.105", port=1502)
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
	return(registers)


def validate(value, comparison, against):
    ops = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
    }
    if not ops[comparison](value, against):
        raise ValueError(f"Value {value} failed validation ({comparison}{against})")
    return(value)


def calculate_value(value, sf):
        result = value * 10**sf
        return result


def decode_string(decoder):
    s = decoder.decode_string(32)  # get 32 char string
    s = s.partition(b"\0")[0]  # omit NULL terminators
    s = s.decode("utf-8")  # decode UTF-8
    return str(s)