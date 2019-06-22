# coding=utf-8

import logging
import time

import RPi.GPIO as GPIO
import configparser

from button import Button
from context_manager import ScreenSaverContext, PlayerContext
from lcd_manager import LcdManager
from mpris_manager import MprisManger
from multiprocessing import Process, Manager

main_config = configparser.ConfigParser()
main_config.read('/home/pi/raspberry-mpris/config.ini')
config = main_config['main_options']

logging.getLogger().setLevel(logging.INFO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.info("GPIO successfully initiated")


def lcd_main_loop(meta,lcd_manager):
    def_screen = ScreenSaverContext(main_config)
    meta_player = PlayerContext()

    while True:
        if meta[0] != "timeout":
            meta_player.set_by_meta(meta)
            lines = meta_player.get_lines()
        else:
            lines = def_screen.get_lines()
        lcd_manager.set_lines(*lines)
        lcd_manager.update()

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)


def update_context():
    while True:
        def_screen.update_furnace()
        def_screen.update_weather()
        time.sleep(60 * int(config["weather_update"]))


def update_context_meta(meta):
    mpris_manager = MprisManger(main_config)
    next_button = Button(int(config["next_buttons"]), lambda: mpris_manager.next_song())
    play_button = Button(int(config["play_buttons"]), lambda: mpris_manager.play_pause())
    prev_button = Button(int(config["prev_buttons"]), lambda: mpris_manager.previous_song())

    while True:
        new_meta = mpris_manager.get_meta()
        if new_meta == "timeout":
            meta[0] = "timeout"
        else:
            for a,b in enumerate(new_meta):
                meta[a] = b

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)


if __name__ == '__main__':
    manager = Manager()
    lcd_manager = LcdManager(main_config)

    d = manager.list(["", "", 0, 0, "X", True])

    p = Process(target=lcd_main_loop, args=(d,lcd_manager))
   # p2 = Process(target=update_context)
    p3 = Process(target=update_context_meta, args=(d,))
    try:
        p.start()
        #p2.start()
        p3.start()
        p.join()
      #  p2.join()
        p3.join()
    except KeyboardInterrupt:
        pass
    finally:
        p.terminate()
       # p2.terminate()
        p3.terminate()
        lcd_manager.close()
      #  mpris_manager.players[mpris_manager.last_player].quit()
        GPIO.cleanup()
        logging.info("good bye")
