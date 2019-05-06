from lcd_codes import *

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