import sys
import unittest
from unittest.mock import MagicMock, patch

""" Mock des modules matériels """
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['time'] = __import__('time')

from classes.Distance_Sensor import Distance_Sensor

# Disable Logging
from classes.Logging_Utils import Logging_Utils
Logging_Utils.setup_logging_in_main(verbose=False, write_file=False)

class TestDistanceSensor(unittest.TestCase):
    """" Tests unitaires pour la classe Distance_Sensor """
    def setUp(self):
        self.gpio_patch = patch('RPi.GPIO')
        self.mock_gpio = self.gpio_patch.start()

        self.time_patch = patch('time.time')
        self.mock_time = self.time_patch.start()

        self.sensor = Distance_Sensor(pin_trig=23, pin_echo=24, side="left")

    def tearDown(self):
        self.gpio_patch.stop()
        self.time_patch.stop()

    """def test_read_value_normal(self):
        #Distance normale dans les limites (exemple : 50 cm)
        # Simule un signal correspondant à 50 cm
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]  # Retourne 0 puis 1, puis 1, puis 0
        self.mock_time.side_effect = [1, 1.00001, 1.00004, 1.00007]  # Simule les timestamps
        result = self.sensor.read_value()
        self.assertEqual(result, 50.0) """

    def test_read_value_out_of_bounds_low(self):
        """Simule un signal correspondant à une distance trop courte"""
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]
        self.mock_time.side_effect = [1, 1.00001, 1.00002, 1.00003]
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_out_of_bounds_high(self):
        """ Simule un signal correspondant à une distance trop longue """
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]
        self.mock_time.side_effect = [1, 1.00001, 1.1, 1.10001]
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_timeout_start(self):
        """ Timeout lors du début du signal """
        self.mock_gpio.input.side_effect = [0, 0, 0, 0]
        self.mock_time.side_effect = [1, 1.06]  # Timeout après 0.05 s
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_timeout_end(self):
        """ Timeout lors de la fin du signal """
        self.mock_gpio.input.side_effect = [0, 1, 1, 1]
        self.mock_time.side_effect = [1, 1.00001, 1.06]  # Timeout après 0.05 s
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_invalid_duration(self):
        """ Durée invalide (durée négative ou nulle) """
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]
        self.mock_time.side_effect = [1, 1, 1, 1]  # Durée nulle
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_exception(self):
        """ Exception inattendue lors de la lecture """
        self.mock_gpio.input.side_effect = Exception("GPIO Error")
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_side_property(self):
        """ Vérifie que side retourne la bonne valeur capitalisée """
        self.assertEqual(self.sensor.side, "Left")

if __name__ == '__main__':
    unittest.main()
