import time
import w1thermsensor


class ScreenSaverContext:
    def __init__(self, config):
        self.config = config['screen_saver']

        self.temp = ""
        self.desc = ""
        self.co = ""

    def get_lines(self):
        return self.get_time_line(), self.get_weather_line()

    def get_time_line(self):
        time_string = time.strftime("%d/%m %H:%M", time.localtime())
        return time_string + " " + self.co + '\x02'

    def get_weather_line(self):
        return self.desc + " " + self.temp + '\x02'

    def set_weather_data(self, weather_data):
        self.desc = weather_data[0]
        self.temp = weather_data[1]
        self.co = weather_data[2]
