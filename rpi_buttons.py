from mpris_controller import MprisController
import RPi.GPIO as GPIO
import logging


class Button:
    gpio_initialized = False
    spotifyd_player = MprisController("spotifyd")
    mopidy_player = MprisController("mopidy")
    def __init__(self, gpio_number):
        if not self.gpio_initialized:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            self.gpio_initialized = True
            logging.info("GPIO successfully initiated")
        GPIO.setup(gpio_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(gpio_number, GPIO.RISING, callback=self.on_press)

    def on_press(self):
        logging.info("Button %s was pressed!" % self.__class__.__name__)

    def __del__(self):
        logging.info("Cleaning GPIO")
        GPIO.cleanup()


class PlayButton(Button):
    def __init__(self, gpio_number):
        super().__init__(gpio_number)

    def on_press(self):
        super().on_press()
        self.spotifyd_player.play_pause()


class NextButton(Button):
    def __init__(self, gpio_number):
        super().__init__(gpio_number)

    def on_press(self):
        super().on_press()
        self.spotifyd_player.next()


class PreviousButton(Button):
    def __init__(self, gpio_number):
        super().__init__(gpio_number)

    def on_press(self):
        super().on_press()
        self.spotifyd_player.previous()