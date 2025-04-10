from classes.Line_Sensor import Line_Sensor
from classes.Distance_Sensor import Distance_Sensor
from classes.RGB_Sensor import RGB_Sensor
from classes.INA_Sensor import INA_Sensor
import threading
import busio
import time

class Sensor_Manager:
    def __init__(self,sensors:dict): 
        """ Définition de tous les capteurs et utilisation du bus commun i²C 
            Argument du constructeur via un dictionnaire
            {
            "line_Sensor" : INSTANCE_LINE_SENSOR,
            "dist_sensor_front" : INSTANCE_DISTANCE_SENSOR,
            "dist_sensor_left" : INSTANCE_DISTANCE_SENSOR,
            "dist_sensor_right" : INSTANCE_DISTANCE_SENSOR,
            "rgb_sensor" : INSTANCE_RGB_SENSOR,
            "ina_sensor" : INSTANCE_INA_SENSOR
            }
        """
        self._line_sensor = sensors['line_Sensor']
        self._dist_sensor_front = sensors['dist_sensor_front']
        self._dist_sensor_left = sensors['dist_sensor_left']
        self._dist_sensor_right = sensors['dist_sensor_right']
        self._rgb_sensor = sensors['rgb_sensor']
        self._ina_sensor = sensors['ina_sensor']
        self._is_on_line = False

    def detect_line(self) -> bool:
        """
        Détecte le passage sur la ligne.
        Renvoie True uniquement lors de la première détection lorsque la voiture entre sur la ligne.
        """
        try:
            if not self._is_on_line and self._line_sensor.read_value():
                self._is_on_line = True
                return True
            elif self._is_on_line and not self._line_sensor.read_value():
                self._is_on_line = False
        except Exception as e:
            print("Erreur lors de la détection de la ligne:", e)
        return False
    
    def get_distance(self) -> tuple:
        """
        Renvoie un tuple des distances (Front, Left, Right) en cm.
        Pour chaque capteur, 5 mesures sont effectuées et la moyenne des lectures valides est calculée.
        En cas d'erreur, la mesure sera ignorée.
        """
        results = [None, None, None]

        def wrapper(sensor, index):
            readings = []
            for _ in range(5):
                try:
                    value = sensor.read_value()
                    if value is not None:
                        readings.append(value)
                except Exception as e:
                    print(sensor.side, e)
                time.sleep(0.01) 
            if readings:
                avg = round(sum(readings) / len(readings),1)
            else:
                avg = None 
            results[index] = avg

        threads = [
            threading.Thread(target=wrapper, args=(self._dist_sensor_front, 0)),
            threading.Thread(target=wrapper, args=(self._dist_sensor_left, 1)),
            threading.Thread(target=wrapper, args=(self._dist_sensor_right, 2))
            ]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return tuple(results)

    def get_current(self) -> float:
        """
        Renvoie la valeur du courant mesuré par le capteur INA.
        En cas d'erreur, renvoie None.
        """
        try:
            sensor_data = self._ina_sensor.read_value()
            return sensor_data
        except Exception as e:
            print("Erreur lors de la lecture du courant: ", e)
            return None
    
    def is_red(self,red_minimum:int,g_r_delta_minimum:int) -> bool:
        """
        Détecte la présence de rouge.
        Le rouge est considéré comme détecté si :
          - la valeur de R est supérieure ou égale à red_minimum,
          - et si la différence (R - G) est supérieure ou égale à g_r_delta_minimum.
        """
        try:
            r, g, b = self._rgb_sensor.read_value()
            if r < red_minimum:
                return False
            if (r - g) < g_r_delta_minimum:
                return False
            return True
        except Exception as e:
            print("Erreur lors de la détection du rouge: ", e)
            return False

    def is_green(self,green_minimum:int,g_r_delta_minimum:int) -> bool:
        """
        Détecte la présence de vert.
        Le vert est considéré comme détecté si :
          - la valeur de G est supérieure ou égale à green_minimum,
          - et si la différence (G - R) est supérieure ou égale à g_r_delta_minimum.
        """
        try:
            r, g, b = self._rgb_sensor.read_value()
            if g < green_minimum:
                return False
            if (g - r) < g_r_delta_minimum:
                return False
            return True
        except Exception as e:
            print("Erreur lors de la détection du vert: ", e)
            return False
    @property
    def rgb_sensor(self):
        return self._rgb_sensor
    @property
    def ina_sensor(self):
        return self._ina_sensor