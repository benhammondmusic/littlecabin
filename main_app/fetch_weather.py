from decouple import config
import requests as api_requests

WEATHER_KEY = config('WEATHER_KEY')
LOCATION = 'zip=04051'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?{LOCATION}&units=imperial&appid={WEATHER_KEY}'


def update_current_weather():

    weather_response = api_requests.get(WEATHER_URL).json()
    # weather_response = {'coord': {'lon': -70.93, 'lat': 44.1614}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 70.69, 'feels_like': 293.5, 'temp_min': 293.71, 'temp_max': 296.15, 'pressure': 1020, 'humidity': 23}, 'visibility': 10000, 'wind': {'speed': 4.12, 'deg': 310}, 'rain': {'1h': 0.12}, 'clouds': {'all': 40}, 'dt': 1621014921, 'sys': {'type': 1, 'id': 4567, 'country': 'US', 'sunrise': 1620983884, 'sunset': 1621036933}, 'timezone': -14400, 'id': 0, 'name': 'Lovell', 'cod': 200}

    current_conditions = weather_response["weather"][0]["description"]
    current_temp = int(weather_response["main"]["temp"])
    print("***WEATHER***", current_conditions, current_temp)
    return {"conditions": current_conditions, "temp": current_temp}
    #  &deg;









"""  SAMPLE RESPONSE
{
     "coord": {"lon": -122.08,"lat": 37.39},
     "weather": [
       {
         "id": 800,
         "main": "Clear",
         "description": "clear sky",
         "icon": "01d"
       }
     ],
     "base": "stations",
     "main": {
       "temp": 282.55,
       "feels_like": 281.86,
       "temp_min": 280.37,
       "temp_max": 284.26,
       "pressure": 1023,
       "humidity": 100
     },
     "visibility": 16093,
     "wind": {
       "speed": 1.5,
       "deg": 350
     },
     "clouds": {
       "all": 1
     },
     "dt": 1560350645,
     "sys": {
       "type": 1,
       "id": 5122,
       "message": 0.0139,
       "country": "US",
       "sunrise": 1560343627,
       "sunset": 1560396563
     },
     "timezone": -25200,
     "id": 420006353,
     "name": "Mountain View",
     "cod": 200
     }
      """