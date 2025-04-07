from classes.Sensor import Sensor
import RPi.GPIO as GPIO

""" Implémente l'interface Sensor"""
class LineSensor(Sensor):
    def __init__(self,pinGPIO:int):
        self.__pinGPIO = pinGPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pinGPIO,GPIO.IN)

    def readValue(self) -> bool:
        """ Return 1 if line is detected, return 0 if not """
        return GPIO.input(self.__pinGPIO)

    """ Getter """
    @property
    def pinGPIO(self):
        return self.__pinGPIO