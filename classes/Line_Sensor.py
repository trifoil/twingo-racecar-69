from classes.Sensor import Sensor
import RPi.GPIO as GPIO

""" Implémente l'interface Sensor"""
class Line_Sensor(Sensor):
    def __init__(self,pin_gpio:int):
        self._pin_gpio = pin_gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_gpio,GPIO.IN)

    def read_value(self) -> bool:
        """ Return 1 if line is detected, return 0 if not """
        return GPIO.input(self._pin_gpio)

    """ Getter """
    @property
    def pin_gpio(self):
        """ Retourne le pin GPIO """
        return self._pin_gpio