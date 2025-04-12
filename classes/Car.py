from classes.Sensor_Manager import Sensor_Manager
from classes.Motor_Manager import Motor_Manager
from classes.Config import Config
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
        self._last_lap_duration = []
        self._current_state = "stand_by"
        self._const_config = const_config
        self._target_lap = 0
        self._last_move = None
        self._last_error = None
        print(f"""
{self._car_name} opérationel !
              """)

        try:
            """ Récupération de la configuration actuelle, si le fichier est présent alors le module était en cours d'exécution et un problème est survenu """
            self._config = Config.load_from_json("current_config.json")
            self._total_laps = self._config.laps_elapsed
            self._target_lap = self._config.laps_total
            self._last_lap_duration = self._config.lap_start_timestamps
            if self._config.should_be_running:
                self._current_state = "racing"
                print(f"""Récupération de la configuration actuelle : {self._car_name} était en cours d'exécution""")
            
        except FileNotFoundError:
            """ Si le fichier n'est pas présent, alors la voiture n'était pas en cours d'exécution, et on crée un nouveau fichier de configuration actuel """
            self._config = Config()
            self._config.set_attributes(should_be_running=False, laps_elapsed=0, laps_total=0, lap_start_timestamps=[])
            self._config.save_to_json("current_config.json")

    def detect_obstacle(self,distances:tuple)->bool:
        """
        Detection d'un obstacle en face de la voiture, via vérification de la distance minimum de configuration de la voiture (exemple 10.0cm)
        Retourne Vrai si détecté
        Sinon retourne faux
        """
        obstacle = False
        front, left, right = distances

        try:
            if front < 20.0:
                obstacle = True
                print("Detected Front")
                while obstacle:
                    
                    front, left, right = self._sensor_manager.get_distance()
                    try :
                        if left > right:
                            self._motor_manager.set_angle(-100)
                            self._motor_manager.set_speed(-60)
                            print("OBSTABLE LEFT>RIGHT")
                        elif right > left:
                            self._motor_manager.set_angle(100)
                            self._motor_manager.set_speed(-60)
                            print("OBSTABLE RIGHT>LEFT")
                    except TypeError :
                        self._motor_manager.set_angle(-100)
                        self._motor_manager.set_speed(-60)

                    if front > 20.0:
                        obstacle = False
                        return obstacle

        except Exception as e:
            print(f"Un erreur est survenue : {e}")

    def count_lap(self,detectedLine:bool) -> None:
        """
        Détection d'une ligne, si ligne detectée alors nombre de tour +1 et sauvegarde de la configuration actuelle
        """
        if detectedLine:
            self._total_laps +=1
            self._config.add_lap()
            self._config.save_to_json("current_config.json")

        print("NEW LAP")

    def start_car(self, mode:str) -> None:
        """ Au démarrage de la voiture, on initialise le mode de conduite et on sauvegarde la configuration actuelle """
        self._current_state = mode
        self._config.add_lap_timestamp()
        self._config.set_attributes(should_be_running=True)
        self._config.save_to_json("current_config.json")

    def stop_car(self):
        """ Arrêt de la voiture, on sauvegarde la configuration actuelle et on remet les moteurs à 0 et les tours à 0 """
        self._current_state = "stand_by"
        self._motor_manager.set_speed(0)
        self._motor_manager.set_angle(0)
        self._target_lap = 0
        self._total_laps = 0
        self._last_lap_duration = []
        self._config.set_attributes(should_be_running=False, laps_elapsed=0, laps_total=0, lap_start_timestamps=[])
        self._config.save_to_json("current_config.json")
        print(f"""
{self._car_name} est arrêté.
              """)

    def calculate_next_move(self, distances: tuple) -> tuple:
        """
        Calcule l'angle de braquage et la vitesse à appliquer en fonction des distances mesurées.

        Parameters:
            distances (tuple): Un triplet (frontDist, leftDist, rightDist) représentant respectivement
                            la distance à l'obstacle devant, à gauche et à droite. Chaque valeur
                            peut être un nombre (en cm) ou None si la mesure est indisponible.

        Returns:
            tuple: Un tuple (angle, speed), où `angle` est un entier entre -100 (braquage max à gauche)
                et 100 (braquage max à droite), et `speed` est la vitesse à appliquer (négative si
                marche arrière, positive sinon).
        """
        frontDist, leftDist, rightDist = distances

        min_front = 10
        hysteresis_margin = 10
        slow_front = 60
        max_front = 70

        Kp = 6
        min_speed = 21
        max_speed = 28
        reverse_speed = -25
        reverse_angle = 45

        if not hasattr(self, "_is_backing_up"):
            self._is_backing_up = False

        if self._is_backing_up:
            if frontDist is not None and frontDist > (min_front + hysteresis_margin):
                self._is_backing_up = False
            else:
                angle_to_apply = 0
                if leftDist is None and rightDist is not None:
                    angle_to_apply = reverse_angle
                elif rightDist is None and leftDist is not None:
                    angle_to_apply = -reverse_angle
                elif leftDist is not None and rightDist is not None:
                    if leftDist < rightDist:
                        angle_to_apply = reverse_angle
                    else:
                        angle_to_apply = -reverse_angle
                return (angle_to_apply, reverse_speed)

        if frontDist is None and (leftDist is None or rightDist is None):
            return (0, 0)

        if frontDist is not None and frontDist < min_front:
            self._is_backing_up = True
            angle_to_apply = 0
            if leftDist is None and rightDist is not None:
                angle_to_apply = reverse_angle
            elif rightDist is None and leftDist is not None:
                angle_to_apply = -reverse_angle
            elif leftDist is not None and rightDist is not None:
                if leftDist < rightDist:
                    angle_to_apply = reverse_angle
                else:
                    angle_to_apply = -reverse_angle
            return (angle_to_apply, reverse_speed)

        if leftDist is None and rightDist is None:
            return (0, min_speed)
        elif leftDist is None:
            error = 1
        elif rightDist is None:
            error = -1
        else:
            error = rightDist - leftDist

        newAngle = max(-100, min(100, Kp * error))

        try:
            rawSpeed = (frontDist - slow_front) / (max_front - slow_front) * 100
        except ZeroDivisionError:
            rawSpeed = 50

        rawSpeed = max(min_speed, min(max_speed, rawSpeed))

        correctionFactor = 1 - (abs(newAngle) / 100) * 0.5
        newSpeed = max(min_speed, rawSpeed * correctionFactor)
        newSpeed = min(newSpeed, max_speed)

        return (newAngle, newSpeed)


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
            speed = 50
        else:
            raise ValueError("La direction doit être 'left' ou 'right'")


        self._motor_manager.set_angle(turn_value)
        self._motor_manager.set_speed(speed) 
        time.sleep(2.4)


        self._motor_manager.set_speed(0)
        self._motor_manager.set_angle(0)

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
        front_disc, left_disc,right_disc = distances

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
        Shunt Voltage: {ina['ShuntVoltage']} V
        Current: {ina['Current']} A

        === Couleur RGB ===
        R: {rgb[0]} G: {rgb[1]} B: {rgb[2]}

        ============================================================
        """)


    def post(self) -> bool:
        """ 
        Fonction au démarrage de la voiture : effectue un test physique des capteurs et des moteurs
        Vérifie que chaque capteur renvoie une valeur valide ( diférent de None) et que les moteurs répondent correctement
         Retourne True si tout est fonctionnel, sinon False.
        """
        print("\n===== POST -> Lancement du test physique =====")

        try:
            """Test capteurs de distance"""
            print("POST -> Test des capteurs de distance")
            distances = self._sensor_manager.get_distance()
            print(f"POST -> Distances (Front, Left, Right): {distances}")
            if any(d is None for d in distances):
                print("POST -> Capteur(s) de distance non fonctionnel(s)")
                pass 

            """ Test capteur de ligne """
            is_line = self._sensor_manager.detect_line()
            print(f"POST -> Ligne détectée : {'Oui' if is_line else 'Non'}")

            """ Test capteur RGB """
            print("POST -> Test du capteur RGB")
            is_red = self._sensor_manager.is_red(red_minimum=100, g_r_delta_minimum=50)
            is_green = self._sensor_manager.is_green(green_minimum=100, g_r_delta_minimum=50)
            print(f"POST -> Rouge détecté : {'Oui' if is_red else 'Non'}")
            print(f"POST -> Vert détecté : {'Oui' if is_green else 'Non'}")

            """ Test capteur INA """
            print("POST -> Test du capteur INA")
            current = self._sensor_manager.get_current()
            if current is None:
                print("POST -> Capteur INA non fonctionnel")
                return False
            print(f"POST -> Courant mesuré : {current} A")

            """ Test moteurs DC """
            print("POST -> Test des moteurs DC")
            self._motor_manager.set_speed(50)
            time.sleep(1)
            self._motor_manager.set_speed(-50)
            time.sleep(1)
            self._motor_manager.set_speed(0)

            """Test servo moteur (direction)"""
            print("POST -> Test du servo moteur")
            self._motor_manager.set_angle(-50)
            time.sleep(0.5)
            self._motor_manager.set_angle(50)
            time.sleep(0.5)
            self._motor_manager.set_angle(0)

            print("POST -> Tous les tests sont PASSÉS")
            return True

        except Exception as e:
            print(f"POST -> Erreur pendant le test : {e}")
            return False
        
        
    def select_mode(self):
        """ Fonction de sélection du mode de conduite de la voiture et retourne le mode sélectionné """
        mode = input(
            "Sélectionnez le mode de conduite:\n"
            "1: Course 1 tour\n"
            "2: Course +1 tour\n"
            "3: Post\n"
            "4: Back and Forward\n"
            "5: Turn 8\n"
            "6: Quit\n"
            "7: Depart Feu Vert\n"
            "8: Evite obstacle\n"
            "Votre choix: "
        )
        if mode == "1":
            print("Mode course 1 tour sélectionné")
            self._target_lap = 1
            self._total_laps = 0
            self._config.set_laps_target(1)
            return "racing"
        elif mode == "2":
            print("Mode course +1 tours sélectionné")
            while True:
                try:
                    nombre_tours = int(input("Combien de tours ? "))
                    if nombre_tours > 0:
                        print(f"Mode course {nombre_tours} tours sélectionné")
                        self._target_lap = nombre_tours
                        self._total_laps = 0
                        self._config.set_laps_target(nombre_tours)
                        return "racing"
                    else:
                        print("Veuillez entrer un nombre entier positif.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un nombre entier.")
        elif mode == "3":
            print("Mode post sélectionné")
            return "post"
        elif mode == "4":
            print("Mode back and forward sélectionné")
            return "back_and_forward"
        elif mode == "5":
            print("Mode turn 8 sélectionné")
            return "turn_8"
        elif mode == "6":
            print("Mode quit sélectionné")
            return "quit"
        elif mode == "7":
            print("Mode depart feu vert sélectionné")
            while True:
                try:
                    nombre_tours = int(input("Combien de tours ? "))
                    if nombre_tours > 0:
                        print(f"Mode course {nombre_tours} tours sélectionné")
                        self._target_lap = nombre_tours
                        self._total_laps = 0
                        self._config.set_laps_target(nombre_tours)
                        return "depart_feu_vert"
                    else:
                        print("Veuillez entrer un nombre entier positif.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un nombre entier.")
        elif mode == "8":
            print("Mode d'evitement d'obstacle")
            return "evite_obstacle"
        else:
            print("Mode non valide.")
            return "stand_by"
        
    def eviter_obstacle(self, distances:tuple)->bool:
        """
        Fonction d'évitement d'obstacle, si un obstacle est détecté alors la voiture double al voiture par la gauche et apres retourne à droite pour revenir la où il était
        Retourne vrai si l'obstacle est détecté
        """ 
        obstacle = False
            
        front, left, right = distances
        if front < 100 :
            obstacle = True
            self._motor_manager.set_angle(-100)
            time.sleep(2)
            self._motor_manager.set_angle(100)
            time.sleep(2)
            self._motor_manager.set_angle(0)
            time.sleep(5)
            self._motor_manager.set_angle(100)
            time.sleep(2.5)
            self._motor_manager.set_angle(-100)
            time.sleep(2.2)
            self._motor_manager.set_angle(0)
        
        
    """ Getters"""
    @property
    def motor_manager(self):
        return self._motor_manager
    
    @property
    def sensor_manager(self):
        return self._sensor_manager
    
    @property
    def current_state(self):
        return self._current_state
    
    @property
    def total_laps(self):
        return self._total_laps
    
    @property
    def target_lap(self):
        return self._target_lap
    
    @total_laps.setter
    def total_laps(self,nv_lap):
        self._total_laps = nv_lap
    