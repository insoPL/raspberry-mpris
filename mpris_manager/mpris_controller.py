import dbus
import logging
from .dbus_tools import except_dbus_error

class MprisController:
    def __init__(self, player_name):
        self.player_name = player_name
        if self.player_name != "mopidy" and self.player_name != "spotifyd": raise ValueError

        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.mpris.MediaPlayer2.'+self.player_name, '/org/mpris/MediaPlayer2')
        self.player = dbus.Interface(proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
        self.properties = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        logging.info("succesfully opened dbus for"+self.player_name)

    @except_dbus_error
    def play_pause(self):
        self.player.PlayPause()
        logging.info("[%s] Play/Paused" % self.player_name)

    @except_dbus_error
    def pause(self):
        self.player.Pause()
        logging.info("[%s] Paused" % self.player_name)

    @except_dbus_error
    def next_song(self):
        self.player.Next()
        logging.info("[%s] Next" % self.player_name)

    @except_dbus_error
    def previous_song(self):
        self.player.Previous()
        logging.info("[%s] Previous" % self.player_name)

    def get_status(self):
        return self._raw_property("PlaybackStatus").lower()

    def _raw_property(self, name):
        try:
            meta = self.properties.Get('org.mpris.MediaPlayer2.Player', name)
        except dbus.exceptions.DBusException:
            return "Paused"

        return meta
