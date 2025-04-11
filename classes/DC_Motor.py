"""
La Classe DC Motor va nous permettre d'instancier les DC motor et de sortir les informations utiles afin
de les controler dans un manager.
Classe DC Motor va comprendre tous les attributs utile à la classe et qui seront repris dans
le motor manager pour le contrôle.
"""


import RPi.GPIO as GPIO



class DC_Motor():
    """
    Constructeur qui va comprendre :
    pin_enable = pin reliée au PWM
    pin_input = pins reliés au pont en H qui permettent de gèrer la vitesse


    GPIO setup permet de setup le mode IN/OUT des pins.
    Ici, toutes les pins sont en sortie (OUT) car ils renvoient leurs infos.
    Le setup High ou Low servira a définir le sens de rotation (accélération ou freinage)
    """

    def __init__(self, pin_enable: int, pin_input1: int, pin_input2: int):
        assert (pin_enable not in [pin_input1, pin_input2]) and (pin_input1 != pin_input2)
        for pin in [pin_enable, pin_input1, pin_input2]:
            assert pin in range(32)
        self._pin_enable = pin_enable
        self._pin_input1 = pin_input1
        self._pin_input2 = pin_input2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_enable, GPIO.OUT)
        GPIO.setup(self._pin_input1, GPIO.OUT)
        GPIO.setup(self._pin_input2, GPIO.OUT)

    """
    listes des set up de getter nécessaires de tout les attributs du DC_Motor
    """

    @property
    def pin_enable(self) -> int:
        return self._pin_enable

    @property
    def pin_input1(self) -> int:
        return self._pin_input1

    @property
    def pin_input2(self) -> int:
        return self._pin_input2



    def set_direction(self, forward: bool) -> None:
        """
        Fonction qui permet de gérer l'accélération ou freinage.
        Elle fonctionne sur un booléen. Si le booléen est True, elle avance. Si False, elle freine.
        """
        if forward:
            GPIO.output(self.pin_input1, GPIO.HIGH)
            GPIO.output(self.pin_input2, GPIO.LOW)
        if not forward:
            GPIO.output(self.pin_input1, GPIO.LOW)
            GPIO.output(self.pin_input2, GPIO.HIGH)



    def stop_brake(self) -> None:
        """
        Fonction stop qui met la voiture à l'arrêt en la faisant freiné.
        En mettant les deux pins en HIGH, le moteur va freiné pour un arrêt rapide.
        """
        GPIO.output(self.pin_input1, GPIO.HIGH)
        GPIO.output(self.pin_input2, GPIO.HIGH)



    def stop_free_wheels(self) -> None:
        """
        Fonction stop qui met la voiture en l'arrêt en coupant le moteur.
        En mettant les deux pins en LOW, le moteur va se mettre à l'arrêt.
        La voiture va continuer jusqu'a l'arrêt complet (freinage par frottement)
        """
        GPIO.output(self.pin_input1, GPIO.LOW)
        GPIO.output(self.pin_input2, GPIO.LOW)


