from classes.Sensor_Manager import Sensor_Manager
from classes.Motor_Manager import Motor_Manager
import busio
import board
import time

class Car:
    def __init__(self,car_name:str,motor_manager:Motor_Manager,sensor_manager:Sensor_Manager,const_config:dict):
        self._car_name = car_name
        print(f"""
Initialisation de la voiture : {self._car_name}
              """)
        self._sensor_manager = sensor_manager
        self._motor_manager = motor_manager
        self._total_laps = int(0)
        self._last_lap_duration = int(0)
        self._current_state = "stand_by"
        self._const_config = const_config
        print(f"""
{self._car_name} opérationel !
              """)

    def detect_obstacle(self,distances:tuple)->bool:
        """
        Detection d'un obstacle en face de la voiture, via vérification de la distance minimum de configuration de la voiture (exemple 10.0cm)
        Retourne Vrai si détecté
        Sinon retourne faux
        """
        front_disc,left_disc,right_disc = distances
        if (front_disc) < self._const_config["OBSTACLE_MINIMUM_DIST"]:
            return True
        return False
    
    def count_lap(self,detectedLine:bool) -> None:
        """
        Détection d'une ligne, si ligne detectée alors nombre de tour +1
        """
        if detectedLine:
            self._total_laps +=1
        print("NEW LAP")

    def start_car(self):
        self._current_state = "running"
    def stop_car(self):
        self._current_state = "stand_by"
        self._motor_manager.setSpeed(0)
        self._motor_manager.setAngle(0)
        print(f"""
{self._car_name} est arrêté.
              """)

    def calculate_next_move(self, distances: tuple, isLine: bool) -> tuple:
        """
        Calcule la décision en temps réel à partir des mesures des capteurs.
        
        Paramètres :
          - distances : un tuple (front, left, right) en cm
          - isLine    : booléen indiquant si la ligne est détectée (pour le comptage des tours)
        
        Renvoie :
          - (new_direction, new_speed) : le pourcentage de braquage (-100 à 100) et la vitesse en pourcentage (0 à 100)
          
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
        front_disc, left_disc, right_disc = distances
        obstacle = self.detect_obstacle(distances)
        time.sleep(0.01)
        try :
            if obstacle:
                if right_disc < 0:
                    raise ValueError("right_disc cannot be negative")
                if right_disc > 100:
                    right_disc = 100
                
                if right_disc < 10 :
                    new_direction = (10 - right_disc * 10)*-1
                    new_speed = 10 - right_disc * 10
                elif right_disc > 40 :
                    new_direction = 90
                    new_speed = 100
                elif right_disc > 10 :
                    new_direction = right_disc /2 
                    new_speed = 100
                else:
                    new_direction = 0
                    new_speed = 100
                return (new_direction, new_speed)
        except :
            pass
    

    def u_turn(self, direction: str) -> None:
        """
        Exécute un U-Turn en braquant à fond (gauche ou droite) pendant une durée donnée,
        à une vitesse spécifiée.

        Paramètres :
          - direction: 'left' ou 'right'
          - duration: durée du U-Turn en secondes
          - speed: vitesse en pourcentage (0 à 100) pendant le U-Turn
        """
        speed = 80
        if direction.lower() == 'left':
            turn_value = -100
        elif direction.lower() == 'right':
            turn_value = 100
        else:
            raise ValueError("La direction doit être 'left' ou 'right'")
        self._motor_manager.setAngle(turn_value)
        self._motor_manager.setSpeed(speed) 
        time.sleep(2.5)

        self._motor_manager.setSpeed(0)
        self._motor_manager.setAngle(0)

    def monitoring(self, distances: tuple, isLine: bool, direction: str, speed: float, ina: dict, rgb: tuple):
        """
        Affiche les données en temps réel pour le suivi de l'état de la voiture.

        Paramètres :
        - distances : un tuple (right, front, left) en cm
        - isLine    : booléen indiquant si la ligne est détectée
        - direction : direction actuelle de la voiture ('left' ou 'right')
        - speed     : vitesse de la voiture en pourcentage
        - ina       : un dictionnaire contenant les données du capteur INA (bus_voltage, shunt_voltage, current)
        - rgb       : un tuple contenant les valeurs RGB (0-255, 0-255, 0-255)
        """
        right_disc, front_disc, left_disc = distances

        # Affichage des données
        print(f"""
        ======= État actuel de la voiture : {self._car_name} =======
        Distance droite: {right_disc} cm
        Distance frontale: {front_disc} cm
        Distance gauche: {left_disc} cm
        Ligne détectée: {'Oui' if isLine else 'Non'}
        Direction: {direction}
        Vitesse: {speed} %

        === Données du capteur INA ===
        Bus Voltage: {ina['BusVoltage']} V
        Shunt Voltage: {ina['Shunt Voltage']} V
        Current: {ina['Current']} A

        === Couleur RGB ===
        R: {rgb[0]} G: {rgb[1]} B: {rgb[2]}

        ============================================================
        """)





    
