import logging
import dbus
from .dbus_tools import except_dbus_error

class BtMprisController:
    def __init__(self, player_name):
        self.player_name = player_name
        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.bluez', self._find_player_path())

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

    def get_status(self):
        return self._raw_property("Status").lower()

    def _raw_property(self, name):
        try:
            meta = self.properties.Get('org.bluez.MediaPlayer1', name)

        except dbus.exceptions.DBusException:
            return "Paused"

        return meta

    @except_dbus_error
    def _find_player_path(self):
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()
        objects = [str(key) for key in objects.keys() if str(key)[-7:] == "player0"]
        if len(objects) == 0:
            logging.warn("[%s] No Devices to connect" % self.player_name)
        else:
            return objects[0]