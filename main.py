import RPi.GPIO as GPIO
from raspris import PreviousButton, PlayButton, NextButton, MprisController
import logging
import time


def main():
    #play_button = PlayButton(38)
    #next_button = NextButton(40)
    #previous_button = PreviousButton(36)

    spotifyd_player = MprisController("spotifyd")
    mopidy_player = MprisController("mopidy")

    while True:
        print(mopidy_player.get_status())
        time.sleep(1)

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logging.info("GPIO successfully initiated")

    logging.getLogger().setLevel(logging.INFO)
    main()
    GPIO.cleanup()
