import sys
import os
import busio
import board
import RPi.GPIO as GPIO
from unittest.mock import MagicMock, patch
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

i2c = busio.I2C(board.SCL,board.SDA)
from classes.Motor_Manager import Motor_Manager
from classes.DC_Motor import DC_Motor
from classes.Servo_Motor import Servo_Motor

moteur1 = DC_Motor(4,17,18)
moteur2 = DC_Motor(5,27,22)
servo_direction = Servo_Motor(8,20)
servo_test = Servo_Motor(15,90)
motor_manager = Motor_Manager([moteur1,moteur2],servo_test,(i2c,0x40))
motor_manager.set_speed(0)


def accl():
    for i in range(70,-1,-1):
        motor_manager.set_speed(i)
        sleep(0.05)
        print(i)
    for i in range(-70,1,1):
        motor_manager.set_speed(i)
        sleep(0.05)
        print(i)

accl()
motor_manager.set_angle(0)

# print("Démarrage moteur en direction avant")
# motor_manager.set_speed(1)
# sleep(3)
# motor_manager.set_speed(0)
# sleep(2)
# print("Démarrage moteur en direction arriere")
# motor_manager.set_speed(-1)
# sleep(3)
# motor_manager.set_speed(0)

# i = 100
# while i >=-100:
#     motor_manager.set_angle(i)
#     sleep(0.05)
#     i-=1