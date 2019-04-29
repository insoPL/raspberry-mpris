import RPi.GPIO as GPIO
from raspris import PreviousButton, PlayButton, NextButton, MprisManger
import logging
import time


def main():
    mpris_manager = MprisManger()

    play_button = PlayButton(38, mpris_manager)
    next_button = NextButton(36, mpris_manager)
    previous_button = PreviousButton(40, mpris_manager)

    while True:
        mpris_manager.check_player()
        time.sleep(3)

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
