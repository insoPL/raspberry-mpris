import RPi.GPIO as GPIO
from raspris import PreviousButton, PlayButton, NextButton, MprisController
import logging
import time


class MprisManger:
    def __init__(self):
        self.current_player = ""
        self.spotifyd_player = MprisController("spotifyd")
        self.mopidy_player = MprisController("mopidy")

    def check_player(self):
        status = str(self.spotifyd_player.get_status())
        logging.info(status)
        status = str(self.mopidy_player.get_status())
        logging.info(status)


def main():
    #play_button = PlayButton(38)
    #next_button = NextButton(40)
    #previous_button = PreviousButton(36)

    mpris_manager = MprisMangager()

    while True:
        print(mpris_manager.check_player())
        time.sleep(5)

if __name__ == '__main__':
    #GPIO.setwarnings(False)
    #GPIO.setmode(GPIO.BOARD)
    #logging.info("GPIO successfully initiated")

    logging.getLogger().setLevel(logging.INFO)
    main()
    #GPIO.cleanup()
