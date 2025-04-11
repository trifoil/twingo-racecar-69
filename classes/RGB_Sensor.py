"""
Classe qui va nous permettre de récupèrer les informations du RGB sensor afin de les utiliser dans le
Sensor Manager.

Son constructeur n'a besoin d'aucun attribut autre que les données du bus I²C.

Il possède une méthode pour récupèrer les informations qu'il capte et les retourne dans un tuple de données
rgb
"""


from classes.Sensor import Sensor
import adafruit_tcs34725
import busio
import board
from classes.Logging_Utils import Logging_Utils

"""
Bus à instancier, partagé par tous les composants i²C...
monbus = busio.I2C(board.SCL,board.SDA)
"""

class RGB_Sensor(Sensor):

    logger = Logging_Utils.get_logger()

    def __init__(self, i2c:tuple):
        self._i2c_bus ,self._address = i2c
        self._sensor = adafruit_tcs34725.TCS34725(self._i2c_bus, self._address)
    
    def read_value(self):
        """ return un tuple de valeur (r,g,b) en entiers"""
        if self._sensor.color_rgb_bytes is None:
            __class__.logger.critical("Erreur de lecture du capteur RBG!")
            raise ValueError("Erreur de lecture du capteur RGB")
        __class__.logger.info("Lecture d'une valeur sur le capteur RGB. Valeur: "+str(self._sensor.color_rgb_bytes))
        return self._sensor.color_rgb_bytes
        
