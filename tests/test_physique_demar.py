from Sensor_Manager import Sensor_Manager
from LineSensor import Line_Sensor
from DistanceSensor import Distance_Sensor
from RGBSensor import Rgb_Sensor
from INASensor import Ina_Sensor
from MotorManager import MotorManager
import time
import busio
import board

"""Initialisation des capteurs"""
line_sensor = Line_Sensor()
dist_sensor_front = Distance_Sensor("front")
dist_sensor_left = Distance_Sensor("left")
dist_sensor_right = Distance_Sensor("right")
rgb_sensor = Rgb_Sensor()
ina_sensor = Ina_Sensor()

sensors = {
    "line_Sensor": line_sensor,
    "dist_sensor_front": dist_sensor_front,
    "dist_sensor_left": dist_sensor_left,
    "dist_sensor_right": dist_sensor_right,
    "rgb_sensor": rgb_sensor,
    "ina_sensor": ina_sensor
}

"""Initialisation du gestionnaire de capteurs"""
sensor_manager = Sensor_Manager(sensors)

"""Initialisation du bus I2C pour les moteurs"""
i2c = busio.I2C(board.SCL, board.SDA)

"""Initialisation du gestionnaire de moteurs"""
motor_manager = MotorManager(i2c)

"""Initialisation des moteurs"""
print("Initialisation des moteurs...")
motor_manager.initializeMotors()

print("Démarrage du test des capteurs et des moteurs. Appuyez sur Ctrl+C pour arrêter.")
try:
    while True:
        """ Test des distances """
        distances = sensor_manager.get_distance()
        print(f"Distances (Front, Left, Right): {distances}")

        """ Test de la ligne """
        is_line_detected = sensor_manager.detect_line()
        print(f"Ligne détectée: {'Oui' if is_line_detected else 'Non'}")

        """ Test des couleurs """
        is_red_detected = sensor_manager.is_red(red_minimum=100, g_r_delta_minimum=50)
        is_green_detected = sensor_manager.is_green(green_minimum=100, g_r_delta_minimum=50)
        print(f"Rouge détecté: {'Oui' if is_red_detected else 'Non'}")
        print(f"Vert détecté: {'Oui' if is_green_detected else 'Non'}")

        """Test du courant"""
        current = sensor_manager.get_current()
        print(f"Courant mesuré: {current} A")

        """Test des moteurs DC"""
        print("Test des moteurs DC...")
        motor_manager.setSpeed(50)  # Avancer à 50% de la vitesse
        time.sleep(2)
        motor_manager.setSpeed(-50)  # Reculer à 50% de la vitesse
        time.sleep(2)
        motor_manager.setSpeed(0)  # Arrêt

        """Test du servo moteur"""
        print("Test du servo moteur...")
        motor_manager.setAngle(-50)  # Braquage à 50% gauche
        time.sleep(1)
        motor_manager.setAngle(50)  # Braquage à 50% droite
        time.sleep(1)
        motor_manager.setAngle(0)  # Tout droit

        """Pause pour éviter de saturer la console"""
        time.sleep(1)

except KeyboardInterrupt:
    print("Test des capteurs et des moteurs arrêté.")