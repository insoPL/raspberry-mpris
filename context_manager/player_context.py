from unidecode import unidecode


class PlayerContext:
    def __init__(self):
        self.title = ""
        self.artists = ""
        self.length = 0
        self.position = 0
        self.player = "X"
        self.all_paused = True

    def set_by_meta(self,meta):
        self.title, self.artists, self.length, new_position, last_player, all_paused = meta
        self.player = last_player
        self.all_paused = all_paused
        if abs(self.position-new_position)>3:
            self.position=new_position

    def get_lines(self):
        if not self.all_paused:
            self.position += 1
        return self.get_player_line(), self.get_timer_line()

    def get_timer_line(self):
        if self.all_paused:
            playing_status = '\x01'
        else:
            playing_status = '\x00'

        timer_str = self._pretty_sec(self.position) + "/" + self._pretty_sec(self.length)
        player_str = "[%s]" % self.player[0].upper()
        return (playing_status+" "+timer_str+" "+player_str).center(16)

    def get_player_line(self):
        return " - ".join((unidecode(self.title), unidecode(self.artists)))

    def _pretty_sec(self, time_in_sec):
        time_in_sec = int(time_in_sec)
        minutes = int(time_in_sec / 60)
        seconds = int(time_in_sec % 60)
        return "%i:%02d" % (minutes, seconds)
