import RPi.GPIO as GPIO
import logging


class Button:
    def __init__(self, gpio_number, lambda_press):
        self.lambda_press = lambda_press
        GPIO.setup(gpio_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(gpio_number, GPIO.RISING, callback=self.on_press, bouncetime=400)

    def on_press(self, channel):
        logging.info("Button pressed!")
        self.lambda_press()