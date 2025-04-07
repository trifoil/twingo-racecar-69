import RPI.GPIO as GPIO


class DCMotor():
    def __init__(self, pinEnable: int, pinInput1: int, pinInput2: int):
        self.__pinEnable = pinEnable
        self.__pinInput1 = pinInput1
        self.__pinInput2 = pinInput2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pinEnable, GPIO.OUT)
        GPIO.setup(self.__pinInput1, GPIO.OUT)
        GPIO.setup(self.__pinInput2, GPIO.OUT)
    
    @property
    def pinEnable(self) -> int:
        return self.__pinEnable
    @property
    def pinInput1(self) -> int:
        return self.__pinInput1
    @property
    def pinInput2(self) -> int:
        return self.__pinInput2
    
    def setDirection(self, front:bool)-> None:
        if front:
            GPIO.output(self.pinInput1, GPIO.HIGH)
            GPIO.output(self.pinInput2, GPIO.LOW)
        if not front:
            GPIO.output(self.pinInput1, GPIO.LOW)
            GPIO.output(self.pinInput2, GPIO.HIGH)

    def stop(self) -> None:
        GPIO.output(self.pinInput1, GPIO.HIGH)
        GPIO.output(self.pinInput2, GPIO.HIGH)
            

    