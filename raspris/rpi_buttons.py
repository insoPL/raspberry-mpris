import RPi.GPIO as GPIO
import logging


class Button:
    def __init__(self, gpio_number, mpris_manager):
        self.mpris_manager = mpris_manager
        GPIO.setup(gpio_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(gpio_number, GPIO.RISING, callback=self.on_press, bouncetime=200)

    def on_press(self, channel):
        logging.info("Button %s was pressed!" % self.__class__.__name__)


class PlayButton(Button):
    def __init__(self, gpio_number, mpris_manager):
        Button.__init__(self, gpio_number, mpris_manager)

    def on_press(self, channel):
        Button.on_press(self, channel)
        self.mpris_manager.play_pause()


class NextButton(Button):
    def __init__(self, gpio_number, mpris_manager):
        Button.__init__(self, gpio_number, mpris_manager)

    def on_press(self, channel):
        Button.on_press(self, channel)
        self.mpris_manager.next_song()


class PreviousButton(Button):
    def __init__(self, gpio_number, mpris_manager):
        Button.__init__(self, gpio_number, mpris_manager)

    def on_press(self, channel):
        Button.on_press(self, channel)
        self.mpris_manager.previous_song()
