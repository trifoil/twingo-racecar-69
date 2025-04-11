""" Environnement de test pour tous les tests de la voiture """


"""
Le fichier Test_Car a pour but d'être le fichier de tests des fonctionnalités de Twingo_Race_Car.
Il doit comprendre l'intégralité des imports des classes utilisés dans la voiture.

Une partie des lignes nous servira à "simuler" des composants GPIO afin de permettre à l'interpreter de travailler.

Une partie en unitest sera implementé à la fin.
Elle comprendra un test unitaire par méthode présente sur Twingo_Race_Car et pour chacune de leur excpetions.
"""

# import sys
# import unittest
# from unittest.mock import MagicMock, patch


# """Stockage du chemin vers le dossier classes afin de pouvoir faire les import"""
# import os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# classes = os.path.join(current_dir, '..','classes')
# sys.path.insert(0, classes)

# """Liste complète des imports des classes qui seront utilisés"""

# from classes import Car

# """Mock de RPi.GPIO, time, board et busio, ils serviront de façon général et suffisent pour les moteurs"""
# sys.modules['RPi'] = MagicMock()
# sys.modules['RPi.GPIO'] = MagicMock()
# sys.modules['board'] = MagicMock()
# sys.modules['busio'] = MagicMock()
# sys.modules['time'] = __import__('time')
# """on utilise le "vrai" module time,on le mock pas"""

# """Simulation des modules des capteurs - ina219 (capteur courrant), TCS34725 (capteur rgb) - 
# pour que les tests fonctionnent sur windwows """
# sys.modules['adafruit_ina219'] = MagicMock()
# sys.modules['adafruit_ina219.INA219'] = MagicMock()
# sys.modules['adafruit_tcs34725'] = MagicMock()

# class Test_Car(unittest.TestCase):
#     def setUp(self):

#         self.i2c_mock = "???"

#         self.dc_motor_mock_1 = MagicMock()
#         self.dc_motor_mock_2 = MagicMock()
#         self.servo_motor_mock = MagicMock()

#         self.line_sensor_mock = MagicMock()
#         self.distance_sensor_front_mock = MagicMock()
#         self.distance_sensor_left_mock = MagicMock()
#         self.distance_sensor_right_mock = MagicMock()
#         self.rgb_sensor_mock = MagicMock()
#         self.ina_sensor_mock = MagicMock()

#         self.motor_manager_mock = Motor_Manager([self.dc_motor_mock_1,self.dc_motor_mock_2,self.servo_motor_mock],self.i2c_mock)

#         self.sensor_manager_mock = Sensor_Manager({"line_Sensor" : self.line_sensor_mock,
#             "dist_sensor_front" : self.distance_sensor_front_mock,
#             "dist_sensor_left" : self.distance_sensor_left_mock,
#             "dist_sensor_right" : self.distance_sensor_right_mock,
#             "rgb_sensor" : self.rgb_sensor_mock,
#             "ina_sensor" : self.ina_sensor_mock})

#         self.car = Car("Twingo Race Car", self.i2c_mock, self.sensor_manager_mock, self.motor_manager_mock)