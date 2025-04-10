import json
import os
import sys
import os
import busio
import board
import RPi.GPIO as GPIO
from time import sleep
from classes.Distance_Sensor import Distance_Sensor
from classes.Motor_Manager import Motor_Manager
from classes.DC_Motor import DC_Motor
from classes.Servo_Motor import Servo_Motor
from classes.Line_Sensor import Line_Sensor
from classes.INA_Sensor import INA_Sensor
from classes.RGB_Sensor import RGB_Sensor
from classes.Sensor_Manager import Sensor_Manager
from classes.Car import Car

import threading

def main():
    """ Création d'un bus I2C partagé"""
    i2c = busio.I2C(board.SCL,board.SDA)

    """ Récupération des configurations physique du module"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'config', 'physical_config.json')
    with open(json_path, 'r') as f:
        config = json.load(f)

    """ Instance de tous les capteurs et moteurs avec les valeurs de la configuration récupérée """
    front_distance_test = Distance_Sensor(config["HCRS04"]["FRONT"]["TRIG_PIN"],config["HCRS04"]["FRONT"]["ECHO_PIN"] ,config["HCRS04"]["FRONT"]["NAME"])
    left_distance_test = Distance_Sensor(config["HCRS04"]["LEFT"]["TRIG_PIN"],config["HCRS04"]["LEFT"]["ECHO_PIN"] ,config["HCRS04"]["LEFT"]["NAME"])
    right_distance_test = Distance_Sensor(config["HCRS04"]["RIGHT"]["TRIG_PIN"],config["HCRS04"]["RIGHT"]["ECHO_PIN"] ,config["HCRS04"]["RIGHT"]["NAME"])
    line_sensor_test = Line_Sensor(config["IR_SENSOR"]["GPIO_PIN"])
    rgb_sensort_test = RGB_Sensor((i2c,0x29))
    ina_sensor_test = INA_Sensor((i2c,0x40))
    moteur1 = DC_Motor(config["DC_MOTORS"]["LEFT_MOTOR"]["ENABLE_BOARD_CHANNEL"],config["DC_MOTORS"]["LEFT_MOTOR"]["INPUT_PIN_1"],config["DC_MOTORS"]["LEFT_MOTOR"]["INPUT_PIN_2"])
    moteur2 = DC_Motor(config["DC_MOTORS"]["RIGHT_MOTOR"]["ENABLE_BOARD_CHANNEL"],config["DC_MOTORS"]["RIGHT_MOTOR"]["INPUT_PIN_1"],config["DC_MOTORS"]["RIGHT_MOTOR"]["INPUT_PIN_2"])
    servo_test = Servo_Motor(config["SERVO"]["BOARD_CHANNEL"],config["SERVO"]["RANGE_DEGREES_FROM_CENTER"])
    sensors = {
                "line_Sensor" : line_sensor_test,
                "dist_sensor_front" : front_distance_test,
                "dist_sensor_left" : left_distance_test,
                "dist_sensor_right" : right_distance_test,
                "rgb_sensor" : rgb_sensort_test,
                "ina_sensor" : ina_sensor_test
    }

    """ Instance des managers """
    motor_manager = Motor_Manager([moteur1,moteur2],servo_test,(i2c,0x40))
    sensor_manager = Sensor_Manager(sensors)
    config = {
        "OBSTACLE_MINIMUM_DIST" : 10.0,
        "MAX_FRONT_DIST" : 10.0
    }
    TWINGO = Car("TWINGO", motor_manager, sensor_manager,config)

    """ Boucle principale """
    CAR = True
    while CAR:
        if TWINGO.current_state == "stand_by":
            """ Si la voiture est en stanby, ça veut dire que la sélection de mode est en cours """
            new_mode = TWINGO.select_mode()
            print(f"Mode sélectionné : {new_mode}")
            TWINGO.start_car(new_mode)
        elif TWINGO.current_state == "racing":
            """ Si la voiture est en mode course, on Récupère les données capteurs, calcul les target, et applique les modifications aux moteurs, en vérifiant les obstacles et conditions de fin de course """ 
            line = TWINGO.sensor_manager.detect_line()
            rgb = TWINGO.sensor_manager.rgb_sensor.read_value()
            ina = TWINGO.sensor_manager.get_current()

            if line:
                TWINGO.total_laps += 1
                print(f"Tour {TWINGO.total_laps} détecté !")
            distances = TWINGO.sensor_manager.get_distance()
            new_direction, new_speed = TWINGO.calculate_next_move(distances, line)
            fr_new_direction = "braquage " + str(new_direction) + "%"
            if new_speed > 0 :
                fr_new_direction += "droite"
            elif new_speed < 0:
                fr_new_direction += "gauche"
            else:
                fr_new_direction = "freinage"
            TWINGO.motor_manager.set_speed(int(new_speed))
            TWINGO.motor_manager.set_angle(int(new_direction))
            TWINGO.monitoring(distances, line, fr_new_direction, new_speed, ina, rgb)
            if TWINGO.total_laps >= TWINGO.target_lap:
                print("Course terminée !")
                TWINGO.stop_car()

        elif TWINGO.current_state == "post":
            """ Si la voiture est en mode post, on fait un test de tous les moteurs et capteurs """
            print("Power On Self Mode")
            TWINGO.post()
            TWINGO.motor_manager.initialize_motors()
            TWINGO.start_car("stand_by")
            print("Power On Self Mode terminé !")
            
        elif TWINGO.current_state == "back_and_forward":
                """ Si la voiture est en mode back_and_forward, on fait un allée retour en accélérant et décélérant progressivement"""
                print("Allée retour en cours")
                TWINGO.motor_manager.initialize_motors()
                for i in range(0, 101, 1):
                    TWINGO.motor_manager.set_speed(i)
                    sleep(4/100)
                TWINGO.motor_manager.set_speed(0)
                sleep(1)
                for i in range(0, -101, -1):
                    TWINGO.motor_manager.set_speed(i)
                    sleep(4/100)
                TWINGO.stop_car()
                print("Allée retour terminé !")

        elif TWINGO.current_state == "turn_8":
            """ Si la voiture est en mode turn_8, on fait un 8 avec la voiture en faisant simplement 2 virages à gauche et 2 virages à droite """
            print("Grand 8 en cours")
            TWINGO.motor_manager.initialize_motors()
            TWINGO.u_turn('left')
            TWINGO.u_turn('left')
            TWINGO.u_turn('right')
            TWINGO.u_turn('right')
            TWINGO.stop_car()
            print("Grand 8 terminé !")
        
        elif TWINGO.current_state == "quit":
            """ Si la voiture est en mode quit, on arrête la voiture et on quitte le programme """
            print("Arrêt de la voiture")
            TWINGO.motor_manager.initialize_motors()
            # GPIO.cleanup() # Pas sur de ça, à vérifier en pratique
            print("Arrêt de la voiture terminé !")
            CAR = False
            break

        else:
            print("Mode non reconnu")
            TWINGO.current_state = "stand_by"
        sleep(0.1)
    print(" bye bye !")
if __name__ == "__main__":
    main()