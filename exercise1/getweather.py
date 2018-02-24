import os
import sys
import json
import requests

openweather_api_key = os.getenv('OPENWEATHER_API_KEY')
city_name = os.getenv('CITY_NAME', 'Bratislava')
base_url = 'https://api.openweathermap.org/data/2.5/weather'

if openweather_api_key is None:
    print('OPENWEATHER_API_KEY is not set. Exiting.')
    sys.exit(1)


def get_current_weather():
 
    headers = {'Content-Type': 'application/json'}

    api_url = '{0}?q={1}&units=metric&APPID={2}'.format(base_url, city_name, openweather_api_key)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def print_weather(current_weather):

    if current_weather is not None:
        city=current_weather['name']
        desc=current_weather['weather'][0]['description']
        temp=current_weather['main']['temp']
        humd=current_weather['main']['humidity']

        print('source=openweathermap, city="{0}", description="{1}", temp={2}, humidity={3}'.format(city, desc, temp, humd))
    else:
        print('Data not available.')


print_weather(get_current_weather())

