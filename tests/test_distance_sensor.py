
"""
Tests unitaires pour la classe DistanceSensor.
Simulation (Mock) complète de RPi.GPIO et time.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

"""Mock de RPi.GPIO et time"""
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['time'] = __import__('time') 
"""on utilise le "vrai" module time,on le mock pas"""

from DistanceSensor import Distance_Sensor

class TestDistanceSensor(unittest.TestCase):
    def setUp(self):
        """Patch des fonctions GPIO et time"""
        self.gpio_patch = patch('RPi.GPIO')
        self.mock_gpio = self.gpio_patch.start()

        self.time_patch = patch('time.time')
        self.mock_time = self.time_patch.start()

        """Simule les timings d'entrée du capteur"""
        self.times = [1, 1.00001, 1.002, 1.00201]  # durée ≈ 2 ms
        self.mock_time.side_effect = self.times

        """Valeurs par défaut pour GPIO.input"""
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]

        """Création du capteur simulé"""
        self.sensor = Distance_Sensor(pinTrig=23, pinEcho=24, side="left")

    def tearDown(self):
        self.gpio_patch.stop()
        self.time_patch.stop()

    def test_read_value_valid(self):
        """Lecture correcte avec une durée valide"""
        result = self.sensor.read_value()
        self.assertAlmostEqual(result, 34.3, places=1)

    def test_read_value_timeout_start(self):
        """Timeout au début du signal (pas de changement à 1)"""
        self.mock_gpio.input.side_effect = [0] * 100
        self.mock_time.side_effect = [1 + i*0.001 for i in range(100)]
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_timeout_end(self):
        """Timeout à la fin du signal (pas de retour à 0)"""
        self.mock_gpio.input.side_effect = [0, 1] + [1]*100
        self.mock_time.side_effect = [1 + i*0.001 for i in range(102)]
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_out_of_bounds_low(self):
        """Distance trop courte (< 2 cm)"""
        self.mock_time.side_effect = [1, 1.00001, 1.00002, 1.00003]  # durée = 0.00002
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_read_value_out_of_bounds_high(self):
        """Distance trop longue (> 400 cm)"""
        self.mock_time.side_effect = [1, 1.00001, 1.1, 1.10001]  # durée ≈ 0.1s 
        result = self.sensor.read_value()
        self.assertIsNone(result)

    def test_side_property(self):
        """Vérifie la propriété 'side'"""
        self.assertEqual(self.sensor.side, "Left")

if __name__ == '__main__':
    unittest.main()
