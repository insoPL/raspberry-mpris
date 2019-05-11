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

