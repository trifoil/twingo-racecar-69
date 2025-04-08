import sys
import os
import busio
import board
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("import des classes...")
from classes.DistanceSensor import Distance_Sensor
from classes.LineSensor import Line_Sensor
from classes.INASensor import Ina_Sensor
from classes.RGBSensor import Rgb_Sensor

print("import Done !")
print("création I2C...")
i2c = busio.I2C(board.SCL,board.SDA)
print("I2C Done !")
print("création instances capteurs...")
front_distance_test = Distance_Sensor(6,5,'front')
left_distance_test = Distance_Sensor(11,9,'left')
right_distance_test = Distance_Sensor(26,19,'right')
line_sensor_test = Line_Sensor(20)
# ina_sensor_test = Ina_Sensor((0x40,i2c))
print("Capteurs Done !")