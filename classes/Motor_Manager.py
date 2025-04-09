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
        self._dc_motors_propulsion = motors
        self._servo_direction = servo
        busio_i2c = i2c[0]
        i2c_addresse = i2c[1]
        self._pwm_driver = PCA9685(busio_i2c)
        self._pwm_driver.frequency = 50

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
        servo_duty = self._angle_to_pwm(int(new_angle))
        self._pwm_driver.channels[self._servo_direction.board_channel].duty_cycle = ((2**16)-1) - servo_duty


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
                channel = self._pwm_driver.channels[motor.pin_enable]
                channel.duty_cycle =65535 - int((safe_speed_percentage/100.0) * bits_16)


    def _range_value(self, value: int, min_val: int = -100, max_val: int = 100) -> int:
        """
        Limite une valeur entre min_val et max_val.
        :param value: la valeur à limiter
        :param min_val: la valeur minimale (par défaut -100)
        :param max_val: la valeur maximale (par défaut 100)
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

    def _angle_to_pwm(self,angle: int) -> int:
        center_angle = self._servo_direction.initial_angle
        range_deg = self._servo_direction.range_degrees
        min_pulse_ms = self._servo_direction.min_pulse
        max_pulse_ms = self._servo_direction.max_pulse
        freq = self._servo_direction.frequency

        periode_ms = 1000.0 / freq  # ex: 1000/60 ≈ 16.67 ms
        
        t_min_duty = min_pulse_ms / periode_ms   # ex: ≈ 1.0/16.67 ≈ 0.06
        t_max_duty = max_pulse_ms / periode_ms   # ex: ≈ 2.0/16.67 ≈ 0.12
        
        normalized_angle = center_angle + (angle / 100.0) * range_deg
        
        duty_fraction = t_min_duty + (t_max_duty - t_min_duty) * (normalized_angle / 180.0)
        
        return int(duty_fraction * 65535)