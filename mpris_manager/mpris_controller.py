import dbus
import logging

class MprisController:
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

    def pause(self):
        self.player.Pause()
        logging.info("[%s] Paused" % self.player_name)

    def next_song(self):
        self.player.Next()
        logging.info("[%s] Next" % self.player_name)

    def previous_song(self):
        self.player.Previous()
        logging.info("[%s] Previous" % self.player_name)

    def get_status(self):
        return self._raw_property("PlaybackStatus").lower()

    def _raw_property(self, name):
        meta = self.properties.Get('org.mpris.MediaPlayer2.Player', name)
        return meta