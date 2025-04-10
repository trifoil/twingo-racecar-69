from classes.Sensor import Sensor
import busio
import board
import adafruit_ina219
"""
Bus à instancier, partagé par tous les composants i²C...
monbus = busio.I2C(board.SCL,board.SDA)
"""

class INA_Sensor(Sensor):
    def __init__(self, i2c:tuple):
        if not type(i2c[1]) == int: 
            raise ValueError("Le type du tuple i2c[1] doit etre un entier, ici: "+str(type(i2c[1])))
        self._i2c_bus ,self._address = i2c
        self._sensor = adafruit_ina219.INA219(self._i2c_bus,self._address)

    def read_value(self) -> dict:
        """
        Return un dictionaire avec comme clef le nom à récupérer, courant, power, ... et en valeur, la valeur lue par le capteur
        """
        return {
            "BusVoltage" : self._sensor.bus_voltage,
            "ShuntVoltage" : self._sensor.shunt_voltage,
            "Current" : self._sensor.current
        }