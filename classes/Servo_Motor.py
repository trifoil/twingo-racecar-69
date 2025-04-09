"""
Classe du Servo Moteur qui va nous permettre de controler l'angle des roues.
Importance de l'angle initial afin de pouvoir toujours restart sur un angle logique et empêcher des rotations impossible.
Importance des options possibles d'angles afin d'éviter que le servo moteur aillent dans des angles impossibles.
"""


"""
Constructeur de la classe :
• board_channel => branchement de PWM drive (PCA9685)
• range_degrees => angles possibles pris par le servomoteur
• min et max pulse => constante du servomoteur qui nous permettront de calculer et setup des angles de rotations
• Initial angle => Nous permet de restart a une angle initial donnée et de retourner à cette angle si nécessaire
• Frequency => Fréquence qu'on va utiliser pour l'intégralité des composants du système, on la retrouvera dans le motor manager
"""
class Servo_Motor():
    def __init__(self, board_channel:int, range_degrees:int):
        assert board_channel in [i for i in range(16)]
        
        self._board_channel = board_channel
        self._range_degrees = range_degrees
        self._min_pulse = 1.0 # in ms
        self._max_pulse = 2.0 # in ms
        self._initial_angle = 90
        self._frequency = 60

        assert (self._initial_angle - range_degrees) >= 0
        assert (self._initial_angle + range_degrees) <= 180



    """
    Listes des getters afin de récupèrer les données plus tard
    """
    @property
    def board_channel(self) -> int:
        return self._board_channel
    @property
    def range_degrees(self) -> float:
        return self._range_degrees
    @property
    def min_pulse(self) -> float:
        return self._min_pulse
    @property
    def max_pulse(self) -> float:
        return self._max_pulse
    @property
    def initial_angle(self) -> float:
        return self._initial_angle
    @property
    def frequency(self) -> float:
        return self._frequency

    
    
    
