from classes.SensorManager import SensorManager
from classes.MotorManager import MotorManager
import busio
import board
import time

class TwingoRaceCar:
    def __init__(self,name:str,i2c_bus:busio.I2C=busio.I2C(board.SCL,board.SDA)):
        self.__name = name
        print(f"""
Initialisation de la voiture : {self.__name}
              """)
        self.__sensorManager = SensorManager(i2c_bus)
        self.__motorManager = MotorManager(i2c_bus)
        self.__totalLaps = int
        self.__lastLapDuration = int
        self.__curentState = "standBy"
        self.__constConfig = {
            "OBSTACLE_MINIMUM_DIST" : 10.0
        }
        print(f"""
{self.__name} opérationel !
              """)

    def detectObstacle(self,distances:tuple)->bool:
        """
        Detection d'un obstacle en face de la voiture, via vérification de la distance minimum de configuration de la voiture (exemple 10.0cm)
        Retourne Vrai si détecté
        Sinon retourne faux
        """
        frontDist,leftDist,rightDist = distances
        if (frontDist) < self.__constConfig["OBSTACLE_MINIMUM_DIST"]:
            return True
        return False
    
    def countLap(self,detectedLine:bool) -> None:
        """
        Détection d'une ligne, si ligne detectée alors nombre de tour +1
        """
        if detectedLine:
            self.__totalLaps +=1
        print("NEW LAP")

    def startCar(self):
        pass
    def stopCar(self):
        pass

    def calculateNextMove(self, distances: tuple, isLine: bool) -> tuple:
        """
        Calcule la décision en temps réel à partir des mesures des capteurs.
        
        Paramètres :
          - distances : un tuple (front, left, right) en cm
          - isLine    : booléen indiquant si la ligne est détectée (pour le comptage des tours)
        
        Renvoie :
          - (newDirection, newSpeed) : le pourcentage de braquage (-100 à 100) et la vitesse en pourcentage (0 à 100)
          
        La logique :
          1. Si la distance frontale est inférieure au seuil, arrêt d'urgence.
          2. Calcul du braquage : 
             - On définit une erreur = (distance_droite - distance_gauche).
             - On applique un gain proportionnel pour obtenir un pourcentage de braquage.
          3. Calcul de la vitesse :
             - On fait une interpolation linéaire entre la distance minimale et une distance frontale max.
             - On réduit la vitesse si le braquage est important (pour plus de stabilité).
          4. Si la ligne est détectée, on incrémente le compteur de tours.
          5. On met à jour la direction et la vitesse via le motorManager.
        """
        frontDist, leftDist, rightDist = distances
        if frontDist is None or frontDist < self.__constConfig["OBSTACLE_MINIMUM_DIST"]:
            self.__motorManager.stopMotors()
            return (0, 0)

        Kp = 10  # facteur de gain (à ajuster par calibration)
        error = rightDist - leftDist  # Si positif, la voiture est plus proche du mur de gauche et doit tourner à droite.
        newDirection = max(-100, min(100, Kp * error))

        min_front = self.__constConfig["OBSTACLE_MINIMUM_DIST"]  
        max_front = self.__constConfig["MAX_FRONT_DIST"]
        newSpeed = (frontDist - min_front) / (max_front - min_front) * 100
        newSpeed = max(0, min(100, newSpeed))
        reduction_factor = 1 - (abs(newDirection) / 100) * 0.5  
        newSpeed = newSpeed * reduction_factor

        if isLine:
            self.countLap(isLine)

        self.__motorManager.setAngle(newDirection)
        self.__motorManager.setSpeed(newSpeed, newSpeed)

        return (newDirection, newSpeed)

    def u_turn(self, direction: str, duration: float, speed: float) -> None:
        """
        Exécute un U-Turn en braquant à fond (gauche ou droite) pendant une durée donnée,
        à une vitesse spécifiée.

        Paramètres :
          - direction: 'left' ou 'right'
          - duration: durée du U-Turn en secondes
          - speed: vitesse en pourcentage (0 à 100) pendant le U-Turn
        """
        if direction.lower() == 'left':
            turn_value = -100
        elif direction.lower() == 'right':
            turn_value = 100
        else:
            raise ValueError("La direction doit être 'left' ou 'right'")
        self.__motorManager.setAngle(turn_value)
        self.__motorManager.setSpeed(speed)
        time.sleep(duration)

        self.__motorManager.setSpeed(0)