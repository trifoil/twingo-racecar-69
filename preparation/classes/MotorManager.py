from preparation.classes.DCMotor import DCMotor
from classes.ServoMotor import ServoMotor
import adafruit_pca9685
import busio

class MotorManager():
    def __init__(self, i2c_bus:busio.I2C):
        self.__dcMotorsPropultion = [DCMotor(5, 17, 18), DCMotor(4, 27, 22)]
        self.__servoDirection = ServoMotor(0, 45)
        self.__i2c_bus = i2c_bus
        self.__pwmDriver = adafruit_pca9685.PCA9685(self.__i2c_bus)
        self.__pwmDriver.frequency = self.__servoDirection.frequency

    def setSpeed(self, speed:float) -> None:
        """
        Définit la vitesse des moteurs DC.
        
        :param speed: Valeur comprise entre -100 et 100.
                      Un signe négatif indique la marche arrière, positif la marche avant, 0 arret.
        """
        front = (speed >= 0)
        speed_value = abs(speed)
        
        dc_duty = int((speed_value / 100.0) * 65535)
        
        for motor in self.__dcMotorsPropultion:
            if speed_value == 0:
                motor.stop()
            else:
                motor.setDirection(front)
                self.__pwmDriver.channels[motor.pinEnable].duty_cycle = dc_duty

    def setAngle(self, steering:float) -> None:
        """
        Définit l'angle pour le servo de direction. :param steering: Pourcentage de braquage de -100 (pleine gauche) à 100 (pleine droite), 0(tout droit).
        """
        servo_duty = self.convert_steering_to_duty(steering)
        self.__pwmDriver.channels[self.__servoDirection.boardChannel].duty_cycle = servo_duty

    def initializeMotors(self) -> None:
        """
        Initialise les moteurs en mettant les moteurs DC à l'arrêt, et le servo au milieu
        """
        self.setAngle(0)

        for motor in self.__dcMotorsPropultion:
            motor.stop()
        

    def convert_steering_to_duty(self, steering: float) -> int:
        """
        Convertit un pourcentage de braquage (de -100 à 100) en une valeur duty_cycle (0 à 65535)
        pour un servo dont la plage mécanique est limitée autour du centre.
        
        Paramètres :
        - steering: pourcentage de braquage (-100 à 100)
        - center_angle: l'angle central du servo (en degrés), typiquement 90°.
        - range_deg: la déviation maximale par rapport au centre, ici 45°.
                    Cela signifie que -100% correspondra à center_angle - range_deg (90-45=45°)
                    et 100% à center_angle + range_deg (90+45=135°).
        - freq: fréquence du signal PWM (ex: 60 Hz)
        - min_pulse_ms: largeur d'impulsion minimale en ms (pour 0° dans le mapping complet, ex: 1.0 ms)
        - max_pulse_ms: largeur d'impulsion maximale en ms (pour 180° dans le mapping complet, ex: 2.0 ms)
        
        La fonction calcule d'abord la période du signal, détermine la plage de duty cycle
        pour le servo complet, puis extrait la valeur correspondant à l'angle effectif.
        
        :return: Valeur duty_cycle sur 16 bits (0 à 65535)
        """
        center_angle = self.__servoDirection.centerAngle
        range_deg = self.__servoDirection.rangeDegrees
        min_pulse_ms = self.__servoDirection.minPulse
        max_pulse_ms = self.__servoDirection.maxPulse
        freq = self.__servoDirection.frequency

        periode_ms = 1000.0 / freq  # ex: 1000/60 ≈ 16.67 ms
        
        t_min_duty = min_pulse_ms / periode_ms   # ex: ≈ 1.0/16.67 ≈ 0.06
        t_max_duty = max_pulse_ms / periode_ms   # ex: ≈ 2.0/16.67 ≈ 0.12
        
        normalized_angle = center_angle + (steering / 100.0) * range_deg
        
        duty_fraction = t_min_duty + (t_max_duty - t_min_duty) * (normalized_angle / 180.0)
        
        return int(duty_fraction * 65535)
        