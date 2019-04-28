from mpris_controller import MprisController
import RPi.GPIO as GPIO
import logging


class Button:
    gpio_initialized = False
    spotifyd_player = MprisController("spotifyd")
    mopidy_player = MprisController("mopidy")

    def __init__(self, gpio_number):
        GPIO.setup(gpio_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(gpio_number, GPIO.RISING, callback=self.on_press, bouncetime = 5000)

    def on_press(self, channel):
        logging.info("Button %s was pressed!" % self.__class__.__name__)

class PlayButton(Button):
    def __init__(self, gpio_number):
        Button.__init__(self, gpio_number)

    def on_press(self, channel):
        Button.on_press(self, channel)
        self.spotifyd_player.play_pause()


class NextButton(Button):
    def __init__(self, gpio_number):
        Button.__init__(self, gpio_number)

    def on_press(self, channel):
        Button.on_press(self, channel)
        self.spotifyd_player.next()


class PreviousButton(Button):
    def __init__(self, gpio_number):
        Button.__init__(self, gpio_number)

    def on_press(self, channel):
        Button.on_press(self, channel)
        self.spotifyd_player.previous()
