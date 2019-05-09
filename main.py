# coding=utf-8

import RPi.GPIO as GPIO
from mpris_manager import MprisManger
from lcd_manager import LcdManager
from button import Button
import logging
import time
from timeloop import Timeloop
from datetime import timedelta
from context_manager import ScreenSaverContext, PlayerContext

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

def_screen = ScreenSaverContext()
meta_player = PlayerContext()

tl = Timeloop()


@tl.job(interval=timedelta(seconds=1))
def update_lcd():
    mpris_manager.check_player()
    if mpris_manager.timeout_timer<1:
        meta = mpris_manager.get_meta()
        meta_player.set_by_meta(meta)
        lines = meta_player.get_lines()
    else:
        lines = def_screen.get_lines()
    lcd_manager.set_lines(*lines)
    lcd_manager.update()


@tl.job(interval=timedelta(minutes=5))
def update_context():
    def_screen.update_furnce()
    def_screen.update_weather()

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
