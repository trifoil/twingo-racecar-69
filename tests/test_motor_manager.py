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

from busio import I2C

class DummyPWMChannel:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self._duty_cycle = 0

    @property
    def duty_cycle(self):
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value: int):
        self._duty_cycle = value

class DummyPCA9685:
    def __init__(self, i2c_bus: I2C, *, address: int=0x40, reference_clock_speed: int=25000000):
        self.i2c = i2c_bus
        self.address = address
        self.reference_clock_speed = reference_clock_speed
        self.freqency = 0
        self.channels = [DummyPWMChannel(i) for i in range(16)]


# --- Import de SensorManager après avoir patché les modules matériels ---
from classes.Motor_Manager import Motor_Manager
from classes.DC_motor import DC_Motor
from classes.Servo_Motor import Servo_Motor


class Test_Motor_Manager(unittest.TestCase):

    motor_manager: Motor_Manager

    @patch("classes.Motor_Manager.PCA9685", new=DummyPCA9685)
    def test_creation_instance(self):
        self.__class__.motors = [MagicMock(spec=DC_Motor), MagicMock(spec=DC_Motor)]
        self.__class__.motors[0].pin_enable = 4
        self.__class__.motors[1].pin_enable = 5
        self.__class__.servo = MagicMock(spec=Servo_Motor)
        self.__class__.servo.freqency = 60
        self.__class__.servo.range_degrees = 45
        self.__class__.servo.min_pulse = 1.0
        self.__class__.servo.max_pulse = 2.0
        self.__class__.servo.initial_angle = 90
        self.__class__.servo.board_channel = 7
        self.__class__.i2c = MagicMock(spec=I2C)
        self.__class__.motor_manager = Motor_Manager(
            self.__class__.motors,
            self.__class__.servo,
            (self.__class__.i2c, 0x41))

    def test_set_speed_for_all_valid_positives(self):
        start = 1
        end = 100
        old_value = 1
        for i in range(start, end+1, 1):
            self.__class__.motor_manager.set_speed(i)
            for motor in self.__class__.motors:
                duty_cycle = self.__class__.motor_manager._pwm_driver.channels[motor.pin_enable].duty_cycle
                self.assertGreaterEqual(duty_cycle, old_value)
                self.assertGreaterEqual(duty_cycle, 1)
                self.assertGreaterEqual((2**16)-1, duty_cycle)
                old_value = duty_cycle

        for motor in self.__class__.motors:
            for args in motor.set_direction.call_args_list:
                self.assertEqual(args[0][0], True)
            motor.stop_free_wheels.assert_not_called()
            motor.reset_mock()


    def test_set_speed_for_all_valid_negatives(self):
        start = -100
        end = 0
        old_value = (2**16)-1
        for i in range(start, end, 1):
            self.__class__.motor_manager.set_speed(i)
            for motor in self.__class__.motors:
                duty_cycle = self.__class__.motor_manager._pwm_driver.channels[motor.pin_enable].duty_cycle
                self.assertGreaterEqual(old_value, duty_cycle)
                self.assertGreaterEqual(duty_cycle, 1)
                self.assertGreaterEqual((2**16)-1, duty_cycle)
                old_value = duty_cycle

        for motor in self.__class__.motors:
            for args in motor.set_direction.call_args_list:
                self.assertEqual(args[0][0], False)
            motor.stop_free_wheels.assert_not_called()
            motor.reset_mock()

    
    def test_set_speed_for_null_values(self):
        for motor in self.__class__.motors:
            self.__class__.motor_manager._pwm_driver.channels[motor.pin_enable].duty_cycle = 125
        self.__class__.motor_manager.set_speed(0)
        for motor in self.__class__.motors:
            self.assertEqual(self.__class__.motor_manager._pwm_driver.channels[motor.pin_enable].duty_cycle, 125)
            motor.set_direction.assert_not_called()
            motor.stop_free_wheels.assert_called_once_with()
            motor.reset_mock()


    def test_set_speed_for_out_of_range_values(self):
        values = [101, -101, 2000, -2000]
        for value in values:
            self.__class__.motor_manager.set_speed(value)
            for motor in self.__class__.motors:
                duty_cycle = self.__class__.motor_manager._pwm_driver.channels[motor.pin_enable].duty_cycle
                self.assertEqual((2**16)-1, duty_cycle)
                motor.reset_mock()


    def test_set_angle_all_valid_values(self):
        start = -100
        end = 100
        motor_manager = self.__class__.motor_manager
        for i in range(start, end, 1):
            motor_manager.set_angle(i)
            duty_cycle = motor_manager._pwm_driver.channels[motor_manager._servo_direction.board_channel].duty_cycle
            self.assertGreaterEqual((2**16)-1, duty_cycle)
            self.assertGreaterEqual(duty_cycle, 0)


if __name__ == "__main__":
    unittest.main()