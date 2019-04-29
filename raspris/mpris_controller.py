import dbus
import logging

class MprisManger:
    def __init__(self):
        self.current_player = "mopidy"
        self.silence = True
        self.players = dict()
        self.players["spotifyd"] = _MprisController("spotifyd")
        self.players["mopidy"] = _MprisController("mopidy")

    def check_player(self):
        no_player = True
        for name, player in self.players.items():
            if player.get_status() == "Playing":
                no_player = False
                if self.current_player != name:
                    self.players[self.current_player].play_pause()
                    self.current_player = name
                    logging.info("Currently rocking:" + self.current_player)
                    return self.current_player
        if no_player and not self.silence:
            logging.info("Currently silence")
            self.silence = True
        return self.current_player


    def play_pause(self):
        self.players[self.current_player].play_pause()

    def next_song(self):
        self.players[self.current_player].next_song()

    def previous_song(self):
        self.players[self.current_player].previous_song()

    def get_status(self):
        return self.players[self.current_player].get_status()

class _MprisController:
    def __init__(self, player_name):
        self.player_name = player_name
        if self.player_name != "mopidy" and self.player_name != "spotifyd": raise ValueError

        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.mpris.MediaPlayer2.'+self.player_name, '/org/mpris/MediaPlayer2')
        self.player = dbus.Interface(proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
        self.properties = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        logging.info("succesfully opened dbus for"+self.player_name)

    def play_pause(self):
        self.player.PlayPause()
        logging.info("[%s] Play/Paused" % self.player_name)

    def next_song(self):
        self.player.Next()
        logging.info("[%s] Next" % self.player_name)

    def previous_song(self):
        self.player.Previous()
        logging.info("[%s] Previous" % self.player_name)

    def get_status(self):
        return self._raw_property("PlaybackStatus")

    def _raw_property(self, name):
        meta = self.properties.Get('org.mpris.MediaPlayer2.Player', name)
        return meta
