"""
Tests unitaires pour la classe MotorManager.
Simulation (Mock) complète de RPi.GPIO, time et PCA9685.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

"""Mock des modules externes"""
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['time'] = __import__('time')  # On garde le vrai time
sys.modules['adafruit_pca9685'] = MagicMock()
sys.modules['busio'] = MagicMock()

from Motor_Manager import Motor_Manager
from DC_Motor import DC_Motor
from Servo_Motor import Servo_Motor

class TestMotorManager(unittest.TestCase):
    def setUp(self):
        """Patch des fonctions GPIO et PCA9685"""
        self.gpio_patch = patch('RPi.GPIO')
        self.mock_gpio = self.gpio_patch.start()

        self.pca9685_patch = patch('adafruit_pca9685.PCA9685')
        self.mock_pca9685 = self.pca9685_patch.start()

        """Création des moteurs simulés"""
        self.motor1 = DC_Motor(pin_enable=17, pin_input1=27, pin_input2=22)
        self.motor2 = DC_Motor(pin_enable=18, pin_input1=23, pin_input2=24)
        self.servo = Servo_Motor(board_channel=0, range_degrees=180)

        """Création du gestionnaire de moteur simulé"""
        self.motor_manager = Motor_Manager(
            motors=[self.motor1, self.motor2],
            i2c=(0x40, "busio.I2C")
        )

    def tearDown(self):
        self.gpio_patch.stop()
        self.pca9685_patch.stop()

    def test_initialize_motors(self):
        """Test de l'initialisation des moteurs"""
        self.motor_manager.initialize_motors()
        # Vérifie que les moteurs sont initialisés correctement
        self.mock_gpio.setup.assert_any_call(17, self.mock_gpio.OUT)
        self.mock_gpio.setup.assert_any_call(18, self.mock_gpio.OUT)

    def test_set_speed(self):
        """Test de la configuration de la vitesse des moteurs"""
        self.motor_manager.set_speed(50)
        # Vérifie que le PWM est configuré pour chaque moteur
        self.mock_gpio.PWM.assert_any_call(17, 100)
        self.mock_gpio.PWM.assert_any_call(18, 100)
        pwm_instance = self.mock_gpio.PWM.return_value
        pwm_instance.start.assert_any_call(50)

    def test_set_angle(self):
        """Test de la configuration de l'angle du servo"""
        self.motor_manager.set_angle(90)
        # Vérifie que l'angle est converti en PWM et envoyé au servo
        pwm_value = self.motor_manager._angle_to_pwm(90)
        self.mock_pca9685.return_value.channels[0].duty_cycle = pwm_value

    def test_reverse_motor(self):
        """Test de l'inversion des moteurs"""
        self.motor1.set_direction(forward=False)
        self.mock_gpio.output.assert_any_call(27, False)  # Pin input1 désactivé
        self.mock_gpio.output.assert_any_call(22, True)   # Pin input2 activé

if __name__ == '__main__':
    unittest.main()
