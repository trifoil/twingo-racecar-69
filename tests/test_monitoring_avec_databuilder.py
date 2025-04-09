import random
import time

class Car:
    def __init__(self, car_name):
        self._car_name = car_name

    def monitoring(self, distances: tuple, isLine: bool, direction: str, speed: float, ina: dict, rgb: tuple):
        """
        Affiche les données en temps réel pour le suivi de l'état de la voiture.
        """
        right_disc, front_disc, left_disc = distances

        # Affichage des données
        print(f"""
        ======= État actuel de la voiture : {self._car_name} =======
        Distance droite: {right_disc} cm
        Distance frontale: {front_disc} cm
        Distance gauche: {left_disc} cm
        Ligne détectée: {'Oui' if isLine else 'Non'}
        Direction: {direction}
        Vitesse: {speed} %

        === Données du capteur INA ===
        Bus Voltage: {ina['BusVoltage']} V
        Shunt Voltage: {ina['Shunt Voltage']} V
        Current: {ina['Current']} A

        === Couleur RGB ===
        R: {rgb[0]} G: {rgb[1]} B: {rgb[2]}

        ============================================================
        """)


def generate_random_data():

    right_dist = random.randint(0, 100)
    front_dist = random.randint(0, 100)
    left_dist = random.randint(0, 100)
    

    is_line_detected = random.choice([True, False])
    

    direction = random.choice(['left', 'right','front'])
    

    speed = random.uniform(0, 100)
    

    ina_data = {
        'BusVoltage': round(random.uniform(3.0, 5.0), 2),
        'Shunt Voltage': round(random.uniform(0.0, 0.2), 2),
        'Current': round(random.uniform(0, 10), 2)
    }
    

    rgb_data = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    return (right_dist, front_dist, left_dist), is_line_detected, direction, speed, ina_data, rgb_data


car = Car(car_name="Twingo_Race_Car")


try:
    while True:

        distances, is_line, direction, speed, ina, rgb = generate_random_data()


        car.monitoring(distances, is_line, direction, speed, ina, rgb)


        time.sleep(2)

except KeyboardInterrupt:
    print("Simulation stopped.")
