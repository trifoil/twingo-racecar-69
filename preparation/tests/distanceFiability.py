import time
import statistics
from ..classes.SensorManager import SensorManager

"""
Exemple de sortie:

------
Début des mesures...
Résultats sur 100 mesures :
Capteur FRONT : Moyenne = 4.93 cm, Écart-type = 0.06 cm, % hors marge = 0.0%
Capteur LEFT  : Moyenne = 6.19 cm, Écart-type = 0.09 cm, % hors marge = 1.0%
Capteur RIGHT : Moyenne = 7.54 cm, Écart-type = 0.11 cm, % hors marge = 0.0%
------
"""

# Paramètres du test
NUM_MEASUREMENTS = 100
# Valeurs attendues et marge acceptable (en cm)
EXPECTED_FRONT = 5
EXPECTED_LEFT  = 7
EXPECTED_RIGHT = 8
MARGIN = 1

def compute_stats(values, expected, margin):
    """ Calcule la moyenne, l'écart-type et le pourcentage de mesures en dehors de la marge """
    if not values:
        return None, None, None
    avg = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0
    count_outside = sum(1 for x in values if abs(x - expected) > margin)
    percent_outside = (count_outside / len(values)) * 100
    return avg, std, percent_outside

def run_test():
    sensor_manager = SensorManager()
    front_measurements = []
    left_measurements = []
    right_measurements = []

    print("Début des mesures...")
    for i in range(NUM_MEASUREMENTS):
        front, left, right = sensor_manager.getDistance()
        if front is not None:
            front_measurements.append(front)
        if left is not None:
            left_measurements.append(left)
        if right is not None:
            right_measurements.append(right)
        time.sleep(0.05)  # Pause entre les mesures

    # Calcul des statistiques pour chaque capteur
    front_stats = compute_stats(front_measurements, EXPECTED_FRONT, MARGIN)
    left_stats  = compute_stats(left_measurements, EXPECTED_LEFT, MARGIN)
    right_stats = compute_stats(right_measurements, EXPECTED_RIGHT, MARGIN)

    print("Résultats sur {} mesures :".format(NUM_MEASUREMENTS))
    print("Capteur FRONT : Moyenne = {:.2f} cm, Écart-type = {:.2f} cm, % hors marge = {:.1f}%".format(*front_stats))
    print("Capteur LEFT  : Moyenne = {:.2f} cm, Écart-type = {:.2f} cm, % hors marge = {:.1f}%".format(*left_stats))
    print("Capteur RIGHT : Moyenne = {:.2f} cm, Écart-type = {:.2f} cm, % hors marge = {:.1f}%".format(*right_stats))

if __name__ == "__main__":
    run_test()
