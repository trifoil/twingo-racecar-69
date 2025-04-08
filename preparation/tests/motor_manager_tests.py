import sys
import types

# --- Injection de dummy modules pour RPi et board ---

# Créer un module dummy pour le package "RPi" s'il n'existe pas déjà
if "RPi" not in sys.modules:
    dummy_rpi = types.ModuleType("RPi")
    sys.modules["RPi"] = dummy_rpi
else:
    dummy_rpi = sys.modules["RPi"]

# Créer un module dummy pour "RPi.GPIO"
dummy_gpio = types.ModuleType("RPi.GPIO")
dummy_gpio.OUT = 1
dummy_gpio.IN = 0
dummy_gpio.BCM = "BCM"
dummy_gpio.BOARD = "BOARD"
dummy_gpio.setmode = lambda mode: None
dummy_gpio.setup = lambda pin, mode: None
dummy_gpio.input = lambda pin: 0
dummy_gpio.output = lambda pin, state: None
dummy_gpio.cleanup = lambda: None

# Assigner dummy_gpio à RPi.GPIO et au package RPi
dummy_rpi.GPIO = dummy_gpio
sys.modules["RPi.GPIO"] = dummy_gpio

# Créer un module dummy pour "board"
dummy_board = types.ModuleType("board")
dummy_board.SCL = "SCL"
dummy_board.SDA = "SDA"
sys.modules["board"] = dummy_board

# --- Fin des injections dummy ---

import unittest
from unittest.mock import patch, MagicMock
import threading
import time
import os

# Ajoute le dossier parent au path pour accéder aux modules dans "classes"
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.insert(0, parent_dir)

# --- Patch du constructeur de TCS34725 pour éviter l'initialisation matérielle ---
# On définit un dummy qui simule l'objet renvoyé par adafruit_tcs34725.TCS34725
class DummyTCS34725:
    def __init__(self, i2c_bus):
        self._i2c_bus = i2c_bus
    @property
    def color_rgb_bytes(self):
        # Retourne des valeurs par défaut (que vous pourrez modifier dans vos tests via des mocks)
        return (100, 50, 20)

# --- Import de SensorManager après avoir patché les modules matériels ---
from classes.MotorManager import MotorManager

