import RPi.GPIO as GPIO
import time

class RainSensor:
    """
    A class representing a rain sensor that can detect whether it's raining or not.

    Attributes:
        pin (int): The GPIO pin number used to connect the rain sensor.

    Methods:
        is_raining(): Reads the sensor value and returns a boolean indicating whether it's raining or not.
    """

    def __init__(self, pin):
        """
        Initializes a new instance of the RainSensor class.

        Args:
            pin (int): The GPIO pin number used to connect the rain sensor.
        """
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    def is_raining(self):
        """
        Reads the sensor value and returns a boolean indicating whether it's raining or not.

        Returns:
            bool: True if it's raining, False otherwise.
        """
        sensor_value = GPIO.input(self.pin)

        if sensor_value == GPIO.LOW:
            return True
        else:
            return False

if __name__ == '__main__':
    try:
        sensor = RainSensor(13)
        while True:
            print(sensor.is_raining())
            time.sleep(5)
    finally:
        GPIO.cleanup()