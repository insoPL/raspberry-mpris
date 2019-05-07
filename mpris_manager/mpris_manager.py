from mpris_controller import MprisController
from BtMprisController import BtMprisController
import logging


class MprisManger:
    def __init__(self):
        self.last_player = "mopidy"
        self.silence = True
        self.players = dict()
        self.players["BtMpris"] = BtMprisController("BtMpris")
        self.players["spotifyd"] = MprisController("spotifyd")
        self.players["mopidy"] = MprisController("mopidy")

    def check_player(self):
        for name, player in self.players.items():
            if player.get_status() == "playing":
                if self.last_player != name:
                    self.players[self.last_player].pause()
                    self.last_player = name
                    logging.info("Currently rocking:" + self.last_player)
                    return self.last_player
        return self.last_player

    def pause(self):
        self.players[self.last_player].pause()

    def play_pause(self):
        self.players[self.last_player].play_pause()

    def next_song(self):
        self.players[self.last_player].next_song()

    def previous_song(self):
        self.players[self.last_player].previous_song()

    def get_status(self):
        return self.players[self.last_player].get_status()

    def get_meta(self):
        meta = list(self.players[self.last_player].get_meta())
        meta.append(self.last_player)
        return tuple(meta)
