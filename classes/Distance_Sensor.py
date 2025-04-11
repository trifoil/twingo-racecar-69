"""
Classe Distance Sensor qui va nous permettre d'utiliser les sensor HC-SR04.
Le constructeur va comprendre les pins de trigger et d'échos et un str side qui nous permet de le nommer
afin de savoir quel côté le sensor regarde.
"""


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
        """
        méthode principale de la classe qui va nous permettre de récupèrer les données de distaces du capteurs
        Un try except est posé au début pour éviter la plupart des formes d'erreurs.
        On vérifie que les données retournées soit bien dans la range de distances captable par le capteurs
        et que le temps de réponse ne soit pas trop long sinon on raise une erreur.
        Si aucune erreur n'est détectées, on récupère la distance en cm.
        """
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


