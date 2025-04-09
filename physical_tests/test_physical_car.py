import sys
import os
import busio
import board
import RPi.GPIO as GPIO
from unittest.mock import MagicMock, patch
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
""" Création d'un bus I2C et Import des classes"""
i2c = busio.I2C(board.SCL,board.SDA)
from classes.Motor_Manager import Motor_Manager
from classes.DC_Motor import DC_Motor
from classes.Servo_Motor import Servo_Motor
from classes.Distance_Sensor import Distance_Sensor
from classes.Line_Sensor import Line_Sensor
from classes.INA_Sensor import INA_Sensor
from classes.RGB_Sensor import RGB_Sensor
from classes.Sensor_Manager import Sensor_Manager
from classes.Car import Car
""" Instance de tous les capteurs et moteurs"""
front_distance_test = Distance_Sensor(6,5,'front')
left_distance_test = Distance_Sensor(11,9,'left')
right_distance_test = Distance_Sensor(26,19,'right')
line_sensor_test = Line_Sensor(20)
rgb_sensort_test = RGB_Sensor((i2c,0x29))
ina_sensor_test = INA_Sensor((i2c,0x44))
moteur1 = DC_Motor(4,17,18)
moteur2 = DC_Motor(5,27,22)
servo_test = Servo_Motor(0,50)

sensors = {
            "line_Sensor" : line_sensor_test,
            "dist_sensor_front" : front_distance_test,
            "dist_sensor_left" : left_distance_test,
            "dist_sensor_right" : right_distance_test,
            "rgb_sensor" : rgb_sensort_test,
            "ina_sensor" : ina_sensor_test
}

""" Instance des managers """
motor_manager = Motor_Manager([moteur1,moteur2],servo_test,(i2c,0x40))
sensor_manager = Sensor_Manager(sensors)
config = {
    "OBSTACLE_MINIMUM_DIST" : 10.0,
    "MAX_FRONT_DIST" : 10.0
}
TWINGO = Car("TWINGO", motor_manager, sensor_manager,config)
