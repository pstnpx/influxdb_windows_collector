import clr
from config import (
    SENSOR_TYPES, 
    COLLECT_CPU_DATA, 
    COLLECT_MB_DATA, 
    COLLECT_RAM_DATA, 
    COLLECT_FAN_DATA, 
    COLLECT_GPU_DATA, 
    COLLECT_HDD_DATA
)

# Load the OpenHardwareMonitorLib.dll file
clr.AddReference("OpenHardwareMonitorLib")

from OpenHardwareMonitor.Hardware import Computer, HardwareType, SensorType


class SystemCollector:

    def __init__(self):
        self.__result = None
        self.__computer = self.initialComputer()

    def getValue(self) -> list[dict]:
        self.__result = self.collect()
        return self.__result

    def collect(self) -> list[dict]:
        for hardware in self.__computer.Hardware:
            data = self.readSensor(hardware)
        return data

    def initialComputer(self):
        computer = Computer()

        computer.CPUEnabled         = COLLECT_CPU_DATA
        computer.MainboardEnabled   = COLLECT_MB_DATA
        computer.RAMEnabled         = COLLECT_RAM_DATA
        computer.FanControllerEnabled = COLLECT_FAN_DATA
        computer.GPUEnabled         = COLLECT_GPU_DATA
        computer.HDDEnabled         = COLLECT_HDD_DATA
        computer.Open()
        
        return computer
    
    def readSensor(self, hardware, data_list=[]):
        hardware.Update()
        for sensor in hardware.Sensors:
            if str(sensor.SensorType) in SENSOR_TYPES:
                data = {
                    'HardwareType'  : str(hardware.HardwareType),
                    'HardwareName'  : str(hardware.Name),
                    'Name'          : str(sensor.Name),
                    'Value'         : "{:.2f}".format(int(sensor.Value)),
                    'SensorType'    : str(sensor.SensorType)
                }
                data_list.append(data)
        for sub_hw in hardware.SubHardware:
            self.readSensor(sub_hw, data_list)
        return data_list