from unidecode import unidecode


class PlayerContext:
    def __init__(self):
        self.title = ""
        self.artists = ""
        self.length = 0
        self.position = 0
        self.player = "X"
        self.all_paused = True
        self.is_stopped = True

    def set_by_meta(self, meta):
        if meta is not None:
            self.title, self.artists, self.length, new_position, self.player, self.all_paused, self.is_stopped = meta
            if abs(self.position - new_position) > 3:
                self.position = new_position

    def get_lines(self):
        if not self.all_paused and self.length > self.position:
            self.position += 1
        return self.get_player_line(), self.get_timer_line()

    def get_timer_line(self):
        if self.all_paused:
            playing_status = '\x01'
        else:
            playing_status = '\x00'

        timer_str = self._pretty_sec(self.position) + "/" + self._pretty_sec(self.length)
        player_str = "[%s]" % self.player[0].upper()
        return playing_status + " " + timer_str + " " + player_str

    def get_player_line(self):
        title = unidecode(self.title)
        artists = unidecode(self.artists)
        if title == "":
            return artists
        else:
            return " - ".join((title, artists))

    def _pretty_sec(self, time_in_sec):
        time_in_sec = int(time_in_sec)
        minutes = int(time_in_sec / 60)
        seconds = int(time_in_sec % 60)
        return "%i:%02d" % (minutes, seconds)
