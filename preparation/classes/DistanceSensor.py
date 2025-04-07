import threading
import RPi.GPIO as GPIO
import time
from classes.Sensor import Sensor


class DistanceSensor(Sensor):
    def __init__(self, pinTrig: int, pinEcho: int, side: str):
        self.__pinTrig = pinTrig
        self.__pinEcho = pinEcho
        self.__side = side.capitalize()
        self.__lock = threading.Lock()
        self.__setup_gpio_once()

    def __setup_gpio_once(self):
        """Initialisation des broches (appelée une seule fois)"""
        GPIO.setup(self.__pinTrig, GPIO.OUT)
        GPIO.setup(self.__pinEcho, GPIO.IN)

    def readValue(self) -> float:
        with self.__lock:
            try:
                GPIO.output(self.__pinTrig, True)
                time.sleep(0.00001)
                GPIO.output(self.__pinTrig, False)

                start_time = time.time()
                timeout = start_time + 0.05
                while GPIO.input(self.__pinEcho) == 0:
                    start_time = time.time()
                    if start_time > timeout:
                        raise TimeoutError("Début du signal trop long.")

                stop_time = time.time()
                timeout = stop_time + 0.05
                while GPIO.input(self.__pinEcho) == 1:
                    stop_time = time.time()
                    if stop_time > timeout:
                        raise TimeoutError("Fin du signal trop long.")

                duration = stop_time - start_time
                if duration <= 0:
                    raise ValueError("Durée invalide.")
                
                distance = round(duration * 17150, 2)

                if distance < 2 or distance > 400:
                    raise ValueError(f"Hors limites : {distance} cm")
                
                return distance

            except Exception as e:
                print(f"[{self.__side}] Erreur : {e}")
                return None

    @property
    def side(self):
        return self.__side

if __name__ == "__main__":
    def show1000distances(capteur):
        for _ in range(1000):
            value = capteur.readValue()
            if value is not None:
                print(f"{capteur.side}: {value} cm")
            else:
                print(f"{capteur.side}: erreur de lecture")
            time.sleep(0.05)  # pour éviter de spammer le capteur

    # Init GPIO une seule fois
    GPIO.setmode(GPIO.BCM)

    # Crée les capteurs
    capteurDroite = DistanceSensor(23, 12, 'droite')
    capteurGauche = DistanceSensor(24, 16, 'gauche')
    capteurDevant = DistanceSensor(25, 20, 'devant')

    # Crée les threads
    threads = [
        threading.Thread(target=show1000distances, args=(capteurDevant,)),
        threading.Thread(target=show1000distances, args=(capteurGauche,)),
        threading.Thread(target=show1000distances, args=(capteurDroite,))
    ]

    # Démarre les threads
    for th in threads:
        th.start()

    # Attente
    for th in threads:
        th.join()

    # Nettoyage des GPIO à la toute fin
    GPIO.cleanup()
    print("done")
