# coding=utf-8

import logging
import time

import RPi.GPIO as GPIO
import configparser

from button import Button
from context_manager import ScreenSaverContext, PlayerContext
from lcd_manager import LcdManager
from mpris_manager import MprisManger
import multiprocessing

config = configparser.ConfigParser()
config.read('/home/pi/raspberry-mpris/config.ini')
main_config = config['main_options']

logging.getLogger().setLevel(logging.INFO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.info("GPIO successfully initiated")


def lcd_main_loop(song_metadata, lcd_manager):
    def_screen = ScreenSaverContext(config)
    meta_player = PlayerContext()
    while True:
        if song_metadata[6]:
            lines = def_screen.get_lines()
        else:
            meta_player.set_by_meta(song_metadata)
            lines = meta_player.get_lines()
        lcd_manager.set_lines(*lines)
        lcd_manager.update()

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)


def update_context():
    while True:
        def_screen.update_thermometer()
        def_screen.update_weather()
        time.sleep(60 * int(main_config["weather_update"]))


def update_context_meta(song_metadata):
    mpris_manager = MprisManger(config)
    next_button = Button(int(main_config["next_buttons"]), lambda: mpris_manager.next_song())
    play_button = Button(int(main_config["play_buttons"]), lambda: mpris_manager.play_pause())
    prev_button = Button(int(main_config["prev_buttons"]), lambda: mpris_manager.previous_song())

    while True:
        new_meta = mpris_manager.get_meta()
        for a,b in enumerate(new_meta):
            song_metadata[a] = b

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)


if __name__ == '__main__':
    process_manager = multiprocessing.Manager()
    lcd_manager = LcdManager(config)

    manager = multiprocessing.Manager()
    song_metadata = manager.list(["", "", 0, 0, "X", True, True])

    lcd_screen_update_process = multiprocessing.Process(target=lcd_main_loop, args=(song_metadata, lcd_manager))
    meta_update_process = multiprocessing.Process(target=update_context_meta, args=(song_metadata,))

    try:
        lcd_screen_update_process.start()
        meta_update_process.start()

        lcd_screen_update_process.join()
        meta_update_process.join()

    except KeyboardInterrupt:
        pass

    finally:
        lcd_screen_update_process.terminate()
        meta_update_process.terminate()
        lcd_manager.close()
        GPIO.cleanup()
        logging.info("good bye")
