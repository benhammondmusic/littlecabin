from django.test import TestCase
from .fetch_weather import update_current_weather

class WeatherTestCase(TestCase):
    def test_weather_response(self):
        """ update_current_weather() method should return
        - an object with key "temp" and int value, and key "conditions" with string value
        - temp should be in a valid range for earth degrees F(greater than -50 and less than 150)
         """
        current_weather_obj = update_current_weather()

        self.assertEqual(type(current_weather_obj["temp"]), int)
        self.assertEqual(type(current_weather_obj["conditions"]), str)
        self.assertGreater(current_weather_obj["temp"], -50)
        self.assertLess(current_weather_obj["temp"], 150)




#  