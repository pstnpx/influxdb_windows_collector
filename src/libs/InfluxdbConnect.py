from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from config import INFLUXDB_HOST, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET
import datetime

class InfluxDBConnector:
    def __init__(self):
        self.__client = InfluxDBClient(
            url=INFLUXDB_HOST,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG)
        self.__write_api = self.__client.write_api(write_options=SYNCHRONOUS)

    def generatePoints(self, data: list) -> list:
        now = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        points = []
        for item in data:
            if item != "":
                point = {
                    "measurement": "pc_hwinfo",
                    "_time": now,
                    "tags" : { 
                        'HardwareType'  : item['HardwareType'],
                        'HardwareName'  : item['HardwareName'],
                        'Name'          : item['Name']
                    },
                    "fields": {
                        item['SensorType'] : float(item['Value'])
                    }
                }
                points.append(point)
        return points
    
    def sendData(self, data: list):
        points = self.generatePoints(data)
        self.__write_api.write(
            bucket=INFLUXDB_BUCKET, 
            record=points
        )