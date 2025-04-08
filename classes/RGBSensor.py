from classes.Sensor import Sensor
import adafruit_tcs34725
import busio
import board

"""
Bus à instancier, partagé par tous les composants i²C...
monbus = busio.I2C(board.SCL,board.SDA)
"""

class Rgb_Sensor(Sensor):
    def __init__(self, i2c:tuple):
        self._i2c_bus ,self._address = i2c
        self._sensor = adafruit_tcs34725.TCS34725(self._i2c_bus, self._address)
    
    def read_value(self):
        """ return un tuple de valeur (r,g,b) en entiers"""
        if self._sensor.color_rgb_bytes is None:
            raise ValueError("Erreur de lecture du capteur RGB")
        return self._sensor.color_rgb_bytes
        
