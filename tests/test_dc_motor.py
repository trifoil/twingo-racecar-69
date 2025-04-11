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

import unittest
from classes.DC_Motor import DC_Motor

# Disable Logging
from classes.Logging_Utils import Logging_Utils
Logging_Utils.setup_logging_in_main(verbose=False, write_file=False)

class Test_DC_Motor(unittest.TestCase):
    def test_pins_are_differents_and_in_range_of_16(self):
        for i in range(16):
            for j in range(16):
                for k in range(16):
                    if i in [j, k] or j == k:
                        with self.assertRaises(AssertionError, msg="pin_enable="+str(i)+" pin_input1="+str(j)+" pin_input2="+str(k)):
                            dc_motor = DC_Motor(i, j, k)
                    else:
                        dc_motor = DC_Motor(i, j, k)
                        self.assertIsInstance(dc_motor, DC_Motor)
    

    def test_pins_out_of_range_raise_error(self):
        working_pins = [2,3]
        error_pins = [-1, 17, 200]
        for pin in error_pins:
            with self.assertRaises(AssertionError):
                dc_motor = DC_Motor(working_pins[0], working_pins[0], pin)
            with self.assertRaises(AssertionError):
                dc_motor = DC_Motor(working_pins[0], pin, working_pins[0])
            with self.assertRaises(AssertionError):
                dc_motor = DC_Motor(pin, working_pins[0], working_pins[0])