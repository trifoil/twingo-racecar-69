"""
Classe Config a pour but de noter dans un fichier externe (.json) toutes les configs actuelles de la voiture.
Le but est de pouvoir reset la voiture sans perdre ses états lors d'un crash tout en prennant
note de certaines informations complémentaires.

Les informations sauvegardées sont :
• should_be_running : permet de savoir si la voiture devrait être en train de rouler
• laps_elapsed : Nombre de tour réalisés depuis le lancement
• total_laps : Nombre de tour au total que la voiture doit réaliser
• lap_start_timestamps : Le temps en unix pour savoir quand un tour a été commencé

Ses méthodes sont :
• reset : reset les informations
• set_laps_target : définit le nombre de tours demandés
• add_laps : incrémente de 1 le nombre de tour réalisés
• set_attribute : permet de paramètrer l'intégralités des attributs en une fois
• add_lap_timestamp : ajoute un timestamp au tour en cours
• writelaptime : ajoute le temps actuel au timestamp en cours
• get_config_dict : retourne les informations du fichier de config sous forme de dictionnaire
• get_last_lap_time : recupère l'information du time stamp du tour précédent
• get_last_lap_time_formatted : formatte le time stamp pour savoir le lire correctement
• is_complete : Vérifie que le nombre total de tour a été réalisé
• get_formatted_config : Affiche les informations du fichier config dans l'invit de commande
• save_to_json : Sauvegarde les informations du fichier de config dans un fichier json
• load_to_json : Récupère les attributs du fichier config enregistré dans un fichier json
"""

import json
import time
from datetime import datetime

class Config:
    def __init__(self):
        self.reset()  # Initialize with default values


    def reset(self):
        """Fonction de reset qui va poser tout les attributs de la classe à 0, vider la liste des time stamps,
        remettre l'état de la voiture à "ne devrait pas rouler" """
        self._should_be_running = False  # Changed to reflect desired state
        self._laps_elapsed = 0
        self._laps_total = 0
        self._lap_start_timestamps = []


    def set_laps_target(self, total_laps):
        """Set le nombre de tour souhaités"""
        if not isinstance(total_laps, int) or total_laps < 0:
            raise ValueError("Total laps must be a positive integer")
        self._laps_total = total_laps



    def add_lap(self):
        """Ajoute un tour au nombre de tour complété"""
        self._laps_elapsed += 1
        self.writelaptime()



    def set_attributes(self, should_be_running=None, laps_elapsed=None, laps_total=None, lap_start_timestamps=None):
        """Cette méthode permet de set tout les attributs un par un et vérifie que tout les attributs soit
        complété avec une valeur
        """
        if should_be_running is not None:
            self._should_be_running = should_be_running
        if laps_elapsed is not None:
            self._laps_elapsed = laps_elapsed
        if laps_total is not None:
            self._laps_total = laps_total
        if lap_start_timestamps is not None:
            if isinstance(lap_start_timestamps, (list, tuple)):
                for ts in lap_start_timestamps:
                    self._validate_timestamp(ts)
                self._lap_start_timestamps = list(lap_start_timestamps)
            else:
                self._validate_timestamp(lap_start_timestamps)
                self._lap_start_timestamps = [lap_start_timestamps]


    def _validate_timestamp(self, timestamp):
        """Vérifie que le timestamp est une donnée raisonnable en unix"""
        current_time = int(time.time())
        if not isinstance(timestamp, (int, float)):
            raise ValueError("Timestamp must be a number")
        if timestamp < 0:
            raise ValueError("Timestamp cannot be negative")
        if timestamp > current_time + 86400:  # Allow timestamps up to 1 day in future
            raise ValueError("Timestamp too far in the future")


    def set_should_be_running(self, value):
        self._should_be_running = bool(value)


    def add_lap_elapsed(self, value):
        self._laps_elapsed = value + 1
    
    def set_laps_total(self, value):
        self._laps_total = value



    def add_lap_timestamp(self, timestamp=None):
        """Ajoute un timestamps (temps actuel si aucun n'a été fournis)"""
        if timestamp is None:
            timestamp = time.time()
        self._validate_timestamp(timestamp)
        self._lap_start_timestamps.append(timestamp)
    
    def writelaptime(self):
        """Ajoute le temps actuel au timestamp"""
        self.add_lap_timestamp()
    
    # Property getters
    @property
    def should_be_running(self):
        """Permet de vérifier si la voiture devrait être en train rouler ou pas"""
        return self._should_be_running
    
    @property
    def laps_elapsed(self):
        return self._laps_elapsed
    
    @property
    def laps_total(self):
        return self._laps_total
    
    @property
    def lap_start_timestamps(self):
        return self._lap_start_timestamps.copy()
    
    # Additional getters
    def get_config_dict(self):
        """Retourne une dictionnaire avec les configs du système"""
        return {
            'should_be_running': self._should_be_running,
            'laps_elapsed': self._laps_elapsed,
            'laps_total': self._laps_total,
            'lap_start_timestamps': self._lap_start_timestamps.copy()
        }
    
    def get_last_lap_time(self):
        """Récupère le timestamp du dernier tour"""
        if not self._lap_start_timestamps:
            return None
        return self._lap_start_timestamps[-1]
    
    def get_last_lap_time_formatted(self):
        """Récupère la version formaté en YYMMDD du timestamp du tour précèdent"""
        last_lap = self.get_last_lap_time()
        if last_lap is None:
            return "No laps recorded"
        return datetime.fromtimestamp(last_lap).strftime('%Y-%m-%d %H:%M:%S')
    
    def get_laps_remaining(self):
        """Calcule le nombre de tours restants"""
        return max(0, self._laps_total - self._laps_elapsed)
    
    def is_complete(self):
        """Vérifie si tout les tours ont été réalisés"""
        return self._laps_elapsed >= self._laps_total > 0
    
    def get_formatted_config(self):
        """Renvoie un string lisible de la config en cours dans l'invit de command"""
        return (
            f"Should be running: {'Yes' if self._should_be_running else 'No'}\n"
            f"Laps Completed: {self._laps_elapsed}/{self._laps_total}\n"
            f"Laps Remaining: {self.get_laps_remaining()}\n"
            f"Last Lap Time: {self.get_last_lap_time_formatted()}\n"
            f"All Lap Times: {[self.get_last_lap_time_formatted() for _ in self._lap_start_timestamps]}"
        )
    
    def __str__(self):
        return self.get_formatted_config()
    
    def save_to_json(self, filename="config.json"):
        """Sauvegarde la config dans un fichier JSON dans le dossier config"""
        filepath = f"config/{filename}"
        with open(filepath, 'w') as f:
            json.dump(self.get_config_dict(), f, indent=4)

    @classmethod
    def load_from_json(cls, filename="config.json"):
        """Charge la configuration depuis un fichier JSON du dossier config et retoure une instance de Config"""
        filepath = f"config/{filename}"
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        config = cls()
        config.set_attributes(
            should_be_running=data.get('should_be_running', False),
            laps_elapsed=data.get('laps_elapsed', 0),
            laps_total=data.get('laps_total', 0),
            lap_start_timestamps=data.get('lap_start_timestamps', [])
        )
        return config