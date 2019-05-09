import logging

import requests
import time
import configparser

from requests.auth import HTTPBasicAuth
from unidecode import unidecode


class ScreenSaverContext:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.config = config['screen_saver']

        self.temp = ""
        self.desc = ""
        self.co = 0
        self.update_weather()
        self.update_furnce()

    def get_lines(self):
        return self.get_time_line(), self.get_weather_line()

    def get_time_line(self):
        time_string = time.strftime("%H:%M %d/%m", time.localtime())
        return time_string+" "+str(self.co)+'\x02'

    def get_weather_line(self):
        return self.desc + " "+ str(self.temp)+'\x02'

    def update_weather(self):
        api_key = self.config["openweathermap_key"]
        location = self.config["location"]
        lang = self.config["lang"]
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}".format(location, api_key, lang)
        r = requests.get(url)
        j = r.json()
        self.desc = unidecode(j['weather'][0]['description'])
        self.temp = int(j['main']['temp'])

    def update_furnce(self):
        ip = self.config["furnace_ip"]
        user = self.config["furnace_username"]
        passwd = self.config["furnace_pass"]

        try:
            self.co = requests.get('http://' + ip + '/getregister.cgi?device=0&tkot_value', auth=HTTPBasicAuth(user, passwd))
        except requests.exceptions.ConnectionError:
            logging.warn("Cant reach CO2 furnace")
            self.co = "N/A"
