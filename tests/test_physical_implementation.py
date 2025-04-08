import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.DistanceSensor import Distance_Sensor
from classes.LineSensor import Line_Sensor
from classes.INASensor import Ina_Sensor
from classes.RGBSensor import Rgb_Sensor

print("import done")