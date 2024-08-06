from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from utils import const, tools, modbus



'''
Module for reading the modbus values for a battery
'''



def read_modbus_data(
        client,
        address: int,
        count: int,
        slave: int,
        prefix: str
):
    '''
    Read the battery modbus data
    '''

    data = {}

    modbus_data = modbus.read_holding_registers(
        client=client,
        address=address,
        count=count,
        slave=slave
    )

    if not modbus_data.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            modbus_data.registers,
            byteorder=Endian.BIG,
            wordorder=Endian.LITTLE,
        )

        # 0x00 - 16 - manufacturer
        try:
            data[prefix + "manufacturer"] = tools.decode_string(decoder)
        except UnicodeDecodeError:
             data[prefix + "manufacturer"] = None

        # 0x10 - 16 - model
        try:
            data[prefix + "model"] = tools.decode_string(decoder)
        except UnicodeDecodeError:
            data[prefix + "model"] = None

        # 0x20 - 16 - firmware version
        try:
            data[prefix + "firmware_version"] = tools.decode_string(decoder)
        except UnicodeDecodeError:
            data[prefix + "firmware_version"] = None

        # 0x30 - 16 - serial number
        data[prefix + "serial_number"] = tools.decode_string(decoder)

        # 0x40 - 1 - device ID
        data[prefix + "device_id"] = decoder.decode_16bit_uint()

        # 0x41 - 1 - reserved
        decoder.decode_16bit_uint()

        # 0x42 - 2 - rated energy
        data[prefix + "rated_energy"] = decoder.decode_32bit_float()

        # 0x44 - 2 - max charge continuous power
        data[prefix +
             "max_power_continuous_charge"
             ] = decoder.decode_32bit_float()

        # 0x46 - 2 - max discharge continuous power
        data[prefix +
             "max_power_continuous_discharge"
             ] = decoder.decode_32bit_float()

        # 0x48 - 2 - max charge peak power
        #
        data[prefix + "max_power_peak_charge"] = decoder.decode_32bit_float()

        # 0x4A - 2 - max discharge peak power
        data[prefix + "max_power_peak_discharge"] = decoder.decode_32bit_float()

        storage_data = modbus.read_holding_registers(
            client=client,
            address=address + 0x6C,
            count=28,
            slave=slave
        )

        if storage_data.isError():
            return False

        decoder = BinaryPayloadDecoder.fromRegisters(
            storage_data.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE
        )

        # 0x6C - 2 - avg temp C
        tempavg = decoder.decode_32bit_float()
        # 0x6E - 2 - max temp C
        tempmax = decoder.decode_32bit_float()
        # 0x70 - 2 - inst voltage V
        batteryvoltage = decoder.decode_32bit_float()
        # 0x72 - 2 - inst current A
        batterycurrent = decoder.decode_32bit_float()
        # 0x74 - 2 - inst power W
        batterypower = decoder.decode_32bit_float()
        # 0x76 - 4 - cumulative discharged (Wh)
        cumulative_discharged = decoder.decode_64bit_uint()
        # 0x7a - 4 - cumulative charged (Wh)
        cumulative_charged = decoder.decode_64bit_uint()
        # 0x7E - 2 - current max size Wh
        battery_max = decoder.decode_32bit_float()
        # 0x80 - 2 - available size Wh
        battery_availbable = decoder.decode_32bit_float()
        # 0x82 - 2 - SoH %
        battery_SoH = decoder.decode_32bit_float()
        
        # 0x84 - 2 - SoC %
        battery_SoC  = decoder.decode_32bit_float()
        if battery_SoC > 100:
            battery_SoC = 100.0
        if battery_SoC < 0:
            battery_SoC = 0.0
        data[prefix + "state_of_charge"] = round(battery_SoC, 2)
        

        data[prefix + "temp_avg"] = round(tempavg, 1)
        data[prefix + "temp_max"] = round(tempmax, 1)
        data[prefix + "voltage"] = round(batteryvoltage, 3)
        data[prefix + "current"] = float(round(batterycurrent, 3))
        data[prefix + "power"] = float(round(batterypower, 3))
        data[prefix + "energy_discharged"] = round(
            cumulative_discharged / 1000, 3
        )
        data[prefix + "energy_charged"] = round(
            cumulative_charged / 1000, 3
        )
        data[prefix + "size_max"] = round(battery_max, 3)
        data[prefix +
             "size_available"] = round(battery_availbable, 3)
        data[prefix + "state_of_health"] = round(battery_SoH, 0)
        
        battery_status = decoder.decode_32bit_uint()

        # voltage and current are bogus in certain statuses
        if not battery_status in [3, 4, 6]:
            data[prefix + "voltage"] = 0.0
            data[prefix + "current"] = 0.0
            data[prefix + "power"] = 0.0

        if battery_status in const.BATTERY_STATUSSES:
            data[prefix +
                 "status"] = const.BATTERY_STATUSSES[battery_status]
        else:
            # data[prefix + "status"] = battery_status
            print(f"{battery_status=}")
            
        return data