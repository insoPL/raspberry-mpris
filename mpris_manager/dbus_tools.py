from functools import wraps
import logging
import dbus

def except_dbus_error(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):

        try:
           return func(*args, **kwargs)

        except dbus.exceptions.DBusException:
            logging.warn("[%s] Dbus device not found"%args[0].player_name)
            return None

    return func_wrapper