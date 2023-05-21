"""
TemperatureHumiditySensor class with noise reduction functionality:

The TemperatureHumiditySensor class is used to read temperature and humidity values from a DHT11 or DHT22 temperature
and humidity sensor connected to a Raspberry Pi. The class is initialized with the sensor type (DHT11 or DHT22) and the
GPIO pin number to which the sensor is connected.

The read_temperature_and_humidity method is used to read the temperature and humidity values from the sensor.
The method takes multiple readings and calculates the average temperature and humidity values to reduce noise in the
sensor readings. The number of readings is determined by the num_readings attribute, which is set to 5 by default.

If the readings are successful, the method returns a tuple containing the average temperature and humidity values,
while returning None if the sensor reading fails. It is recommended to adjust the num_readings attribute value as
needed to obtain more accurate readings.
"""
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
class TemperatureHumiditySensor:
    def __init__(self, sensor_type, pin):
        self.sensor_type = sensor_type
        self.pin = pin
        self.num_readings = 5

    def read_temperature_and_humidity(self):
        temperatures = []
        humidities = []
        for i in range(self.num_readings):
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)
            if humidity is not None and temperature is not None:
                humidities.append(humidity)
                temperatures.append(temperature)
        if humidities and temperatures:
            average_humidity = sum(humidities) / float(len(humidities))
            average_temperature = sum(temperatures) / float(len(temperatures))
            return (average_temperature, average_humidity)
        else:
            return None


if __name__ == '__main__':
    try:
        sensor = TemperatureHumiditySensor(Adafruit_DHT.DHT11, 4)
        while True:
            print(sensor.read_temperature_and_humidity())
            time.sleep(5)
    finally:
        GPIO.cleanup()