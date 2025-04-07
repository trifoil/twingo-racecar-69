from classes.I2CSensor import I2CSensor
import adafruit_tcs34725
import busio
import board

"""
Bus à instancier, partagé par tous les composants i²C...
monbus = busio.I2C(board.SCL,board.SDA)
"""

class RGBSensor(I2CSensor):
    def __init__(self, I2CAddress:str, i2c_bus:busio.I2C):
        super().__init__(I2CAddress, i2c_bus)
        self.__sensor = adafruit_tcs34725.TCS34725(self._i2c_bus)
    
    def readValue(self):
        """ return un tuple de valeur (r,g,b) en entiers"""
        return self.__sensor.color_rgb_bytes
        
