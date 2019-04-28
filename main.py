from rpi_buttons import PlayButton, NextButton, PreviousButton
import logging

def main():
    play_button = PlayButton(38)
    next_button = NextButton(40)
    previous_button = PreviousButton(36)
    message = input("Press enter to quit\n\n")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    main()
