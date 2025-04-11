import sys
from unittest.mock import MagicMock, patch
import types



"""Créer un module dummy pour le package "RPi" s'il n'existe pas déjà"""

if "RPi" not in sys.modules:
    dummy_rpi = types.ModuleType("RPi")
    sys.modules["RPi"] = dummy_rpi
else:
    dummy_rpi = sys.modules["RPi"]

"""Créer un module dummy pour "RPi.GPIO"."""
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

""" Assigner dummy_gpio à RPi.GPIO et au package RPi """
dummy_rpi.GPIO = dummy_gpio
sys.modules["RPi.GPIO"] = dummy_gpio

""" Créer un module dummy pour "board". """
dummy_board = types.ModuleType("board")
dummy_board.SCL = "SCL"
dummy_board.SDA = "SDA"
sys.modules["board"] = dummy_board


from classes.INA_Sensor import INA_Sensor 

import unittest

class TestINA_Sensor(unittest.TestCase):
    """ Classe de tests pour la classe INA_Sensor
    qui testes les cas normaux, extrêmes et les erreurs potentielles """

    @patch('classes.INA_Sensor.adafruit_ina219.INA219')
    def test_read_value_normal(self, MockINA219):
        """ Test avec des valeurs normales """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = 12.3
        mock_sensor.shunt_voltage = 1.5
        mock_sensor.current = 0.42
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor((bus, 0x40))
        result = sensor.read_value()

        expected = {
            "BusVoltage": 12.3,
            "ShuntVoltage": 1.5,
            "Current": 0.42
        }

        self.assertEqual(result, expected)

    @patch('classes.INA_Sensor.adafruit_ina219.INA219')
    def test_read_value_extreme(self, MockINA219):
        """ Test avec des valeurs extrêmes """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = 32.0
        mock_sensor.shunt_voltage = 5.0
        mock_sensor.current = 3.0
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor((bus, 0x40))
        result = sensor.read_value()

        expected = {
            "BusVoltage": 32.0,
            "ShuntVoltage": 5.0,
            "Current": 3.0
        }

        self.assertEqual(result, expected)

    @patch('classes.INA_Sensor.adafruit_ina219.INA219')
    def test_read_value_none_values(self, MockINA219):
        """ Test si le capteur retourne None """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = None
        mock_sensor.shunt_voltage = None
        mock_sensor.current = None
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor((bus, 0x40))
        result = sensor.read_value()

        expected = {
            "BusVoltage": None,
            "ShuntVoltage": None,
            "Current": None
        }

        self.assertEqual(result, expected)

    # @patch('classes.INA_Sensor.adafruit_ina219.INA219')
    # def test_read_value_raises_exception(self, MockINA219):
    #     """ Test d’un capteur qui plante lors de la lecture, ex: problème matériel """
    #     mock_sensor = MagicMock()
    #     mock_sensor.bus_voltage = 12.0
    #     mock_sensor.shunt_voltage = 2.0
    #     mock_sensor.current = MagicMock(side_effect=Exception("Sensor read error"))
    #     MockINA219.return_value = mock_sensor

    #     bus = MagicMock()
    #     sensor = INA_Sensor((0x40, bus))

    #     with self.assertRaises(Exception):
    #         sensor.read_value()

    @patch('classes.INA_Sensor.adafruit_ina219.INA219')
    def test_invalid_i2c_address(self, MockINA219):
        """ Test d’une adresse I2C malformée, ex: chaîne invalide """
        with self.assertRaises(ValueError):
            sensor = INA_Sensor(("invalid_address", MagicMock()))

if __name__ == "__main__":
    unittest.main()
