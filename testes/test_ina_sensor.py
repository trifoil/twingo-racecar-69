import sys
from unittest.mock import MagicMock

"""Simulation des modules pour que les tests fonctionnent sur windwows"""
sys.modules['board'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()
sys.modules['adafruit_ina219.INA219'] = MagicMock()

from INASensor import INA_Sensor #Faut mettre le bon nom de fichier

import unittest
from unittest.mock import MagicMock, patch

class TestINASensor(unittest.TestCase):
    """ Classe de tests pour la classe INASensor
    qui testes les cas normaux, extrêmes et les erreurs potentielles """

    @patch('INASensor.adafruit_ina219.INA219')
    def test_read_value_normal(self, MockINA219):
        """ Test avec des valeurs normales """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = 12.3
        mock_sensor.shunt_voltage = 1500
        mock_sensor.current = 0.42
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor(("0x40", bus))
        result = sensor.read_value()

        expected = {
            "BusVoltage": 12.3,
            "ShuntVoltage": 1.5,
            "Current": 0.42
        }

        self.assertEqual(result, expected)

    @patch('INASensor.adafruit_ina219.INA219')
    def test_read_value_extreme(self, MockINA219):
        """ Test avec des valeurs extrêmes """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = 32.0
        mock_sensor.shunt_voltage = 5000
        mock_sensor.current = 3.0
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor(("0x40", bus))
        result = sensor.readValue()

        expected = {
            "BusVoltage": 32.0,
            "ShuntVoltage": 5.0,
            "Current": 3.0
        }

        self.assertEqual(result, expected)

    @patch('INASensor.adafruit_ina219.INA219')
    def test_read_value_none_values(self, MockINA219):
        """ Test si le capteur retourne None """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = None
        mock_sensor.shunt_voltage = None
        mock_sensor.current = None
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor(("0x40", bus))
        result = sensor.readValue()

        expected = {
            "BusVoltage": None,
            "ShuntVoltage": None,
            "Current": None
        }

        self.assertEqual(result, expected)

    @patch('INASensor.adafruit_ina219.INA219')
    def test_read_value_raises_exception(self, MockINA219):
        """ Test d’un capteur qui plante lors de la lecture, ex: problème matériel """
        mock_sensor = MagicMock()
        mock_sensor.bus_voltage = 12.0
        mock_sensor.shunt_voltage = 2000
        mock_sensor.current = MagicMock(side_effect=Exception("Sensor read error"))
        MockINA219.return_value = mock_sensor

        bus = MagicMock()
        sensor = INA_Sensor(("0x40", bus))

        with self.assertRaises(Exception):
            sensor.readValue()

    @patch('INASensor.adafruit_ina219.INA219')
    def test_invalid_i2c_address(self, MockINA219):
        """ Test d’une adresse I2C malformée, ex: chaîne invalide """
        with self.assertRaises(ValueError):
            sensor = INA_Sensor(("invalid_address", MagicMock()))

if __name__ == "__main__":
    unittest.main()
