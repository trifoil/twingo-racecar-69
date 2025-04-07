import sys
import types

# --- Injection de dummy modules pour RPi et board ---

# Créer un module dummy pour le package "RPi" s'il n'existe pas déjà
if "RPi" not in sys.modules:
    dummy_rpi = types.ModuleType("RPi")
    sys.modules["RPi"] = dummy_rpi
else:
    dummy_rpi = sys.modules["RPi"]

# Créer un module dummy pour "RPi.GPIO"
dummy_gpio = types.ModuleType("RPi.GPIO")
dummy_gpio.OUT = 1
dummy_gpio.IN = 0
dummy_gpio.BCM = "BCM"
dummy_gpio.BOARD = "BOARD"
dummy_gpio.setmode = lambda mode: None
dummy_gpio.setup = lambda pin, mode: None
dummy_gpio.input = lambda pin: 0
dummy_gpio.output = lambda pin, state: None
dummy_gpio.cleanup = lambda: None

# Assigner dummy_gpio à RPi.GPIO et au package RPi
dummy_rpi.GPIO = dummy_gpio
sys.modules["RPi.GPIO"] = dummy_gpio

# Créer un module dummy pour "board"
dummy_board = types.ModuleType("board")
dummy_board.SCL = "SCL"
dummy_board.SDA = "SDA"
sys.modules["board"] = dummy_board

# --- Fin des injections dummy ---

import unittest
from unittest.mock import patch, MagicMock
import threading
import time
import os

# Ajoute le dossier parent au path pour accéder aux modules dans "classes"
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.insert(0, parent_dir)

# --- Patch du constructeur de TCS34725 pour éviter l'initialisation matérielle ---
# On définit un dummy qui simule l'objet renvoyé par adafruit_tcs34725.TCS34725
class DummyTCS34725:
    def __init__(self, i2c_bus):
        self._i2c_bus = i2c_bus
    @property
    def color_rgb_bytes(self):
        # Retourne des valeurs par défaut (que vous pourrez modifier dans vos tests via des mocks)
        return (100, 50, 20)

# --- Import de SensorManager après avoir patché les modules matériels ---
from classes.SensorManager import SensorManager

class TestSensorManager(unittest.TestCase):
    def setUp(self):
        # Patch du constructeur de TCS34725 dans le module adafruit_tcs34725
        self.patcher_tcs = patch("adafruit_tcs34725.TCS34725", new=DummyTCS34725)
        self.addCleanup(self.patcher_tcs.stop)
        self.mock_tcs = self.patcher_tcs.start()

        # Création d'un bus fictif (le contenu n'est pas utilisé dans les tests)
        self.mock_bus = MagicMock()

        # Instanciation de SensorManager avec le bus mocké
        self.sm = SensorManager(self.mock_bus)
        
        # Remplacer les capteurs par des mocks pour pouvoir contrôler leurs retours
        self.sm._SensorManager__lineSensor = MagicMock(name="LineSensor")
        self.sm._SensorManager__distSensorFront = MagicMock(name="DistanceSensorFront")
        self.sm._SensorManager__distSensorLeft = MagicMock(name="DistanceSensorLeft")
        self.sm._SensorManager__distSensorRight = MagicMock(name="DistanceSensorRight")
        # Même si le RGBSensor est patché via DummyTCS34725, nous le remplaçons par un mock pour les tests
        self.sm._SensorManager__rgbSensor = MagicMock(name="RGBSensor")
        self.sm._SensorManager__inaSensor = MagicMock(name="INASensor")
        
        # Par défaut, on définit __isOnLine sur False
        self.sm._SensorManager__isOnLine = False

    # Tests pour detectLine()
    def test_detectLine_firstPassage(self):
        self.sm._SensorManager__lineSensor.readValue.return_value = True
        self.assertTrue(self.sm.detectLine())
        # Lorsque la ligne n'est plus détectée, la détection doit renvoyer False
        self.sm._SensorManager__lineSensor.readValue.return_value = False
        self.assertFalse(self.sm.detectLine())

    def test_detectLine_exception(self):
        self.sm._SensorManager__lineSensor.readValue.side_effect = Exception("Test exception")
        self.assertFalse(self.sm.detectLine())

    # Tests pour getDistance()
    def test_getDistance_all_valid(self):
        self.sm._SensorManager__distSensorFront.readValue.side_effect = [10, 10, 10, 10, 10]
        self.sm._SensorManager__distSensorLeft.readValue.side_effect = [20, 20, 20, 20, 20]
        self.sm._SensorManager__distSensorRight.readValue.side_effect = [30, 30, 30, 30, 30]
        distances = self.sm.getDistance()
        self.assertEqual(distances, (10.0, 20.0, 30.0))

    def test_getDistance_partial_failure(self):
        self.sm._SensorManager__distSensorFront.readValue.side_effect = [None, 10, 10, None, 10]
        self.sm._SensorManager__distSensorLeft.readValue.side_effect = [None, None, None, None, None]
        self.sm._SensorManager__distSensorRight.readValue.side_effect = [30, 30, 30, 30, 30]
        distances = self.sm.getDistance()
        self.assertEqual(distances, (10.0, None, 30.0))

    # Tests pour getCurrent()
    def test_getCurrent_valid(self):
        self.sm._SensorManager__inaSensor.readValue.return_value = {"Current": 1.23}
        self.assertEqual(self.sm.getCurrent(), 1.23)

    def test_getCurrent_exception(self):
        self.sm._SensorManager__inaSensor.readValue.side_effect = Exception("Test exception")
        self.assertIsNone(self.sm.getCurrent())

    # Tests pour isRed()
    def test_isRed_true(self):
        self.sm._SensorManager__rgbSensor.readValue.return_value = (100, 50, 20)
        self.assertTrue(self.sm.isRed(50, 20))

    def test_isRed_false_low_r(self):
        self.sm._SensorManager__rgbSensor.readValue.return_value = (40, 20, 20)
        self.assertFalse(self.sm.isRed(50, 20))

    def test_isRed_false_low_delta(self):
        self.sm._SensorManager__rgbSensor.readValue.return_value = (100, 90, 20)
        self.assertFalse(self.sm.isRed(50, 20))

    def test_isRed_exception(self):
        self.sm._SensorManager__rgbSensor.readValue.side_effect = Exception("Test exception")
        self.assertFalse(self.sm.isRed(50, 20))

    # Tests pour isGreen()
    def test_isGreen_true(self):
        self.sm._SensorManager__rgbSensor.readValue.return_value = (50, 100, 20)
        self.assertTrue(self.sm.isGreen(50, 20))

    def test_isGreen_false_low_g(self):
        self.sm._SensorManager__rgbSensor.readValue.return_value = (50, 40, 20)
        self.assertFalse(self.sm.isGreen(50, 20))

    def test_isGreen_false_low_delta(self):
        self.sm._SensorManager__rgbSensor.readValue.return_value = (90, 100, 20)
        self.assertFalse(self.sm.isGreen(50, 20))

    def test_isGreen_exception(self):
        self.sm._SensorManager__rgbSensor.readValue.side_effect = Exception("Test exception")
        self.assertFalse(self.sm.isGreen(50, 20))

if __name__ == '__main__':
    unittest.main()
