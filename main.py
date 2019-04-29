import RPi.GPIO as GPIO
from raspris import PreviousButton, PlayButton, NextButton, MprisController
import logging
import time


class MprisManger:
    def __init__(self):
        self.current_player = ""
        self.players = dict()
        self.players["spotifyd"] = MprisController("spotifyd")
        self.players["mopidy"] = MprisController("mopidy")

    def check_player(self):
        for name, player in self.players.items():
            if player.get_status == "Playing":
                if self.current_player == "":
                    self.current_player = name
                    return self.current_player
                elif self.current_player != name:
                    self.players[self.current_player].play_pause()
                    self.current_player = name
                    return self.current_player
        self.current_player = ""
        return self.current_player


def main():
    #play_button = PlayButton(38)
    #next_button = NextButton(40)
    #previous_button = PreviousButton(36)

    mpris_manager = MprisManger()

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
