from sense_hat import SenseHat
from time import sleep


class Display:
    def __init__(self):
        self.sense = SenseHat()
        self.sense.show_message("System is ready", text_colour=(0, 0, 255))

    def show_checked_in(self):
        self.sense.clear()
        self.sense.show_message("Check In", text_colour=(0, 255, 0))

    def show_checked_out(self):
        self.sense.clear()
        self.sense.show_message("Check Out", text_colour=(255, 255, 0))

    def show_error(self):
        self.sense.clear()
        self.sense.show_message("Error", text_colour=(255, 0, 0))

    def show_loading(self):
        self.sense.show_message("Loading", text_colour=(230, 230, 250), scroll_speed=0.05)
        for i in range(1, 8):
            self.sense.set_rotation(i * 45)
            sleep(0.5)
