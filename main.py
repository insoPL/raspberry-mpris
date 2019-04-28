import RPi.GPIO as GPIO
from raspris import PreviousButton, PlayButton, NextButton

def main():
    play_button = PlayButton(38)
    next_button = NextButton(40)
    previous_button = PreviousButton(36)
    message = input("Press enter to quit\n\n")


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logging.info("GPIO successfully initiated")

    logging.getLogger().setLevel(logging.INFO)
    main()
    GPIO.cleanup()

