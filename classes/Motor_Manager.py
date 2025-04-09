from classes.DC_motor import DC_Motor
from classes.Servo_Motor import Servo_Motor
from adafruit_pca9685 import PCA9685
import busio

class Motor_Manager():
    def __init__(self, motors: list[DC_Motor], servo: Servo_Motor, i2c: (int, busio.I2C)):
        """
        :param motors: liste des moteurs (généralement 2) utilisés pour la propulsion du véhicule  
        :param i2c: un tuple de deux éléments, le premier est l'adresse i2c et le second est une instance de busio.I2C  
        """
        self._dc_motors_propulsion: list[DC_Motor] = motors
        self._servo_direction: Servo_Motor = servo
        busio_i2c = i2c[0]
        i2c_addresse = i2c[1]
        self._pwm_driver: PCA9685 = PCA9685(busio_i2c)
        self._pwm_driver.frequency = self._servo_direction.frequency

    def set_speed(self, new_speed: int) -> None:
        """
        Définit la vitesse actuelle utilisée par tous les moteurs du gestionnaire.
        :param new_speed: la vitesse des moteurs en % de la vitesse maximale (entre -100 et 100)
        """
        is_going_forward = new_speed > 0
        speed_percentage = abs(new_speed)
        self._set_speed_with_percentage_and_if_its_going_forward(speed_percentage, is_going_forward)


    def set_angle(self, new_angle: int) -> None:
        """
        Définit l’angle de rotation actuel des roues utilisées par le gestionnaire.
        :param new_angle: l’angle de rotation en pourcentage de l’angle maximal (entre -100 % et 100 %)
        """
        servo_duty = self._angle_to_pwm(new_angle)
        pca_channel = self._pwm_driver.channels[self._servo_direction.board_channel]
        pca_channel.duty_cycle = servo_duty


    def initialize_motors(self) -> None:
        """
        Initialise tous les moteurs en réglant leur angle à 0° et en les arrêtant.
        """
        self.set_angle(0)
        self.set_speed(0)


    def _set_speed_with_percentage_and_if_its_going_forward(self, speed_percentage: int, is_going_forward: bool) -> None:
        """
        Définit la vitesse actuelle utilisée par tous les moteurs du gestionnaire avec un pourcentage de vitesse et une condition pour savoir si c'est en avant ou en arrière.
        :param speed_percentage: la vitesse à laquelle les roues doivent aller dans une certaine direction
        :param is_going_forward: si les roues doivent aller en avant (vrai) ou en arrière (faux)
        """
        bits_16 = (2 ** 16)-1
        safe_speed_percentage = self._range_value(speed_percentage)
        for motor in self._dc_motors_propulsion:
            if safe_speed_percentage == 0:
                motor.stop_free_wheels()
            else:
                motor.set_direction(is_going_forward)
                pwm_16_bits = (safe_speed_percentage/100.0) * bits_16
                channel = self._pwm_driver.channels[motor.pin_enable]
                channel.duty_cycle = int((safe_speed_percentage/100.0) * bits_16)


    def _range_value(self, value: int, min: int =-100, max: int = 100):
        """
        Limite une valeur entre une valeur 'min' et une valeur 'max'. Si la valeur est inférieure à 'min', elle sera renvoyée.
        :param value: la valeur à limiter
        :param min: la valeur minimale de la plage
        :param max: la valeur maximale de la plage
        """
        assert isinstance(value, int) 
        assert isinstance(min, int)
        assert isinstance(max, int)
        assert min <= max
        
        if (value < min):
            return min
        elif (value > max):
            return max
        else:
            return value


    def _angle_to_pwm(self, angle: int) -> int:
        """
        Convertit un angle de direction en PWM sur 16 bits.
        :param angle: l'angle en % de -100.0 à 100.0
        """
        bits_16 = (2 ** 16)-1
        servo = self._servo_direction
        period_ms = 1000.0 / servo.freqency
        
        min_duty = servo.min_pulse / period_ms
        max_duty = servo.max_pulse / period_ms

        normalized_angle = servo.initial_angle + (angle / 100.0) * servo.range_degrees

        duty_fraction = min_duty + (max_duty - min_duty) * (normalized_angle / 180.0)

        return int(duty_fraction * bits_16)