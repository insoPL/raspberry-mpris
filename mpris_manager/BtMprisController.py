import logging
import dbus
from dbus_tools import except_dbus_error
from .mpris_controller import MprisController


class BtMprisController(MprisController):
    def __init__(self, player_name):
        MprisController.__init__(self, player_name)

    def initialize(self):
        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.bluez',self._find_player_path())
        self.player = dbus.Interface(proxy, dbus_interface='org.bluez.MediaPlayer1')
        self.properties = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        logging.info("succesfully opened dbus for"+self.player_name)

    @except_dbus_error
    def play_pause(self):
        if self.get_status() == "playing":
            self.player.Pause()
            logging.info("[%s] Pause dbus sent" % self.player_name)
        else:
            self.player.Play()
            logging.info("[%s] Play dbus sent" % self.player_name)

    @except_dbus_error
    def get_status(self):
        return self._raw_property("Status").lower()

    @except_dbus_error
    def get_meta(self):
        def adjust_time_to_player(time):
            time /= 1000
            return int(time)

        title, artists, length, position = "","","0","0"

        meta = self._raw_property("Track")
        assert isinstance(meta, dict)
        for key, value in meta.items():
            if "Title" in key:
                title = value
            elif "Artist" in key:
                artists = value
            elif "Duration" in key:
                length = adjust_time_to_player(value)
        position = self._raw_property("Position")
        position = adjust_time_to_player(position)

        return title,artists, length, position

    def _raw_property(self, name):
        return self.properties.Get('org.bluez.MediaPlayer1', name)

    def _find_player_path(self):
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()
        objects = [str(key) for key in objects.keys() if str(key)[-7:] == "player0"]
        if len(objects) == 0:
            raise dbus.exceptions.DBusException
        else:
            return objects[0]
