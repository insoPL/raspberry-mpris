# coding=utf-8

import RPi.GPIO as GPIO
from mpris_manager import MprisManger
from button import Button
import logging
import time

from lcd_manager import LcdManager

NEXT_BUTTON = 17
PLAY_BUTTON = 4
PREV_BUTTON = 16


def main():
    mpris_manager = MprisManger()
    next_button = Button(NEXT_BUTTON, lambda : mpris_manager.next_song())
    play_button = Button(PLAY_BUTTON, lambda : mpris_manager.play_pause())
    prev_button = Button(PREV_BUTTON, lambda : mpris_manager.previous_song())

    lcd_manager = LcdManager()

    while True:
        mpris_manager.check_player()
        meta = mpris_manager.get_meta()
        lcd_manager.set_by_meta(meta)
        time.sleep(1/2)

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    logging.info("GPIO successfully initiated")

    logging.getLogger().setLevel(logging.INFO)
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        LcdManager.close()
        GPIO.cleanup()
        logging.info("good bye")
