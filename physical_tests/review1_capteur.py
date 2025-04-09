import sys
import os
import busio
import board
import RPi.GPIO as GPIO
from time import sleep
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.Distance_Sensor import Distance_Sensor
from classes.Line_Sensor import Line_Sensor
from classes.INA_Sensor import INA_Sensor
from classes.RGB_Sensor import RGB_Sensor

i2c = busio.I2C(board.SCL,board.SDA)
print("-------------------------------------------------------------------")
print("CONNEXION AU CAPTEURS DU MODULE...")
front_distance_test = Distance_Sensor(6,5,'front')
left_distance_test = Distance_Sensor(11,9,'left')
right_distance_test = Distance_Sensor(26,19,'right')
line_sensor_test = Line_Sensor(20)
rgb_sensort_test = RGB_Sensor((i2c,0x29))
ina_sensor_test = INA_Sensor((i2c,0x40))
print("CONNEXION ETABLIE !")
print("-------------------------------------------------------------------")

for i in range(100):
    if line_sensor_test.read_value():
        ligne = "OUI"
    else:
        ligne = "NON"
    print(f"""
 --> Distance Droite : {right_distance_test.read_value()} cm
 <-- Distance Gauche : {left_distance_test.read_value()} cm
 <-> Distance Devant : {front_distance_test.read_value()} cm 
          """)

    sleep(3)

    print(f"""
    ||||| Detection de ligne : {ligne}
          """)
    
    sleep(3)

    print(f"""
    ||||| Rrouge, Vert, Blueu: {rgb_sensort_test.read_value()}
          """)
    
    sleep(3)

    print(f"""
    ||||| Tension électique du servomoteur : {ina_sensor_test.read_value()}
          """)   

# """
# Test des capteurs de distances
# """
# print(right_distance_test.read_value())
# print(front_distance_test.read_value())
# print(left_distance_test.read_value())

# """
# Test capteur line
# """
# print(line_sensor_test.read_value())

# """
# Test catpeur rgb
# """ 
# print(rgb_sensort_test.read_value())

# """
# Test catpeur INA
# """
# print(ina_sensor_test.read_value())