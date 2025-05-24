import configparser
import logging

config = configparser.ConfigParser()
config.read('config.ini')

# INFLUXDB
INFLUXDB_HOST = config['INFLUXDB']['host']
INFLUXDB_TOKEN = config['INFLUXDB']['token']
INFLUXDB_ORG = config['INFLUXDB']['org']
INFLUXDB_BUCKET = config['INFLUXDB']['bucket']
POLLING_INTERVAL = int(config['INFLUXDB']['polling_interval'])

# LOGGING
LOG_FILENAME = config['LOGGING']['filename']
MAX_LOG_SIZE_BYTES = int(config['LOGGING']['max_size_mb']) * 1024 * 1024
BACKUP_COUNT = int(config['LOGGING']['backup_count'])
LOG_LEVEL = getattr(logging, config['LOGGING']['level'].upper(), logging.INFO)

# DATA COLLECTION FLAGS
COLLECT_CPU_DATA = config.getboolean('DATA_COLLECTION', 'cpu')
COLLECT_MB_DATA = config.getboolean('DATA_COLLECTION', 'motherboard')
COLLECT_RAM_DATA = config.getboolean('DATA_COLLECTION', 'ram')
COLLECT_FAN_DATA = config.getboolean('DATA_COLLECTION', 'fan')
COLLECT_GPU_DATA = config.getboolean('DATA_COLLECTION', 'gpu')
COLLECT_HDD_DATA = config.getboolean('DATA_COLLECTION', 'hdd')

# SENSOR TYPES (allowing multiple values)
VALID_SENSOR_TYPES = [
    "SmallData", "Load", "Fan", "Voltage", "Temperature",
    "Power", "Throughput", "Clock", "Data", "Control"
]
SENSOR_TYPES = [s.strip() for s in config['SENSOR']['types'].split(',') if s.strip()]

# Validate sensor types
invalid_sensors = [s for s in SENSOR_TYPES if s not in VALID_SENSOR_TYPES]
if invalid_sensors:
    raise ValueError(f"Invalid SENSOR_TYPE(s): {invalid_sensors}. Must be in {VALID_SENSOR_TYPES}")
