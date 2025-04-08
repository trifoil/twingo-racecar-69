import sys
from unittest import mock
import unittest


"""mock de RPi.GPIO"""
sys.modules['RPi'] = mock.Mock()
sys.modules['RPi.GPIO'] = mock.Mock()

import RPi.GPIO as GPIO
from LineSensor import LineSensor

class TestLineSensor(unittest.TestCase):
    def setUp(self):
        self.pin = 40
        self.sensor = LineSensor(self.pin)

    def test_read_value_high(self):
        GPIO.input.return_value = 1  
        """ Simule une ligne détectée """
        self.assertTrue(self.sensor.readValue())

    def test_read_value_low(self):
        GPIO.input.return_value = 0  
        """Simule absence de ligne"""
        self.assertFalse(self.sensor.readValue())

    def test_pin_getter(self):
        self.assertEqual(self.sensor.pinGPIO, self.pin)

if __name__ == '__main__':
    unittest.main()
