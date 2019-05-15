# coding=utf-8

import logging
import time

import RPi.GPIO as GPIO
import configparser

from button import Button
from context_manager import ScreenSaverContext, PlayerContext
from lcd_manager import LcdManager
from mpris_manager import MprisManger

config = configparser.ConfigParser()
config.read('/home/pi/raspberry-mpris/config.ini')
config = config['main_options']

logging.getLogger().setLevel(logging.INFO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.info("GPIO successfully initiated")

mpris_manager = MprisManger(config)
next_button = Button(int(config["next_buttons"]), lambda : mpris_manager.next_song())
play_button = Button(int(config["play_buttons"]), lambda : mpris_manager.play_pause())
prev_button = Button(int(config["prev_buttons"]), lambda : mpris_manager.previous_song())

lcd_manager = LcdManager()

def_screen = ScreenSaverContext()
meta_player = PlayerContext()


def update_lcd():
    meta = mpris_manager.get_meta()
    if meta != "timeout":
        meta_player.set_by_meta(meta)
        lines = meta_player.get_lines()
    else:
        lines = def_screen.get_lines()
    lcd_manager.set_lines(*lines)
    lcd_manager.update()


def update_context():
    def_screen.update_furnace()
    def_screen.update_weather()


try:
    while True:
        update_lcd()

        if int(time.time()) % (60*int(config["furnace_update"])) == 0:
            update_context()  # Is making web requests so can take a while to execute, i should add threading

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)
except KeyboardInterrupt:
    pass
finally:
    lcd_manager.close()
    GPIO.cleanup()
    logging.info("good bye")
