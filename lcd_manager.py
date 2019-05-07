from lcd_codes import *
import logging

class LcdManager:
    def __init__(self):
        lcd_init()
        self.line1 = "Welcome"
        self.line2 = "   Home"


    def set_text(self, line1, line2):
        self.line1 = line1
        self.line2 = line2
        self.update_screen()

    def update_screen(self):
        lcd_string(self.line1, LCD_LINE_1)
        lcd_string(self.line2, LCD_LINE_2)

    @staticmethod
    def close():
        lcd_byte(0x01, LCD_CMD)

    def set_by_meta(self, meta):
        def pretty_sec(time_in_sec):
            minutes = int(time_in_sec/60)
            seconds = int(time_in_sec%60)
            return "%i:%02d" % (minutes,seconds)

        title,artists, length, position, player = meta

        line1 = title+" - "+artists
        line2 = pretty_sec(position)+"/"+pretty_sec(length)+"  [%s]"%player[0].upper()
        self.set_text(line1, line2)