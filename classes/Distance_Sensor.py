import threading
import RPi.GPIO as GPIO
import time
from classes.Sensor import Sensor
from classes.Logging_Utils import Logging_Utils

class Distance_Sensor(Sensor):

    logger = Logging_Utils.get_logger()

    def __init__(self, pin_trig: int, pin_echo: int, side: str):
        self._pin_trig = pin_trig
        self._pin_echo = pin_echo
        self._side = side.capitalize()
        self._lock = threading.Lock()
        self._setup_gpio_once()
        
    def _setup_gpio_once(self):
        """Initialisation des broches (appelée une seule fois)"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_trig, GPIO.OUT)
        GPIO.setup(self._pin_echo, GPIO.IN)

    def read_value(self) -> float:
        with self._lock:
            try:
                GPIO.output(self._pin_trig, True)
                time.sleep(0.00001)
                GPIO.output(self._pin_trig, False)

                start_time = time.time()
                timeout = start_time + 0.05
                while GPIO.input(self._pin_echo) == 0:
                    start_time = time.time()
                    if start_time > timeout:
                        __class__.logger.warning("Début du signal trop long.")
                        raise TimeoutError("Début du signal trop long.")

                stop_time = time.time()
                timeout = stop_time + 0.05
                while GPIO.input(self._pin_echo) == 1:
                    stop_time = time.time()
                    if stop_time > timeout:
                        __class__.logger.warning("Fin du singla trop long")
                        raise TimeoutError("Fin du signal trop long.")

                duration = stop_time - start_time
                if duration <= 0:
                    __class__.logger.warning(f"Durée invalide: {duration}")
                    raise ValueError("Durée invalide.")
                
                distance = round(duration * 17150, 2)

                if distance < 2 or distance > 400:
                    __class__.logger.warning(f"Hors des limites de distance: {distance}cm")
                    raise ValueError(f"Hors limites : {distance} cm")
                
                __class__.logger.info(f"Lecture d'une valeur sur le capteur de distance: {distance}cm")
                return distance

            except Exception as e:
                return None

    @property
    def side(self):
        return self._side

# if __name__ == "__main__":
#     front_distance_test = Distance_Sensor(6,5,'front')
#     print(front_distance_test.read_value())
#     def show_1000_distances(capteur):
#         for _ in range(1000):
#             value = capteur.readValue()
#             if value is not None:
#                 print(f"{capteur.side}: {value} cm")
#             else:
#                 print(f"{capteur.side}: erreur de lecture")
#             time.sleep(0.05)  # pour éviter de spammer le capteur

#     # Init GPIO une seule fois
#     GPIO.setmode(GPIO.BCM)

#     # Crée les capteurs
#     capteurDroite = Distance_Sensor(23, 12, 'droite')
#     capteurGauche = Distance_Sensor(24, 16, 'gauche')
#     capteurDevant = Distance_Sensor(25, 20, 'devant')

#     # Crée les threads
#     threads = [
#         threading.Thread(target=_, ar_gs=(capteurDevant,)),
#         threading.Thread(target=_, ar_gs=(capteurGauche,)),
#         threading.Thread(target=_, ar_gs=(capteurDroite,))
#     ]

#     # Démarre les threads
#     for th in threads:
#         th.start()

#     # Attente
#     for th in threads:
#         th.join()

#     # Nettoyage des GPIO à la toute fin
#     GPIO.cleanup()
#     print("done")
