# coding=utf-8
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from unidecode import unidecode

class LcdManager:
    def __init__(self):
        self.lcd = CharLCD(pin_rs=20, pin_e=21, pins_data=[6, 13, 19, 26], auto_linebreaks=False, numbering_mode=GPIO.BCM, cols=16)

        self.line1 = "Welcome"
        self.line2 = "   Home"


    def set_text(self, line1, line2):
        self.line1 = line1
        self.line2 = line2
        self.update_screen()

    def update_screen(self):
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string(self.line1[:15])
        self.lcd.cursor_pos = (1,0)
        self.lcd.write_string(self.line2[:15])

    def close(self):
        self.lcd.close(clear=True)

    def set_by_meta(self, meta):
        def pretty_sec(time_in_sec):
            minutes = int(time_in_sec/60)
            seconds = int(time_in_sec%60)
            return "%i:%02d" % (minutes,seconds)

        title,artists, length, position, player = meta

        line1 = unidecode(title)+" - "+unidecode(artists)
        line2 = pretty_sec(position)+"/"+pretty_sec(length)+"  [%s]"%player[0].upper()
        self.set_text(line1, line2)
