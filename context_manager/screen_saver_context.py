import logging
import time
from xml.etree import ElementTree

import requests
import w1thermsensor
from requests.auth import HTTPBasicAuth
from unidecode import unidecode


class ScreenSaverContext:
    def __init__(self, config):
        self.config = config['screen_saver']

        self.temp = ""
        self.desc = ""
        self.co = 0

        self.update_weather()
        self.update_thermometer()

    def get_lines(self):
        return self.get_time_line(), self.get_weather_line()

    def get_time_line(self):
        time_string = time.strftime("%d/%m %H:%M", time.localtime())
        return time_string+" "+str(self.co)

    def get_weather_line(self):
        return self.desc + " " + str(self.temp) + '\x02'

    def update_weather(self):
        api_key = self.config["openweathermap_key"]
        location = self.config["location"]
        lang = self.config["lang"]
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}".format(location, api_key, lang)

        try:
            r = requests.get(url)
            j = r.json()

            self.desc = unidecode(j['weather'][0]['description']).capitalize()
            self.temp = int(j['main']['temp'])
        except requests.exceptions.RequestException:
            logging.warn("Cant reach weather service")
            self.desc = "Weather service unavailable"
            self.temp = "N/A"

    def update_thermometer(self):
        sensor = w1thermsensor.W1ThermSensor()
        temp = sensor.get_temperature()
        temp = str(int(temp))+'\x02'
        self.co = temp

    def update_thermometer_from_furnace(self):
        fur_ip = self.config["furnace_ip"]
        fur_user = self.config["furnace_username"]
        fur_pass = self.config["furnace_pass"]

        auth = HTTPBasicAuth(fur_user, fur_pass)
        try:
            ret = requests.get('http://' + fur_ip + '/getregister.cgi?device=0&tkot_value', auth=auth)
        except requests.exceptions.RequestException:
            logging.warn("Cant reach CO2 furnace")
            self.co = "N/A"
            return

        xml_ret = ElementTree.fromstring(ret.content)
        co_temp = int(float(xml_ret[0][0].get("v")))
        self.co = str(co_temp)+'\x02'
