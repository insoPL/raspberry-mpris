# coding=utf-8
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from unidecode import unidecode
from moving_line import Line

class LcdManager:
    LCD_WIDTH = 16
    def __init__(self):
        self.lcd = CharLCD(pin_rs=20, pin_e=21, pins_data=[6, 13, 19, 26], auto_linebreaks=True, numbering_mode=GPIO.BCM, cols=self.LCD_WIDTH)

        self.lines = [
            Line('This string is too long to fit', self.LCD_WIDTH),
            Line('test', self.LCD_WIDTH)
        ]

    def close(self):
        self.lcd.close(clear=True)

    def set_by_meta(self, meta):
        def pretty_sec(time_in_sec):
            minutes = int(time_in_sec/60)
            seconds = int(time_in_sec%60)
            return "%i:%02d" % (minutes,seconds)

        title,artists, length, position, player = meta

        self.lines[0].set_text(" - ".join((unidecode(title),unidecode(artists))))
        self.lines[1].set_text(pretty_sec(position)+"/"+pretty_sec(length)+"  [%s]" % player[0].upper())

    def update(self):
        i = 0
        for line in self.lines:
            self.lcd.cursor_pos = (i, 0)
            self.lcd.write_string(str(line))
            i += 1
