import unittest
from classes.Servo_Motor import Servo_Motor

class Test_DC_Motor(unittest.TestCase):
    def test_board_channel_valid_range(self):
        start = 0
        end = 15
        try:
            for i in range(start, end+1, 1):
                servo = Servo_Motor(board_channel=i, range_degrees=45)
        except:
            self.fail("Il y a une erreur lorse qu'on met une valeur comprise entre 0 et 15 pour le param 'board_channel' dans le constructeur de 'Servo_Motor'")

    def test_range_degrees_is_not_under_zero_or_over_180(self):
        for i in range(0, 180+1):
            servo = None
            has_run = False
            try:
                servo = Servo_Motor(board_channel=7, range_degrees=i)
                has_run = True
            except:
                pass
            
            if has_run:
                self.assertIsInstance(servo, Servo_Motor)
                min_angle = servo._initial_angle - i
                max_angle = servo._initial_angle + i
                self.assertGreaterEqual(min_angle, 0)
                self.assertGreaterEqual(180, max_angle)

if __name__ == "__main__":
    unittest.main()