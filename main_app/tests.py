from django import test
from django.test import TestCase
from .fetch_weather import update_current_weather
from .views import is_family_member, create_random_user

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


class UserTestCase(TestCase):
    # def test_is_family_member(self):
    #     """ 
        
    #     is_family_member() should return TRUE if user sent as arg is:
    #     - ACTIVE 
    #     - contains the group 'member' 
    #     """
    #     # def is_family_member(user):
    #     #   if not user.is_active:
    #     #        return False
    #     #   return user.groups.filter(name='member').exists()

    def test_create_random_user(self):
        """ create_random_user() should:
        - return a user object which has 
            - a first name (string)
            - a last name (string)
            - a username in the form of an email (string)
            - a password (string)
        """
        test_user = create_random_user()
        self.assertEqual(type(test_user.first_name), str)
        self.assertEqual(type(test_user.last_name), str)
        self.assertEqual(type(test_user.username), str)
        self.assertEqual(type(test_user.password), str)
        self.assertIn('@', test_user.username)
        





        