from unidecode import unidecode


class MetaPlayer:
    def __init__(self):
        self.title = ""
        self.artists = ""
        self.length = 0
        self.position = 0
        self.player = "X"
        self.status = ""

    def set_by_meta(self,meta):
        self.title, self.artists, self.length, self.position = meta

    def get_timer_line(self):
        self.position += 1
        return self._pretty_sec(self.position) + "/" + self._pretty_sec(self.length) + "  [%s]" % self.player[0].upper()

    def get_player_line(self):
        return " - ".join((unidecode(self.title), unidecode(self.artists)))

    def _pretty_sec(self, time_in_sec):
        time_in_sec = int(time_in_sec)
        minutes = int(time_in_sec / 60)
        seconds = int(time_in_sec % 60)
        return "%i:%02d" % (minutes, seconds)
