"""This file is our own customised toolset for the Agent"""
# import Adafruit_DHT
from langchain.tools import BaseTool
# from iodevices.TemperatureHumiditySensor import TemperatureHumiditySensor
from iodevices.rainning_check import RainSensor

# class IndoorTemperatureHumidity(BaseTool):
#     name = "IndoorTemperatureHumidity"
#     description = "Use it when you need to know the temperature and humidity in the room"
#     def _run(self,query: str) -> str:
#         """return Temperature and Humidity"""
#         temperatureHumiditySensor = TemperatureHumiditySensor(Adafruit_DHT.DHT11, 4)
#         temperature,humidity = temperatureHumiditySensor.read_temperature_and_humidity()
        
#         # Test case
#         # temperature,humidity = 23,55

#         #Check for correct return of temperature and humidity
#         try:
#             self.check_not_none(temperature)
#             self.check_not_none(humidity)
#         except ValueError as e:
#             print(e)
#         return '''The current room temperature:{}°C \n The current humidity in the room:{}\%'''.format(temperature,humidity)

#     def check_not_none(self,a):
#         if a is not None:
#             return True
#         else:
#             raise ValueError("Temperature and humidity cannot be None!")
        
#     async def _arun(self, query: str) -> str:
#         """Use the tool asynchronously."""
#         raise NotImplementedError("IndoorTemperatureHumidity does not support async")


class CheckRaining(BaseTool):
    name = "CheckRaining"
    description = "Use it when you are asked to use the raindrop sensor to detect rain"
    def _run(self, query:str) -> str:
        """Return to Whether it's raining or not """
        
        # TODO No parameters for the pins have been passed in yet, this part is not complete
        rainSensor = RainSensor(13)
        isRaining = rainSensor.is_raining()
        # isRaining = True
        # Check for correct return of isRaining
        try:
            self.check_not_none(isRaining)
        except ValueError as e:
            print(e)
        
        if isRaining:
            return "It's raining right now"
        else:
            return "No rain now"

    def check_not_none(self,a):
        if a is not None:
            return True
        else:
            raise ValueError("isRaining cannot be None!")
        
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("CheckRaining does not support async")
    