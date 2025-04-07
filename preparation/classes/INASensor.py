from classes.I2CSensor import I2CSensor
import busio
import board
import adafruit_ina219
"""
Bus à instancier, partagé par tous les composants i²C...
monbus = busio.I2C(board.SCL,board.SDA)
"""

class INASensor(I2CSensor):
    def __init__(self, I2CAddress:str,i2c_bus:busio.I2C):
        super().__init__(I2CAddress,i2c_bus)
        self.__sensor = adafruit_ina219.INA219(self._i2c_bus)

    def readValue(self) -> dict:
        """
        Return un dictionaire avec comme clef le nom à récupérer, courant, power, ... et en valeur, la valeur lue par le capteur
        """
        return {
            "BusVolatage" : self.__sensor.bus_voltage,
            "Shunt Voltage" : self.__sensor.shunt_voltage/1000,
            "Current" : self.__sensor.current
        }