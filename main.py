# coding=utf-8

import RPi.GPIO as GPIO
from mpris_manager import MprisManger
from button import Button
import logging
import time
from timeloop import Timeloop
from datetime import timedelta

from lcd_manager import LcdManager

NEXT_BUTTON = 17 # BCM Pins for buttons
PLAY_BUTTON = 4
PREV_BUTTON = 16

logging.getLogger().setLevel(logging.INFO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.info("GPIO successfully initiated")

mpris_manager = MprisManger()
next_button = Button(NEXT_BUTTON, lambda : mpris_manager.next_song())
play_button = Button(PLAY_BUTTON, lambda : mpris_manager.play_pause())
prev_button = Button(PREV_BUTTON, lambda : mpris_manager.previous_song())

lcd_manager = LcdManager()

tl = Timeloop()

@tl.job(interval=timedelta(seconds=1))
def main():
    mpris_manager.check_player()

@tl.job(interval=timedelta(seconds=5))
def show_song_info():
    meta = mpris_manager.get_meta()
    lcd_manager.set_by_meta(meta)

@tl.job(interval=timedelta(seconds=1))
def update_screen():
    lcd_manager.update()

tl.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    tl.stop()
    lcd_manager.close()
    GPIO.cleanup()
    logging.info("good bye")
