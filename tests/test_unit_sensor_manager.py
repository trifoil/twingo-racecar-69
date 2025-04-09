"""
Tests unitaires pour la classe Sensor_Manager avec mock complet.
Compatible Windows (mock RPi.GPIO, board, busio, etc.).
"""

import sys
import unittest
from unittest.mock import MagicMock

"""MOCKS pour exécuter les tests sur Windows"""
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()

"""Imports après mock"""
from classes.Sensor_Manager import Sensor_Manager

class TestSensorManager(unittest.TestCase):
    def setUp(self):
        self.mock_line = MagicMock()
        self.mock_front = MagicMock()
        self.mock_left = MagicMock()
        self.mock_right = MagicMock()
        self.mock_rgb = MagicMock()
        self.mock_ina = MagicMock()

        self.sensors = {
            "line_Sensor": self.mock_line,
            "dist_sensor_front": self.mock_front,
            "dist_sensor_left": self.mock_left,
            "dist_sensor_right": self.mock_right,
            "rgb_sensor": self.mock_rgb,
            "ina_sensor": self.mock_ina,
        }

        self.manager = Sensor_Manager(self.sensors)

    def test_detect_line_true(self):
        self.mock_line.readValue.return_value = True
        self.assertTrue(self.manager.detect_line())

    def test_detect_line_stays_on_line(self):
        self.mock_line.readValue.side_effect = [True, True]
        self.manager.detect_line()
        self.assertFalse(self.manager.detect_line())

    def test_get_distance_average(self):
        self.mock_front.readValue.side_effect = [10, 12, 11, 9, 13]
        self.mock_left.readValue.side_effect = [20, 20, 20, 20, 20]
        self.mock_right.readValue.side_effect = [30, 32, 34, 36, 38]
        distances = self.manager.get_distance()
        self.assertEqual(distances, (11.0, 20.0, 34.0))

    def test_get_current_ok(self):
        self.mock_ina.readValue.return_value = {"Current": 0.42}
        self.assertEqual(self.manager.get_current(), 0.42)

    def test_get_current_error(self):
        self.mock_ina.readValue.side_effect = Exception("INA Error")
        self.assertIsNone(self.manager.get_current())

    def test_is_red_detected(self):
        self.mock_rgb.readValue.return_value = (250, 100, 50)
        self.assertTrue(self.manager.is_red(200, 100))

    def test_is_red_not_detected(self):
        self.mock_rgb.readValue.return_value = (180, 170, 100)
        self.assertFalse(self.manager.is_red(200, 20))

    def test_is_green_detected(self):
        self.mock_rgb.readValue.return_value = (80, 220, 60)
        self.assertTrue(self.manager.is_green(200, 100))

    def test_is_green_not_detected(self):
        self.mock_rgb.readValue.return_value = (180, 190, 60)
        self.assertFalse(self.manager.is_green(200, 20))

if __name__ == "__main__":
    unittest.main()
