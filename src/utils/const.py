DEVICE_STATUSSES = {
    1: "Off",
    2: "Sleeping (auto-shutdown) – Night mode",
    3: "Grid Monitoring/wake-up",
    4: "Inverter is ON and producing power",
    5: "Production (curtailed)",
    6: "Shutting down",
    7: "Fault",
    8: "Maintenance/setup",
}

BATTERY_STATUSSES = {
    1: "Off",
    3: "Charging",
    4: "Discharging",
    6: "Idle",
    10: "Sleep"
}

EXPORT_CONTROL_MODE = {
    0: "Disabled",
    1: "Direct Export Limitation",
    2: "Indirect Export Limitation",
    4: "Production Limitation"
}

EXPORT_CONTROL_LIMIT_MODE = {
    0: "Total",
    1: "Per phase"
}

STOREDGE_CONTROL_MODE = {
    0: "Disabled",
    1: "Maximize Self Consumption",
    2: "Time of Use",
    3: "Backup Only",
    4: "Remote Control"
}

STOREDGE_AC_CHARGE_POLICY = {
    0: "Disabled",
    1: "Always Allowed",
    2: "Fixed Energy Limit",
    3: "Percent of Production",
}

STOREDGE_CHARGE_DISCHARGE_MODE = {
    0: "Off",
    1: "Charge from excess PV power only",
    2: "Charge from PV first",
    3: "Charge from PV and AC",
    4: "Maximize export",
    5: "Discharge to match load",
    7: "Maximize self consumption",
}

EXPORT_CONTROL_SELECT_TYPES = [
    ["Export control mode", "export_control_mode", 0xE000, EXPORT_CONTROL_MODE],
    ["Export control limit mode", "export_control_limit_mode", 0xE001, EXPORT_CONTROL_LIMIT_MODE],
]

EXPORT_CONTROL_NUMBER_TYPES = [
    ["Export control site limit", "export_control_site_limit", 0xE002, "f", {"min": 0, "max": 10000, "unit": "W"}],
]

STORAGE_SELECT_TYPES = [
    ["Storage Control Mode", "storage_contol_mode", 0xE004, STOREDGE_CONTROL_MODE],
    ["Storage AC Charge Policy", "storage_ac_charge_policy", 0xE005, STOREDGE_AC_CHARGE_POLICY],
    ["Storage Default Mode", "storage_default_mode", 0xE00A, STOREDGE_CHARGE_DISCHARGE_MODE],
    ["Storage Remote Command Mode", "storage_remote_command_mode", 0xE00D, STOREDGE_CHARGE_DISCHARGE_MODE],
]

# TODO Determine the maximum values properly
STORAGE_NUMBER_TYPES = [
    ["Storage AC Charge Limit", "storage_ac_charge_limit", 0xE006, "f", {"min": 0, "max": 100000000000}],
    ["Storage Backup reserved", "storage_backup_reserved", 0xE008, "f", {"min": 0, "max": 100, "unit": "%"}],
    ["Storage Remote Command Timeout", "storage_remote_command_timeout", 0xE00B, "i", {"min": 0, "max": 86400, "unit": "s"}],
    ["Storage Remote Charge Limit", "storage_remote_charge_limit", 0xE00E, "f", {"min": 0, "max": 20000, "unit": "W"}],
    ["Storage Remote Discharge Limit", "storage_remote_discharge_limit", 0xE010, "f", {"min": 0, "max": 20000, "unit": "W"}],
]