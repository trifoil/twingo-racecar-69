"""
Tests unitaires pour la classe Sensor_Manager avec mock complet.
"""

import sys
import unittest
from unittest.mock import MagicMock

"""MOCKS pour exécuter les tests independamment du code métier."""
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()
""" Imports après mock """
from classes.Sensor_Manager import Sensor_Manager


class TestSensorManager(unittest.TestCase):
    """ Tests unitaires pour la classe Sensor_Manager """

    def setUp(self):
        """ Initialisation des mocks pour les capteurs """
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
        """ Vérifie que detect_line retourne True si la ligne est détectée """
        self.mock_line.read_value.return_value = True
        self.assertTrue(self.manager.detect_line())

    def test_detect_line_stays_on_line(self):
        """ Vérifie que detect_line retourne False si la ligne est déjà détectée """
        self.mock_line.read_value.side_effect = [True, True]
        self.manager.detect_line()
        self.assertFalse(self.manager.detect_line())

    def test_get_distance_average(self):
        """ Vérifie le calcul de la moyenne des distances des capteurs """
        self.mock_front.read_value.side_effect = [10, 12, 11, 9, 13]
        self.mock_left.read_value.side_effect = [20, 20, 20, 20, 20]
        self.mock_right.read_value.side_effect = [30, 32, 34, 36, 38]
        distances = self.manager.get_distance()
        self.assertEqual(distances, (11.0, 20.0, 34.0))

    def test_get_current_ok(self):
        """ Vérifie que get_current retourne la valeur correcte """
        self.mock_ina.read_value.return_value = {"Current": 0.42}
        self.assertEqual(self.manager.get_current(), 0.42)

    def test_get_current_error(self):
        """ Vérifie que get_current retourne None en cas d'erreur """
        self.mock_ina.read_value.side_effect = Exception("INA Error")
        self.assertIsNone(self.manager.get_current())

    def test_is_red_detected(self):
        """ Vérifie que is_red détecte correctement une couleur rouge """
        self.mock_rgb.read_value.return_value = (250, 100, 50)
        self.assertTrue(self.manager.is_red(200, 100))

    def test_is_red_not_detected(self):
        """ Vérifie que is_red ne détecte pas une couleur non rouge """
        self.mock_rgb.read_value.return_value = (180, 170, 100)
        self.assertFalse(self.manager.is_red(200, 20))

    def test_is_green_detected(self):
        """ Vérifie que is_green détecte correctement une couleur verte """
        self.mock_rgb.read_value.return_value = (80, 220, 60)
        self.assertTrue(self.manager.is_green(200, 100))

    def test_is_green_not_detected(self):
        """ Vérifie que is_green ne détecte pas une couleur non verte """
        self.mock_rgb.read_value.return_value = (180, 190, 60)
        self.assertFalse(self.manager.is_green(200, 20))

    def test_get_distance_error(self):
        """ Vérifie que get_distance retourne None en cas d'erreur sur un capteur """
        self.mock_front.read_value.side_effect = Exception("Front sensor error")
        self.assertIsNone(self.manager.get_distance())

    def test_detect_line_no_line(self):
        """ Vérifie que detect_line retourne False si aucune ligne n'est détectée """
        self.mock_line.read_value.return_value = False
        self.assertFalse(self.manager.detect_line())

    def test_get_rgb_values(self):
        """ Vérifie que les valeurs RGB sont correctement retournées """
        self.mock_rgb.read_value.return_value = (100, 150, 200)
        self.assertEqual(self.manager.get_rgb_values(), (100, 150, 200))
        self.mock_front.read_value.side_effect = [10, 12, 11, 9, 13]
        self.mock_left.read_value.side_effect = [20, 20, 20, 20, 20]
        self.mock_right.read_value.side_effect = [30, 32, 34, 36, 38]
        distances = self.manager.get_distance()
        self.assertEqual(distances, (11.0, 20.0, 34.0))

    def test_get_current_ok(self):
        """ Vérifie que get_current retourne la valeur correcte """
        self.mock_ina.read_value.return_value = {"Current": 0.42}
        self.assertEqual(self.manager.get_current(), 0.42)

    def test_get_current_error(self):
        """ Vérifie que get_current retourne la bonne valeur en cas d'erreur """
        self.mock_ina.read_value.side_effect = Exception("INA Error")
        self.assertIsNone(self.manager.get_current())

    def test_is_red_detected(self):
        """ Vérifie que is_red détecte correctement une couleur rouge """
        self.mock_rgb.read_value.return_value = (250, 100, 50)
        self.assertTrue(self.manager.is_red(200, 100))

    def test_is_red_not_detected(self):
        """ Vérifie que is_red ne détecte pas une couleur non rouge """
        self.mock_rgb.read_value.return_value = (180, 170, 100)
        self.assertFalse(self.manager.is_red(200, 20))

    def test_is_green_detected(self):
        """ Vérifie que is_green détecte correctement une couleur verte """
        self.mock_rgb.read_value.return_value = (80, 220, 60)
        self.assertTrue(self.manager.is_green(200, 100))

    def test_is_green_not_detected(self):
        """ Vérifie que is_green ne détecte pas une couleur non verte """
        self.mock_rgb.read_value.return_value = (180, 190, 60)
        self.assertFalse(self.manager.is_green(200, 20))

if __name__ == "__main__":
    unittest.main()
