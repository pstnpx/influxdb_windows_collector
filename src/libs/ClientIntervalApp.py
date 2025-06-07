import time
from utils.logger import create_log
from libs.SystemCollector import SystemCollector
from libs.InfluxdbConnect import InfluxDBConnector
from config import POLLING_INTERVAL, LOG_FILENAME, MAX_LOG_SIZE_BYTES, BACKUP_COUNT
import logging
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class ClientIntervalApp:
    def __init__(self):
        self.__logger = create_log(LOG_FILENAME, MAX_LOG_SIZE_BYTES, BACKUP_COUNT, logging.INFO)
        self.__system_collector = SystemCollector()
        self.__influxdb_connector = InfluxDBConnector()

    def run(self):
        self.__logger.info("-------- Collector app started ---------")
        if not is_admin():
            self.__logger.warning("This application is not running with admin privileges.")
            self.__logger.warning("Data will not collect properly without admin privileges.")
        last_cycle_start_time = time.time() 

        while True:
            next_expected_start_time = last_cycle_start_time + POLLING_INTERVAL
            timestart_processing = time.time()

            data = None
            try:
                data = self.__system_collector.getValue()
                self.__influxdb_connector.sendData(data)
                last_cycle_start_time = next_expected_start_time
                timeprocessed = time.time() - timestart_processing
                self.__logger.info(f"Done - Processed time = {timeprocessed:.3f}s")

            except Exception as e:
                self.__logger.exception("Exception error sending data to tsdb")
                last_cycle_start_time = next_expected_start_time
                if data:
                    self.__logger.error(f"Data that caused the error: {data}")

            finally:
                if data is not None:
                    data.clear()
                    del data

            time_to_sleep = next_expected_start_time - time.time()
            
            if time_to_sleep > 0:
                self.__logger.debug(
                    f"Sleeping for {time_to_sleep:.3f} seconds to meet polling interval of {POLLING_INTERVAL}s."
                )
                time.sleep(time_to_sleep)
            else:
                self.__logger.warning(f"Processing took {abs(time_to_sleep):.3f}s longer than POLLING_INTERVAL ({POLLING_INTERVAL}s). Skipping sleep.")
                last_cycle_start_time = time.time()
