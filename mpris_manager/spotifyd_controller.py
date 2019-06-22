from mpris_controller import MprisController
import logging
import dbus


class SpotifydController(MprisController):

    @staticmethod
    def adjust_time_to_player(time):
        return int(time / 1000)

    def quit(self):
        if self.player_name is None or self.properties is None: return
        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.mpris.MediaPlayer2.'+self.player_name, '/org/mpris/MediaPlayer2')
        main_dbus = dbus.Interface(proxy, dbus_interface='org.mpris.MediaPlayer2')

        try:
            main_dbus.Quit()
        except dbus.exceptions.DBusException:
            pass

        self.player = None
        self.properties = None
        logging.info("[%s] Quit" % self.player_name)
