import logging

from BtMprisController import BtMprisController
from mpris_controller import MprisController
from spotifyd_controller import SpotifydController


class MprisManger:
    def __init__(self, config):
        config = config['main_options']
        self.MAX_TIMEOUT = int(config["screen_saver_timeout"])
        self.last_player_name = "mopidy"
        self.all_paused = True
        self.timeout_timer = 1000000
        self.selfly_closed = False
        self.players = dict()
       # self.players["BtMpris"] = BtMprisController("BtMpris")
        self.players["spotifyd"] = SpotifydController("spotifyd")
        self.players["mopidy"] = MprisController("mopidy")

    @property
    def last_player(self):
        return self.players[self.last_player_name]

    def check_player(self):
        self.all_paused = True
        for name, player in self.players.items():
            if player.get_status() == "playing":
                self.all_paused = False
                self.selfly_closed = False
                self.timeout_timer = 0
                if self.last_player_name != name:
                    self.last_player.pause()
                    self.last_player.quit()
                    self.last_player_name = name
                    logging.info("Currently rocking:" + self.last_player_name)
                    return
        if self.all_paused:
            self.timeout_timer+=1
        return

    def pause(self):
        self.last_player.pause()

    def play_pause(self):
        self.last_player.play_pause()

    def next_song(self):
        self.last_player.next_song()

    def previous_song(self):
        self.last_player.previous_song()

    def get_meta(self):
        """
        Fetches title, artists, length, position, last_player_name, all_paused from current mpris player

        :return: song title, names of artists,  song length, current playing position, last active player name, is playing paused
        :rtype:  (str, unicode, int, int, str, bool)
        """
        self.check_player()

        if self.timeout_timer > self.MAX_TIMEOUT:
            if self.last_player.player is not None:
                self.last_player.quit()
            stopped = True
        else:
            stopped = False

        title, artists, length, position = self.last_player.get_meta()

        return title, artists, length, position, self.last_player_name, self.all_paused, stopped
