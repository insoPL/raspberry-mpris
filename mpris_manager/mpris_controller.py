import dbus
import logging
from dbus_tools import except_dbus_error


class MprisController:
    def __init__(self, player_name):
        self.player_name = player_name
        self.player = None
        self.properties = None

        if self.player_name != "mopidy" and self.player_name != "spotifyd": raise ValueError

        try:
            self.initialize()
        except dbus.exceptions.DBusException:
            pass

    def initialize(self):
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

    @except_dbus_error
    def get_status(self):
        return self._raw_property("PlaybackStatus").lower()

    def get_meta(self):
        def adjust_time_to_player(time):
            if self.player_name == "mopidy":
                time /= 1000000
            elif self.player_name == "spotifyd":
                time /= 1000
            return int(time)

        title, artists, length, position = "","","0","0"

        meta = self._raw_property("Metadata")
        assert isinstance(meta, dict)
        for key, value in meta.items():
            if "title" in key:
                title = value
            elif "artist" in key:
                artists = ", ".join(value)
            elif "length" in key:
                length = adjust_time_to_player(value)
        position = self._raw_property("Position")
        position = adjust_time_to_player(position)

        return title,artists, length, position

    def get_position(self):
        return self._raw_property("Position")

    def _raw_property(self, name):
        return self.properties.Get('org.mpris.MediaPlayer2.Player', name)
