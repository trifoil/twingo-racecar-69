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
        self._target_lap = 0
        self._last_move = None
        self._last_error = None
        print(f"""
{self._car_name} opérationel !
              """)

    def detect_obstacle(self,distances:tuple)->bool:
        """
        Detection d'un obstacle en face de la voiture, via vérification de la distance minimum de configuration de la voiture (exemple 10.0cm)
        Retourne Vrai si détecté
        Sinon retourne faux
        """
        obstacle = False
        front, left, right = distances

        try:
            # if front < self._const_config["OBSTACLE_MINIMUM_DIST"]:
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

                    # if front > self._const_config["OBSTACLE_MINIMUM_DIST"]:
                    if front > 20.0:
                        obstacle = Falses
                        return obstacles

        except Exception as e:
            print(f"Un erreur est survenue : {e}")

    def count_lap(self,detectedLine:bool) -> None:
        """
        Détection d'une ligne, si ligne detectée alors nombre de tour +1
        """
        if detectedLine:
            self._total_laps +=1
        print("NEW LAP")

    def start_car(self, mode:str) -> None:
        self._current_state = mode
    def stop_car(self):
        self._current_state = "stand_by"
        self._motor_manager.set_speed(0)
        self._motor_manager.set_angle(0)
        print(f"""
{self._car_name} est arrêté.
              """)

    def calculate_next_move(self, distances: tuple) -> tuple:
        front_disc, left_disc, right_disc = distances
        target_right = 10.0
        kp = 1.0
        kd = 0.5
        if self._last_move == None:
            self._last_move = time.time()
            diff_time = 0.0
        elif self._last_move != None:
            diff_time = self._last_move - time.time()
            self._last_move = time.time()
        if diff_time > 0:
            if self._last_error == None:
                self._last_error = 0.0
            elif self._last_error != None:
                diff_error = right_disc - target_right
                derivative = diff_error - self._last_error / diff_time
                self._last_error = diff_error
        else:
            derivative = 0.0
        new_direction = kp * (right_disc - target_right) + kd * derivative
        new_speed = 50
        if new_direction > 100:
            new_direction = 100
        if new_direction < -100:
            new_direction = -100
        return (new_direction, new_speed)
    
        # try:
        #     minimum_right =  self._const_config['MINIMUM_RIGHT_DIST']
        #     maximum_right =  self._const_config['MAXIMUM_RIGHT_DIST']
        #     target = maximum_right - minimum_right
        #     if right_disc < 0:
        #         right_disc = 0
        #     if right_disc > 100:
        #         right_disc = 100

        #     new_direction = 10 * right_disc + 100
            
        #     if new_direction > 100:
        #         new_direction = 100
        #     if new_direction < 0:
        #         new_direction = 0
        #     return (new_direction, 50)
        # except:
        #     return (50, 50)
   

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
            "Votre choix: "
        )
        if mode == "1":
            print("Mode course 1 tour sélectionné")
            self._target_lap = 1
            self._total_laps = 0
            return "racing"
        elif mode == "2":
            print("Mode course +1 tours sélectionné")
            while True:
                try:
                    nombre_tours = int(input("Combien de tours ? "))
                    if nombre_tours > 0:
                        print(f"Mode course {nombre_tours} tours sélectionné")
                        self._target_lap = nombre_tours
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
        else:
            print("Mode non valide.")
            return "stand_by"
        
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
    