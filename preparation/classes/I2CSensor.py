from classes.Sensor import Sensor
from abc import abstractmethod
import busio
import board

"""
Bus à instancier, partagé par tous les composants i²C...
monbus = busio.I2C(board.SCL,board.SDA)
"""

class I2CSensor(Sensor):
    def __init__(self, I2CAddress:str,i2c_bus:busio.I2C):
        self._I2CAddress = I2CAddress
        self._i2c_bus = i2c_bus

    @abstractmethod
    def readValue(self):
        pass
   