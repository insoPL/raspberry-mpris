import logging

import requests
from unidecode import unidecode


def download_weather_data(config):
    config = config["weather"]
    api_key = config["openweathermap_key"]
    location = config["location"]
    lang = config["lang"]
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}" \
        .format(location, api_key, lang)

    try:
        r = requests.get(url)
        j = r.json()

        desc = unidecode(j['weather'][0]['description']).capitalize()
        temp = str(int(j['main']['temp']))
    except requests.exceptions.RequestException:
        logging.warn("Cant reach weather service")
        desc = "Weather service unavailable"
        temp = "N/A"
    finally:
        return desc, temp
