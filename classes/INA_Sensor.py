"""
Classe qui va nous permettre d'envoyer les données nécessaires de l'INA sensor vers le sensor Manager.
Elle possède un constructeur et un méthode de read_value

Le constructeur ne fait que récupèrer l'i2c sous forme de tuples
"""


from classes.Logging_Utils import Logging_Utils
from classes.Sensor import Sensor
import busio
import board
import adafruit_ina219


class INA_Sensor(Sensor):

    logger = Logging_Utils.get_logger()

    def __init__(self, i2c:tuple):
        if not type(i2c[1]) == int:
            __class__.logger.critical("Le contructeur de la classe INS_Sensor a eut l'adresse i2c suivante: "+str(i2c[1]+"qui n'est pas un entier"))
            raise ValueError("Le type du tuple i2c[1] doit etre un entier, ici: "+str(type(i2c[1])))
        self._i2c_bus ,self._address = i2c
        self._sensor = adafruit_ina219.INA219(self._i2c_bus,self._address)

    def read_value(self) -> dict:
        """
        Retourne un dictionaire avec comme clef le nom à récupérer, courant, power, ...
        et en valeur, la valeur lue par le capteur.
        """
        __class__.logger.info(f"Lecture d'une valeur sur l'INA: BusVoltage: {self._sensor.bus_voltage}, ShuntVoltage: {self._sensor.shunt_voltage}, Courant: {self._sensor.current}")
        return {
            "BusVoltage" : self._sensor.bus_voltage,
            "ShuntVoltage" : self._sensor.shunt_voltage,
            "Current" : self._sensor.current
        }