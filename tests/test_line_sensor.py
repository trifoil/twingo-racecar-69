import sys
from unittest import mock
import unittest


"""mock de RPi.GPIO"""
sys.modules['RPi'] = mock.Mock()
sys.modules['RPi.GPIO'] = mock.Mock()

import RPi.GPIO as GPIO
from classes.Line_Sensor import Line_Sensor

class TestLine_Sensor(unittest.TestCase):
    """ Classe de tests pour la classe Line_Sensor """
    def setUp(self):
        self.pin = 40
        self.sensor = Line_Sensor(self.pin)

    def test_read_value_high(self):
        """ Teste la méthode read_value() pour une valeur haute """
        GPIO.input.return_value = 1  
        """ Simule une ligne détectée """
        self.assertTrue(self.sensor.read_value())

    def test_read_value_low(self):
        """ Teste la méthode read_value() pour une valeur basse """
        GPIO.input.return_value = 0  
        """Simule absence de ligne"""
        self.assertFalse(self.sensor.read_value())

    def test_pin_getter(self):
        """ Teste le getter du pin """
        self.assertEqual(self.sensor.pin_gpio, self.pin)

if __name__ == '__main__':
    unittest.main()
