import logging

class BtMprisController:
    def __init__(self, player_name):
        self.player_name = player_name
        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.bluez', '/org/bluez/hci0/dev_D0_13_FD_92_78_B9/player0')
        self.player = dbus.Interface(proxy, dbus_interface='org.bluez.MediaPlayer1')
        self.properties = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        logging.info("succesfully opened dbus for"+self.player_name)

    def play_pause(self):
        if self.get_status() == "playing":
            self.player.Pause()
        else:
            self.player.Play()
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
        return self._raw_property("Status").lower()

    def _raw_property(self, name):
        meta = self.properties.Get('org.bluez.MediaPlayer1', name)
        return meta
