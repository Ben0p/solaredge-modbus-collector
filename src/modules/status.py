from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from influxdb_client.rest import ApiException
from utils import const, tools, modbus



'''
Process the inverter status registers
'''



def read_modbus_data(
		ENV,
        client,
        address: int,
        slave: int
):
	'''
	Read the inverter modbus data
	'''
    
	data = {}
    
	if ENV.BATT_1:
		count = 0x12  # Read storedge block as well
	elif ENV.METER_1:
		count = 4  # Just read export control block
	else:
		return True  # Nothing to read here

	modbus_data = modbus.read_holding_registers(
        client=client,
        address=address,
        count=count,
        slave=slave
    )


	if not modbus_data.isError():
		decoder = BinaryPayloadDecoder.fromRegisters(
			modbus_data.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE
		)

		# 0xE000 - 1 - Export control mode
		export_control_mode = decoder.decode_16bit_uint() & 7
		if export_control_mode in const.EXPORT_CONTROL_MODE:
			data["export_control_mode"] = const.EXPORT_CONTROL_MODE[
				export_control_mode
			]
		else:
			#data["export_control_mode"] = export_control_mode
			print(f"{export_control_mode=}")

		# 0xE001 - 1 - Export control limit mode
		export_control_limit_mode = decoder.decode_16bit_uint() & 1
		if export_control_limit_mode in const.EXPORT_CONTROL_MODE:
			data["export_control_limit_mode"] = const.EXPORT_CONTROL_LIMIT_MODE[
				export_control_limit_mode
			]
		else:
			data["export_control_limit_mode"] = export_control_limit_mode

		# 0xE002 - 2 - Export control site limit
		data["export_control_site_limit"] = round(
			decoder.decode_32bit_float(), 3
		)

		if not ENV.BATT_1:
			# Done with the export control block
			return True

		# 0xE004 - 1 - storage control mode
		storage_control_mode = decoder.decode_16bit_uint()
		if storage_control_mode in const.STOREDGE_CONTROL_MODE:
			data["storage_contol_mode"] = const.STOREDGE_CONTROL_MODE[
				storage_control_mode
			]
		else:
			# data["storage_contol_mode"] = storage_control_mode
			print(f"{storage_control_mode=}")

		# 0xE005 - 1 - storage ac charge policy
		storage_ac_charge_policy = decoder.decode_16bit_uint()
		if storage_ac_charge_policy in const.STOREDGE_AC_CHARGE_POLICY:
			data["storage_ac_charge_policy"] = const.STOREDGE_AC_CHARGE_POLICY[
				storage_ac_charge_policy
			]
		else:
			# data["storage_ac_charge_policy"] = storage_ac_charge_policy
			print(f"{storage_ac_charge_policy=}")

		# 0xE006 - 2 - storage AC charge limit (kWh or %)
		data["storage_ac_charge_limit"] = round(
			decoder.decode_32bit_float(), 3
		)

		# 0xE008 - 2 - storage backup reserved capacity (%)
		data["storage_backup_reserved"] = round(
			decoder.decode_32bit_float(), 3
		)

		# 0xE00A - 1 - storage charge / discharge default mode
		storage_default_mode = decoder.decode_16bit_uint()
		if storage_default_mode in const.STOREDGE_CHARGE_DISCHARGE_MODE:
			data["storage_default_mode"] = const.STOREDGE_CHARGE_DISCHARGE_MODE[
				storage_default_mode
			]
		else:
			# data["storage_default_mode"] = storage_default_mode
			print(f"{storage_default_mode=}")

		# 0xE00B - 2- storage remote command timeout (seconds)
		data["storage_remote_command_timeout"] = decoder.decode_32bit_uint()

		# 0xE00D - 1 - storage remote command mode
		storage_remote_command_mode = decoder.decode_16bit_uint()
		if storage_remote_command_mode in const.STOREDGE_CHARGE_DISCHARGE_MODE:
			data[
				"storage_remote_command_mode"
			] = const.STOREDGE_CHARGE_DISCHARGE_MODE[storage_remote_command_mode]
		else:
			data["storage_remote_command_mode"] = storage_remote_command_mode
			print(f"{storage_remote_command_mode=}")

		if type(data["storage_remote_command_mode"]) == str:
			data["storage_remote_command_mode"] = None

		# 0xE00E - 2- storate remote charge limit
		data["storage_remote_charge_limit"] = round(
			decoder.decode_32bit_float(), 3
		)

		# 0xE010 - 2- storate remote discharge limit
		data["storage_remote_discharge_limit"] = round(
			decoder.decode_32bit_float(), 3
		)

	return data
