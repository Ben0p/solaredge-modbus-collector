import env

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from utils import tools, modbus



'''
Module for reading the modbus values for a meter
'''



def read_modbus_data(
        client,
        address: int,
        count: int,
        slave: int,
        prefix: str
):
    '''
    Read the meter modbus data
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
        modbus_data.registers, byteorder=Endian.Big
    )
    accurrent = decoder.decode_16bit_int()
    accurrenta = decoder.decode_16bit_int()
    accurrentb = decoder.decode_16bit_int()
    accurrentc = decoder.decode_16bit_int()
    accurrentsf = decoder.decode_16bit_int()

    accurrent = tools.calculate_value(accurrent, accurrentsf)
    accurrenta = tools.calculate_value(accurrenta, accurrentsf)
    accurrentb = tools.calculate_value(accurrentb, accurrentsf)
    accurrentc = tools.calculate_value(accurrentc, accurrentsf)

    data[prefix +
         "accurrent"] = round(accurrent, abs(accurrentsf))
    data[prefix +
         "accurrenta"] = round(accurrenta, abs(accurrentsf))
    if env.THREE_PHASE:
        data[prefix +
             "accurrentb"] = round(accurrentb, abs(accurrentsf))
        data[prefix +
             "accurrentc"] = round(accurrentc, abs(accurrentsf))

    acvoltageln = decoder.decode_16bit_int()

    acvoltagean = decoder.decode_16bit_int()
    acvoltagebn = decoder.decode_16bit_int()
    acvoltagecn = decoder.decode_16bit_int()

    acvoltagell = decoder.decode_16bit_int()

    acvoltageab = decoder.decode_16bit_int()
    acvoltagebc = decoder.decode_16bit_int()
    acvoltageca = decoder.decode_16bit_int()
    acvoltagesf = decoder.decode_16bit_int()

    acvoltageln = tools.calculate_value(acvoltageln, acvoltagesf)
    acvoltagean = tools.calculate_value(acvoltagean, acvoltagesf)
    acvoltagebn = tools.calculate_value(acvoltagebn, acvoltagesf)
    acvoltagecn = tools.calculate_value(acvoltagecn, acvoltagesf)
    acvoltagell = tools.calculate_value(acvoltagell, acvoltagesf)
    acvoltageab = tools.calculate_value(acvoltageab, acvoltagesf)
    acvoltagebc = tools.calculate_value(acvoltagebc, acvoltagesf)
    acvoltageca = tools.calculate_value(acvoltageca, acvoltagesf)

    data[prefix +
         "acvoltageln"] = round(acvoltageln, abs(acvoltagesf))
    data[prefix +
         "acvoltagean"] = round(acvoltagean, abs(acvoltagesf))
    if env.THREE_PHASE:
        data[prefix +
             "acvoltagebn"] = round(acvoltagebn, abs(acvoltagesf))
        data[prefix +
             "acvoltagecn"] = round(acvoltagecn, abs(acvoltagesf))
        data[prefix +
             "acvoltagell"] = round(acvoltagell, abs(acvoltagesf))
        data[prefix +
             "acvoltageab"] = round(acvoltageab, abs(acvoltagesf))
        data[prefix +
             "acvoltagebc"] = round(acvoltagebc, abs(acvoltagesf))
        data[prefix +
             "acvoltageca"] = round(acvoltageca, abs(acvoltagesf))

    acfreq = decoder.decode_16bit_int()
    acfreqsf = decoder.decode_16bit_int()

    acfreq = tools.calculate_value(acfreq, acfreqsf)

    data[prefix + "acfreq"] = round(acfreq, abs(acfreqsf))

    acpower = decoder.decode_16bit_int()
    acpowera = decoder.decode_16bit_int()
    acpowerb = decoder.decode_16bit_int()
    acpowerc = decoder.decode_16bit_int()
    acpowersf = decoder.decode_16bit_int()

    acpower = tools.calculate_value(acpower, acpowersf)
    acpowera = tools.calculate_value(acpowera, acpowersf)
    acpowerb = tools.calculate_value(acpowerb, acpowersf)
    acpowerc = tools.calculate_value(acpowerc, acpowersf)

    data[prefix + "acpower"] = round(acpower, abs(acpowersf))
    data[prefix + "acpowera"] = round(acpowera, abs(acpowersf))
    if env.THREE_PHASE:
        data[prefix + "acpowerb"] = round(acpowerb, abs(acpowersf))
        data[prefix + "acpowerc"] = round(acpowerc, abs(acpowersf))

    acva = decoder.decode_16bit_int()
    acvaa = decoder.decode_16bit_int()
    acvab = decoder.decode_16bit_int()
    acvac = decoder.decode_16bit_int()
    acvasf = decoder.decode_16bit_int()

    acva = tools.calculate_value(acva, acvasf)
    acvaa = tools.calculate_value(acvaa, acvasf)
    acvab = tools.calculate_value(acvab, acvasf)
    acvac = tools.calculate_value(acvac, acvasf)

    data[prefix + "acva"] = round(acva, abs(acvasf))
    if env.THREE_PHASE:
        data[prefix + "acvaa"] = round(acvaa, abs(acvasf))
        data[prefix + "acvab"] = round(acvab, abs(acvasf))
        data[prefix + "acvac"] = round(acvac, abs(acvasf))

    acvar = decoder.decode_16bit_int()
    acvara = decoder.decode_16bit_int()
    acvarb = decoder.decode_16bit_int()
    acvarc = decoder.decode_16bit_int()
    acvarsf = decoder.decode_16bit_int()

    acvar = tools.calculate_value(acvar, acvarsf)
    acvara = tools.calculate_value(acvara, acvarsf)
    acvarb = tools.calculate_value(acvarb, acvarsf)
    acvarc = tools.calculate_value(acvarc, acvarsf)

    data[prefix + "acvar"] = round(acvar, abs(acvarsf))
    data[prefix + "acvara"] = round(acvara, abs(acvarsf))
    if env.THREE_PHASE:
        data[prefix + "acvarb"] = round(acvarb, abs(acvarsf))
        data[prefix + "acvarc"] = round(acvarc, abs(acvarsf))

    acpf = decoder.decode_16bit_int()
    acpfa = decoder.decode_16bit_int()
    acpfb = decoder.decode_16bit_int()
    acpfc = decoder.decode_16bit_int()
    acpfsf = decoder.decode_16bit_int()

    acpf = tools.calculate_value(acpf, acpfsf)
    acpfa = tools.calculate_value(acpfa, acpfsf)
    acpfb = tools.calculate_value(acpfb, acpfsf)
    acpfc = tools.calculate_value(acpfc, acpfsf)

    data[prefix + "acpf"] = round(acpf, abs(acpfsf))
    data[prefix + "acpfa"] = round(acpfa, abs(acpfsf))
    if env.THREE_PHASE:
        data[prefix + "acpfb"] = round(acpfb, abs(acpfsf))
        data[prefix + "acpfc"] = round(acpfc, abs(acpfsf))

    
    exporteda = decoder.decode_32bit_uint()
    exportedb = decoder.decode_32bit_uint()
    exportedc = decoder.decode_32bit_uint()
    
    importeda = decoder.decode_32bit_uint()
    importedb = decoder.decode_32bit_uint()
    importedc = decoder.decode_32bit_uint()
    energywsf = decoder.decode_16bit_int()

    # Exported
    exported = decoder.decode_32bit_uint()
    if exported < 0:
        exported = 0
    # exported = tools.validate(
    #     tools.calculate_value(exported, energywsf), ">", 0)

    # Imported
    imported = decoder.decode_32bit_uint()
    if imported < 0:
        imported = 0
    # imported = tools.validate(
    #     tools.calculate_value(imported, energywsf), ">", 0)


    exporteda = tools.calculate_value(exporteda, energywsf)
    exportedb = tools.calculate_value(exportedb, energywsf)
    exportedc = tools.calculate_value(exportedc, energywsf)

    importeda = tools.calculate_value(importeda, energywsf)
    importedb = tools.calculate_value(importedb, energywsf)
    importedc = tools.calculate_value(importedc, energywsf)

    data[prefix + "exported"] = round(exported * 0.001, 3)
    data[prefix + "exporteda"] = round(exporteda * 0.001, 3)
    if env.THREE_PHASE:
        data[prefix + "exportedb"] = round(exportedb * 0.001, 3)
        data[prefix + "exportedc"] = round(exportedc * 0.001, 3)
    data[prefix + "imported"] = round(imported * 0.001, 3)
    data[prefix + "importeda"] = round(importeda * 0.001, 3)
    if env.THREE_PHASE:
        data[prefix + "importedb"] = round(importedb * 0.001, 3)
        data[prefix + "importedc"] = round(importedc * 0.001, 3)

    exportedva = decoder.decode_32bit_uint()
    exportedvaa = decoder.decode_32bit_uint()
    exportedvab = decoder.decode_32bit_uint()
    exportedvac = decoder.decode_32bit_uint()
    importedva = decoder.decode_32bit_uint()
    importedvaa = decoder.decode_32bit_uint()
    importedvab = decoder.decode_32bit_uint()
    importedvac = decoder.decode_32bit_uint()
    energyvasf = decoder.decode_16bit_int()

    exportedva = tools.calculate_value(exportedva, energyvasf)
    exportedvaa = tools.calculate_value(exportedvaa, energyvasf)
    exportedvab = tools.calculate_value(exportedvab, energyvasf)
    exportedvac = tools.calculate_value(exportedvac, energyvasf)
    importedva = tools.calculate_value(importedva, energyvasf)
    importedvaa = tools.calculate_value(importedvaa, energyvasf)
    importedvab = tools.calculate_value(importedvab, energyvasf)
    importedvac = tools.calculate_value(importedvac, energyvasf)

    data[prefix +
         "exportedva"] = round(exportedva, abs(energyvasf))
    data[prefix +
         "exportedvaa"] = round(exportedvaa, abs(energyvasf))
    if env.THREE_PHASE:
        data[prefix +
             "exportedvab"] = round(exportedvab, abs(energyvasf))
        data[prefix +
             "exportedvac"] = round(exportedvac, abs(energyvasf))
    data[prefix +
         "importedva"] = round(importedva, abs(energyvasf))
    data[prefix +
         "importedvaa"] = round(importedvaa, abs(energyvasf))
    if env.THREE_PHASE:
        data[prefix +
             "importedvab"] = round(importedvab, abs(energyvasf))
        data[prefix +
             "importedvac"] = round(importedvac, abs(energyvasf))

    importvarhq1 = decoder.decode_32bit_uint()
    importvarhq1a = decoder.decode_32bit_uint()
    importvarhq1b = decoder.decode_32bit_uint()
    importvarhq1c = decoder.decode_32bit_uint()
    importvarhq2 = decoder.decode_32bit_uint()
    importvarhq2a = decoder.decode_32bit_uint()
    importvarhq2b = decoder.decode_32bit_uint()
    importvarhq2c = decoder.decode_32bit_uint()
    importvarhq3 = decoder.decode_32bit_uint()
    importvarhq3a = decoder.decode_32bit_uint()
    importvarhq3b = decoder.decode_32bit_uint()
    importvarhq3c = decoder.decode_32bit_uint()
    importvarhq4 = decoder.decode_32bit_uint()
    importvarhq4a = decoder.decode_32bit_uint()
    importvarhq4b = decoder.decode_32bit_uint()
    importvarhq4c = decoder.decode_32bit_uint()
    energyvarsf = decoder.decode_16bit_int()

    importvarhq1 = tools.calculate_value(importvarhq1, energyvarsf)
    importvarhq1a = tools.calculate_value(importvarhq1a, energyvarsf)
    importvarhq1b = tools.calculate_value(importvarhq1b, energyvarsf)
    importvarhq1c = tools.calculate_value(importvarhq1c, energyvarsf)
    importvarhq2 = tools.calculate_value(importvarhq2, energyvarsf)
    importvarhq2a = tools.calculate_value(importvarhq2a, energyvarsf)
    importvarhq2b = tools.calculate_value(importvarhq2b, energyvarsf)
    importvarhq2c = tools.calculate_value(importvarhq2c, energyvarsf)
    importvarhq3 = tools.calculate_value(importvarhq3, energyvarsf)
    importvarhq3a = tools.calculate_value(importvarhq3a, energyvarsf)
    importvarhq3b = tools.calculate_value(importvarhq3b, energyvarsf)
    importvarhq3c = tools.calculate_value(importvarhq3c, energyvarsf)
    importvarhq4 = tools.calculate_value(importvarhq4, energyvarsf)
    importvarhq4a = tools.calculate_value(importvarhq4a, energyvarsf)
    importvarhq4b = tools.calculate_value(importvarhq4b, energyvarsf)
    importvarhq4c = tools.calculate_value(importvarhq4c, energyvarsf)

    data[prefix +
         "importvarhq1"] = round(importvarhq1, abs(energyvarsf))
    data[prefix + "importvarhq1a"] = round(
        importvarhq1a, abs(energyvarsf)
    )
    if env.THREE_PHASE:
        data[prefix + "importvarhq1b"] = round(
            importvarhq1b, abs(energyvarsf)
        )
        data[prefix + "importvarhq1c"] = round(
            importvarhq1c, abs(energyvarsf)
        )
    data[prefix +
         "importvarhq2"] = round(importvarhq2, abs(energyvarsf))
    data[prefix + "importvarhq2a"] = round(
        importvarhq2a, abs(energyvarsf)
    )
    if env.THREE_PHASE:
        data[prefix + "importvarhq2b"] = round(
            importvarhq2b, abs(energyvarsf)
        )
        data[prefix + "importvarhq2c"] = round(
            importvarhq2c, abs(energyvarsf)
        )
    data[prefix +
         "importvarhq3"] = round(importvarhq3, abs(energyvarsf))
    data[prefix + "importvarhq3a"] = round(
        importvarhq3a, abs(energyvarsf)
    )
    if env.THREE_PHASE:
        data[prefix + "importvarhq3b"] = round(
            importvarhq3b, abs(energyvarsf)
        )
        data[prefix + "importvarhq3c"] = round(
            importvarhq3c, abs(energyvarsf)
        )
    data[prefix +
         "importvarhq4"] = round(importvarhq4, abs(energyvarsf))
    data[prefix + "importvarhq4a"] = round(
        importvarhq4a, abs(energyvarsf)
    )
    if env.THREE_PHASE:
        data[prefix + "importvarhq4b"] = round(
            importvarhq4b, abs(energyvarsf)
        )
        data[prefix + "importvarhq4c"] = round(
            importvarhq4c, abs(energyvarsf)
        )

    return (data)