# coding=utf-8

import RPi.GPIO as GPIO
from mpris_manager import MprisManger
from lcd_manager import LcdManager
from button import Button
import logging
import time
from timeloop import Timeloop
from datetime import timedelta

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

@tl.job(interval=timedelta(seconds=1))
def update_lcd():
    timer_line = mpris_manager.meta_player.get_timer_line()
    player_line = mpris_manager.meta_player.get_player_line()
    lcd_manager.set_lines(timer_line, player_line)
    lcd_manager.update()

@tl.job(interval=timedelta(seconds=10))
def force_update_manager():
    mpris_manager.update_meta()

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
