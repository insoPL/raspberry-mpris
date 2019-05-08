# coding=utf-8
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

from text_line import TextLine

class LcdManager:
    LCD_WIDTH = 16
    def __init__(self):
        self.lcd = CharLCD(pin_rs=20, pin_e=21, pins_data=[6, 13, 19, 26], auto_linebreaks=True, numbering_mode=GPIO.BCM, cols=self.LCD_WIDTH)

        self.lines = [
            TextLine('This string is too long to fit', self.LCD_WIDTH),
            TextLine('test', self.LCD_WIDTH)
        ]

    def close(self):
        self.lcd.close(clear=True)

    def set_lines(self, line, line2):
        self.lines[0] = TextLine(line2, self.LCD_WIDTH)
        self.lines[1] = TextLine(line, self.LCD_WIDTH)

    def update(self):
        i = 0
        for line in self.lines:
            self.lcd.cursor_pos = (i, 0)
            self.lcd.write_string(str(line))
            i += 1
