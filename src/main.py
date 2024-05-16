__author__ = 'Felix Goebel'

import time

from app import App
from controller import Controller
from log import logging
from serial import SerialException
from scenario import *


# MAIN PROGRAMM
if __name__ == '__main__':

    # App & GUI setup
    min_width = 640
    min_height = 480

    app = App(min_width, min_height)
    port_controller = Controller()

    # Sets ignore duplicates, useful here since the arduino sometimes sends duplicate bytes on button press
    combination = set()

    while app.running:
        app.update()  
        try:
            # Convert received bytes and add to the combination set
            if port_controller.arduino.in_waiting > 0:
                selection = ord(port_controller.arduino.readline())
                logging.info(f'Data received -> {selection}')
                combination.add(selection)
            
            # If a combination of two scenarios has been selected, display a corresponding AI image
            if len(combination) == 2:
                selected = Scenario.select(combination)
                app.choose_topic(selected)
                combination.clear()
        
        # Serial Disconnection Handling
        except SerialException:
            # Only log the first disconnection and reset the image
            if port_controller.arduino.is_open:
                logging.error("The Arduino disconnected.")
                combination.clear()
                port_controller.arduino.close()
            # otherwise jsut try to reconnect
            port_controller.reconnect()

        # Debugging
        except:
            logging.error(f"Something else went wrong.")

        # Optional, but recommended since other threads can run during this time
        time.sleep(.01)