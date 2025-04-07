from classes.LineSensor import LineSensor
from classes.DistanceSensor import DistanceSensor
from classes.RGBSensor import RGBSensor
from classes.INASensor import INASensor
import threading
import busio
import time

class SensorManager:
    def __init__(self,bus_i2C:busio.I2C):
        """ Définition de tous les capteurs et utilisation du bus commun i²C """
        self.__i2c_bus = bus_i2C
        self.__lineSensor = LineSensor(20)
        self.__distSensorFront = DistanceSensor(6,5,'Front')
        self.__distSensorLeft = DistanceSensor(11,9,'Left')
        self.__distSensorRight = DistanceSensor(26,19,'Right')
        self.__rgbSensor = RGBSensor(0x29,self.__i2c_bus)
        self.__inaSensor = INASensor(0x40,self.__i2c_bus)
        self.__isOnLine = False

    def detectLine(self) -> bool:
        """
        Détecte le passage sur la ligne.
        Renvoie True uniquement lors de la première détection lorsque la voiture entre sur la ligne.
        """
        try:
            if not self.__isOnLine and self.__lineSensor.readValue():
                self.__isOnLine = True
                return True
            elif self.__isOnLine and not self.__lineSensor.readValue():
                self.__isOnLine = False
        except Exception as e:
            print("Erreur lors de la détection de la ligne:", e)
        return False
    
    def getDistance(self) -> tuple:
        """
        Renvoie un tuple des distances (Front, Left, Right) en cm.
        Pour chaque capteur, 5 mesures sont effectuées et la moyenne des lectures valides est calculée.
        En cas d'erreur, la mesure sera ignorée.
        """
        results = [None, None, None]

        def wrapper(sensor, index):
            readings = []
            for _ in range(5):
                value = sensor.readValue()
                if value is not None:
                    readings.append(value)
                time.sleep(0.01) 
            if readings:
                avg = round(sum(readings) / len(readings),1)
            else:
                avg = None 
            results[index] = avg

        threads = [
            threading.Thread(target=wrapper, args=(self.__distSensorFront, 0)),
            threading.Thread(target=wrapper, args=(self.__distSensorLeft, 1)),
            threading.Thread(target=wrapper, args=(self.__distSensorRight, 2))
        ]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return tuple(results)

    def getCurrent(self) -> float:
        """
        Renvoie la valeur du courant mesuré par le capteur INA.
        En cas d'erreur, renvoie None.
        """
        try:
            sensorData = self.__inaSensor.readValue()
            return sensorData.get('Current', None)
        except Exception as e:
            print("Erreur lors de la lecture du courant: ", e)
            return None
    
    def isRed(self,redMinimum:int,G_R_DeltaMinimum:int) -> bool:
        """
        Détecte la présence de rouge.
        Le rouge est considéré comme détecté si :
          - la valeur de R est supérieure ou égale à redMinimum,
          - et si la différence (R - G) est supérieure ou égale à G_R_DeltaMinimum.
        """
        try:
            r, g, b = self.__rgbSensor.readValue()
            if r < redMinimum:
                return False
            if (r - g) < G_R_DeltaMinimum:
                return False
            return True
        except Exception as e:
            print("Erreur lors de la détection du rouge: ", e)
            return False

    def isGreen(self,greenMinimum:int,G_R_DeltaMinimum:int) -> bool:
        """
        Détecte la présence de vert.
        Le vert est considéré comme détecté si :
          - la valeur de G est supérieure ou égale à greenMinimum,
          - et si la différence (G - R) est supérieure ou égale à G_R_DeltaMinimum.
        """
        try:
            r, g, b = self.__rgbSensor.readValue()
            if g < greenMinimum:
                return False
            if (g - r) < G_R_DeltaMinimum:
                return False
            return True
        except Exception as e:
            print("Erreur lors de la détection du vert: ", e)
            return False