# coding=utf-8
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from register_char import register_char

from text_line import TextLine

class LcdManager:
    LCD_WIDTH = 16
    def __init__(self):
        self.lcd = CharLCD(pin_rs=20, pin_e=21, pins_data=[6, 13, 19, 26], auto_linebreaks=True, numbering_mode=GPIO.BCM, cols=self.LCD_WIDTH)

        for foo, bar in zip(range(len(register_char)),register_char):
            self.lcd.create_char(foo,bar)

        self.lines = [
            TextLine('This string is too long to fit', self.LCD_WIDTH),
            TextLine('test', self.LCD_WIDTH)
        ]

    def close(self):
        self.lcd.close(clear=True)

    def set_lines(self, line, line2):
        self.lines[0].set_text(line)
        self.lines[1].set_text(line2)

    def update(self):
        i = 0
        for line in self.lines:
            self.lcd.cursor_pos = (i, 0)
            self.lcd.write_string(str(line).ljust(16))
            i += 1
