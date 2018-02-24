import os
import sys
import pyowm

owm_api_key = os.getenv('OPENWEATHER_API_KEY')
city_name = os.getenv('CITY_NAME', 'Bratislava')
base_url = 'https://api.openweathermap.org/data/2.5/weather'

if owm_api_key is None:
    print('OPENWEATHER_API_KEY is not set. Exiting.')
    sys.exit(1)

owm = pyowm.OWM(owm_api_key)
observation = owm.weather_at_place(city_name)
w = observation.get_weather()

print('source=openweathermap, city="{0}", description="{1}", temp={2}, humidity={3}'.format(city_name, w.get_detailed_status(), w.get_temperature('celsius')['temp'], w.get_humidity()))

