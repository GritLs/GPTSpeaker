# Import the RPi.GPIO module for controlling GPIO pins
# invaild
import RPi.GPIO as GPIO

class Light:
    def __init__(self, pin):
        # Initialize the Light class with the specified GPIO pin number
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)  # Use board pin numbering scheme
        GPIO.setup(self.pin, GPIO.OUT)  # Set the pin to output mode

    def on(self):
        # Turn on the light
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        # Turn off the light
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        # Toggle the state of the light
        state = GPIO.input(self.pin)
        if state == GPIO.HIGH:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)

    def cleanup(self):
        # Clean up the GPIO pins
        GPIO.cleanup()