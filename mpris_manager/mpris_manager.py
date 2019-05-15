import logging

from BtMprisController import BtMprisController
from mpris_controller import MprisController
from spotifyd_controller import SpotifydController


class MprisManger:
    def __init__(self,config):
        self.MAX_TIMEOUT = int(config["screen_saver_timeout"])
        self.last_player = "mopidy"
        self.all_paused = True
        self.timeout_timer = 1000000
        self.selfly_closed = False
        self.players = dict()
        self.players["BtMpris"] = BtMprisController("BtMpris")
        self.players["spotifyd"] = SpotifydController("spotifyd")
        self.players["mopidy"] = MprisController("mopidy")

    def check_player(self):
        self.all_paused = True
        for name, player in self.players.items():
            if player.get_status() == "playing":
                self.all_paused = False
                self.selfly_closed = False
                self.timeout_timer = 0
                if self.last_player != name:
                    self.players[self.last_player].pause()
                    self.players[self.last_player].quit()
                    self.last_player = name
                    logging.info("Currently rocking:" + self.last_player)
                    return
        if self.all_paused:
            self.timeout_timer+=1
        return

    def pause(self):
        self.players[self.last_player].pause()

    def play_pause(self):
        self.players[self.last_player].play_pause()

    def next_song(self):
        self.players[self.last_player].next_song()

    def previous_song(self):
        self.players[self.last_player].previous_song()

    def get_meta(self):
        self.check_player()
        if self.timeout_timer > self.MAX_TIMEOUT:
            if self.players[self.last_player].player is not None:
                self.players[self.last_player].quit()
            return "timeout"

        meta = list(self.players[self.last_player].get_meta())
        meta.append(self.last_player)
        meta.append(self.all_paused)
        return meta

