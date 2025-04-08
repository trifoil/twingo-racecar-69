
"""
Tests unitaires pour la classe RGBSensor avec simulation complète (Mock) 
des modules hardware Adafruit (busio, board, adafruit_tcs34725).
Ces tests peuvent être lancés sur un ordinateur classique sans Raspberry Pi.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

""" Simulation (Mock) des modules matériels Adafruit avant import """
sys.modules['board'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()

from RGBSensor import RGB_Sensor

class TestRGBSensor(unittest.TestCase):
    def setUp(self):
        """
        Préparation du test : patch du module adafruit_tcs34725 pour simuler le capteur RGB.
        """
        patcher = patch('adafruit_tcs34725.TCS34725')
        self.mock_TCS34725 = patcher.start()
        self.addCleanup(patcher.stop)

        """Création d'un mock pour l'instance du capteur"""
        self.mock_sensor_instance = MagicMock()
        self.mock_TCS34725.return_value = self.mock_sensor_instance

        """Simulation du bus I2C et adresse I2C"""
        self.i2c_mock = ("0x29", MagicMock())
        self.sensor = RGB_Sensor(self.i2c_mock)

    def test_read_value_normal(self):
        """
        Test classique avec une valeur RGB simulée.
        """
        self.mock_sensor_instance.color_rgb_bytes = (100, 150, 200)
        result = self.sensor.read_value()
        self.assertEqual(result, (100, 150, 200))

    def test_read_value_zero(self):
        """
        Test des valeurs RGB à zéro.
        """
        self.mock_sensor_instance.color_rgb_bytes = (0, 0, 0)
        result = self.sensor.read_value()
        self.assertEqual(result, (0, 0, 0))

    def test_read_value_max(self):
        """
        Test des valeurs RGB au maximum (255, 255, 255).
        """
        self.mock_sensor_instance.color_rgb_bytes = (255, 255, 255)
        result = self.sensor.read_value()
        self.assertEqual(result, (255, 255, 255))

    def test_read_value_none(self):
        """
        Test si le capteur retourne None : le test doit lever une exception ou le gérer.
        """
        self.mock_sensor_instance.color_rgb_bytes = None
        with self.assertRaises(TypeError):
            self.sensor.read_value()

if __name__ == '__main__':
    unittest.main()
