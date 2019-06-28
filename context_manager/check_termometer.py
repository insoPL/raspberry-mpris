import w1thermsensor


def check_thermometer():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    return str(int(temp))

# def update_thermometer_from_furnace(self):
#     fur_ip = self.config["furnace_ip"]
#     fur_user = self.config["furnace_username"]
#     fur_pass = self.config["furnace_pass"]
#
#     auth = HTTPBasicAuth(fur_user, fur_pass)
#     try:
#         ret = requests.get('http://' + fur_ip + '/getregister.cgi?device=0&tkot_value', auth=auth)
#     except requests.exceptions.RequestException:
#         logging.warn("Cant reach CO2 furnace")
#         self.co = "N/A"
#         return
#
#     xml_ret = ElementTree.fromstring(ret.content)
#     co_temp = int(float(xml_ret[0][0].get("v")))
#     self.co = str(co_temp) + '\x02'
