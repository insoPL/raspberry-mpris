import logging
from functools import wraps

import dbus


def except_dbus_error(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        self = args[0]
        try:
            if self.player is None or self.properties is None:
                raise dbus.exceptions.DBusException
            return func(*args, **kwargs)
        except dbus.exceptions.DBusException:
            try:
                self.initialize()
                return func(*args, **kwargs)
            except dbus.exceptions.DBusException:
                return None
    return func_wrapper

class BtMprisController:
    def __init__(self, player_name):
        self.player_name = player_name
        self.player = None
        self.properties = None
        try:
            self.initialize()
        except dbus.exceptions.DBusException:
            pass

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
    def pause(self):
        self.player.Pause()
        logging.info("[%s] Pause dbus sent" % self.player_name)

    @except_dbus_error
    def next_song(self):
        self.player.Next()
        logging.info("[%s] Next dbus sent" % self.player_name)

    @except_dbus_error
    def previous_song(self):
        self.player.Previous()
        logging.info("[%s] Previous dbus sent" % self.player_name)

    @except_dbus_error
    def get_status(self):
            return self._raw_property("Status")

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

        if title == "":
            logging.warn("empty meta")

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