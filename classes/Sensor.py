"""
Interface de tout les capteurs utilisés dans le code, elle les obligent à implémenter la méthode read_value
qui nous permettra d'avoir les infos utile dans le sensor manager
"""


from abc import ABC
from abc import abstractmethod

""" Interface Sensor """
class Sensor(ABC):
    @abstractmethod
    def read_value() -> any:
        pass