import RPI.GPIO as GPIO

"""
Constructeur qui va comprendre :
pin_enable = pin reliée au PWM
pin_input = pins reliés au pont en H qui permettent de gèrer la vitesse


GPIO setup permet de setup le mode IN/OUT des pins. 
Ici, toutes les pins sont en sortie (OUT) car ils renvoient leurs infos.
Le setup High ou Low servira a définir le sens de rotation (accélération ou freinage)
"""


class DC_Motor():
    def __init__(self, pin_enable: int, pin_input1: int, pin_input2: int):
        self.__pin_enable = pin_enable
        self.__pin_input1 = pin_input1
        self.__pin_input2 = pin_input2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin_enable, GPIO.OUT)
        GPIO.setup(self.__pin_input1, GPIO.OUT)
        GPIO.setup(self.__pin_input2, GPIO.OUT)

    """
    Set up de getter nécessaire de tout les attributs du DC_Motor
    """

    @property
    def pin_enable(self) -> int:
        return self.__pin_enable

    @property
    def pin_input1(self) -> int:
        return self.__pin_input1

    @property
    def pin_input2(self) -> int:
        return self.__pin_input2

    """
    Fonction qui permet de gérer l'accélération ou freinage.
    """

    def set_direction(self, forward: bool) -> None:
        if forward:
            GPIO.output(self.pin_input1, GPIO.HIGH)
            GPIO.output(self.pin_input2, GPIO.LOW)
        if not forward:
            GPIO.output(self.pin_input1, GPIO.LOW)
            GPIO.output(self.pin_input2, GPIO.HIGH)

    """
    Fonction stop qui met la voiture à l'arrêt en la faisant freiné.
    En mettant les deux pins en HIGH, le moteur va freiné pour un arrêt rapide.
    """

    def stop_brake(self) -> None:
        GPIO.output(self.pin_input1, GPIO.HIGH)
        GPIO.output(self.pin_input2, GPIO.HIGH)

    """
    Fonction stop qui met la voiture en l'arrêt en coupant le moteur.
    En mettant les deux pins en LOW, le moteur va se mettre à l'arrêt.
    La voiture va continuer jusqu'a l'arrêt complet (freinage par frottement)
    """

    def stop_free_wheels(self) -> None:
        GPIO.output(self.pin_input1, GPIO.LOW)
        GPIO.output(self.pin_input2, GPIO.LOW)


