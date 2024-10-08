from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import struct

from utils import tools, modbus



'''
Module for reading the inverter modbus values
'''



def read_modbus_data(
        ENV,
        client,
        address: int,
        count: int,
        slave: int
):
    '''
        Read the inverter modbus data
    '''

    data = {}

    modbus_data = modbus.read_holding_registers(
        client=client,
        address=address,
        count=count,
        slave=slave
    )

    if modbus_data.isError():
        return False

    decoder = BinaryPayloadDecoder.fromRegisters(
        modbus_data.registers,
        byteorder=Endian.BIG
    )
    accurrent = decoder.decode_16bit_uint()
    accurrenta = decoder.decode_16bit_uint()
    accurrentb = decoder.decode_16bit_uint()
    accurrentc = decoder.decode_16bit_uint()
    accurrentsf = decoder.decode_16bit_int()

    accurrent = tools.calculate_value(accurrent, accurrentsf)
    accurrenta = tools.calculate_value(accurrenta, accurrentsf)
    accurrentb = tools.calculate_value(accurrentb, accurrentsf)
    accurrentc = tools.calculate_value(accurrentc, accurrentsf)

    data["accurrent"] = round(accurrent, abs(accurrentsf))
    data["accurrenta"] = round(accurrenta, abs(accurrentsf))

    if ENV.THREE_PHASE:
        data["accurrentb"] = round(accurrentb, abs(accurrentsf))
        data["accurrentc"] = round(accurrentc, abs(accurrentsf))

    acvoltageab = decoder.decode_16bit_uint()
    acvoltagebc = decoder.decode_16bit_uint()
    acvoltageca = decoder.decode_16bit_uint()
    acvoltagean = decoder.decode_16bit_uint()
    acvoltagebn = decoder.decode_16bit_uint()
    acvoltagecn = decoder.decode_16bit_uint()
    acvoltagesf = decoder.decode_16bit_int()

    acvoltageab = tools.calculate_value(acvoltageab, acvoltagesf)
    acvoltagebc = tools.calculate_value(acvoltagebc, acvoltagesf)
    acvoltageca = tools.calculate_value(acvoltageca, acvoltagesf)
    acvoltagean = tools.calculate_value(acvoltagean, acvoltagesf)
    acvoltagebn = tools.calculate_value(acvoltagebn, acvoltagesf)
    acvoltagecn = tools.calculate_value(acvoltagecn, acvoltagesf)

    data["acvoltagean"] = round(acvoltagean, abs(acvoltagesf))

    if ENV.THREE_PHASE:
        data["acvoltageab"] = round(acvoltageab, abs(acvoltagesf))
        data["acvoltagebc"] = round(acvoltagebc, abs(acvoltagesf))
        data["acvoltageca"] = round(acvoltageca, abs(acvoltagesf))
        data["acvoltagebn"] = round(acvoltagebn, abs(acvoltagesf))
        data["acvoltagecn"] = round(acvoltagecn, abs(acvoltagesf))

    acpower = decoder.decode_16bit_int()
    acpowersf = decoder.decode_16bit_int()
    acpower = tools.calculate_value(acpower, acpowersf)

    data["acpower"] = float(round(acpower, abs(acpowersf)))

    acfreq = decoder.decode_16bit_uint()
    acfreqsf = decoder.decode_16bit_int()
    acfreq = tools.calculate_value(acfreq, acfreqsf)

    data["acfreq"] = round(acfreq, abs(acfreqsf))

    acva = decoder.decode_16bit_int()
    acvasf = decoder.decode_16bit_int()
    acva = tools.calculate_value(acva, acvasf)

    try:
        data["acva"] = float(round(acva, abs(acvasf)))
    except OverflowError:
        data["acva"] = None
    try:
        acvar = decoder.decode_16bit_int()
        acvarsf = decoder.decode_16bit_int()
        acvar = tools.calculate_value(acvar, acvarsf)
        data["acvar"] = float(round(acvar, abs(acvarsf)))
    except:
        data["acvar"] = None

    try:
        acpf = decoder.decode_16bit_int()
        acpfsf = decoder.decode_16bit_int()
        acpf = tools.calculate_value(acpf, acpfsf)
        data["acpf"] = float(round(acpf, abs(acpfsf)))
    except (OverflowError, struct.error, NameError):
        data["acpf"] = None

    try:
        acenergy = decoder.decode_32bit_uint()
        acenergysf = decoder.decode_16bit_uint()
        acenergy = tools.validate(
            tools.calculate_value(acenergy, acenergysf), ">", 0
        )
        data["acenergy"] = round(acenergy * 0.001, 3)
    except (OverflowError, struct.error):
        data["acenergy"] = None

    try:
        dccurrent = decoder.decode_16bit_uint()
        dccurrentsf = decoder.decode_16bit_int()
        dccurrent = tools.calculate_value(dccurrent, dccurrentsf)
        data["dccurrent"] = float(round(dccurrent, abs(dccurrentsf)))
    except (OverflowError, struct.error, NameError):
        data["dccurrent"] = None

    try:
        dcvoltage = decoder.decode_16bit_uint()
        dcvoltagesf = decoder.decode_16bit_int()
        dcvoltage = tools.calculate_value(dcvoltage, dcvoltagesf)
        data["dcvoltage"] = float(round(dcvoltage, abs(dcvoltagesf)))
    except (OverflowError, struct.error, NameError):
        data["dcvoltage"] = None

    try:
        dcpower = decoder.decode_16bit_int()
        dcpowersf = decoder.decode_16bit_int()
        dcpower = tools.calculate_value(dcpower, dcpowersf)
        data["dcpower"] = float(round(dcpower, abs(dcpowersf)))
    except (OverflowError, struct.error, NameError):
        data["dcpower"] = None

    try:
        # skip register
        decoder.skip_bytes(2)
        tempsink = decoder.decode_16bit_int()
        # skip 2 registers
        decoder.skip_bytes(4)
        tempsf = decoder.decode_16bit_int()
        
        tempsink = tools.calculate_value(tempsink, tempsf)
        data["tempsink"] = round(tempsink, abs(tempsf))
    except (OverflowError, struct.error, NameError):
        data["tempsink"] = None

    try:
        status = decoder.decode_16bit_int()
        data["status"] = status
        statusvendor = decoder.decode_16bit_int()
        data["statusvendor"] = statusvendor
    except (OverflowError, struct.error, NameError):
        data["status"] = None
        data["statusvendor"] = None

    return data