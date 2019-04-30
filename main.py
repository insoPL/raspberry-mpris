import RPi.GPIO as GPIO
from mpris_manager import MprisManger
from button import Button
import logging
import time


def main():
    mpris_manager = MprisManger()
    next_button = Button(40, lambda : mpris_manager.next_song())
    play_button = Button(38, lambda : mpris_manager.play_pause())
    prev_button = Button(36, lambda : mpris_manager.previous_song())

    while True:
        mpris_manager.check_player()
        time.sleep(1/2)

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logging.info("GPIO successfully initiated")

    logging.getLogger().setLevel(logging.INFO)
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        logging.info("good bye")
