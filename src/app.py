__author__ = 'Felix A. Goebel'

import time
import tkinter as tk

from datetime import datetime
from log import logging
from PIL import Image, ImageTk
from scenario import Scenario


class App(tk.Tk):
    
    # App constructor with constants and imagelabel as well as keybindings
    def __init__(self, min_width, min_height):
        
        super().__init__()
        self.running = True

        self.MIN_WIDTH = min_width
        self.MIN_HEIGHT = min_height
        self.SCREEN_WIDTH = self.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.winfo_screenheight()

        self.title("Kinderbiennale 2024")
        self.geometry(f'{self.MIN_WIDTH}x{self.MIN_HEIGHT}')
        self.attributes("-fullscreen", True)
        self.wm_protocol("WM_DELETE_WINDOW", self._quit)
        
        self.image = self.RESET_IMAGE = Image.open('./images/Canaletto.jpg')
        resized_image = self.image.resize((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), Image.Resampling.LANCZOS)
        
        self.photo = ImageTk.PhotoImage(resized_image)

        self.label = tk.Label(self, image=self.photo)
        self.label.pack()

        self.bind('<Key>', self.on_key_press)
        self.config(cursor='none')

    # Quit on pressing 'x' in the title bar
    def _quit(self):
        logging.info(f'Exiting...')
        self.running = False
        
        
    # Function: Enter/ leave fullscreen mode or exit
    def on_key_press(self, event) -> None:
        if event.char == 'f':
            self.enter_leave_fullscreen()
            self.resize_Image()
        elif event.keysym == 'Escape':
            self._quit()

    # Function: Fit window to screen size with in-built tkinter properties
    def enter_leave_fullscreen(self) -> None:
        if self.attributes('-fullscreen'):
            self.attributes('-fullscreen', False)
        else:
            self.attributes('-fullscreen', True)

    # Function: Resizing the window
    def resize_Image(self) -> None:
        width, height = self.get_app_size()
        logging.info(f'Resizing to {width}x{height}')
        
        img = self.image.resize((width, height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.label.config(image=photo)
        self.label.image = photo
    
    # Choose a topic
    def choose_topic(self, scenario : Scenario) -> None:
        logging.info(f'Beginning to crossfade...\n{scenario}')
        width, height = self.get_app_size()
        
        image = Image.open(scenario.image_list[scenario.index]) # pick an image at the current index (scenario - image list)
        
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS) # resize that image to fit the current screen size 
        resized_current_image = self.RESET_IMAGE.resize((width, height), Image.Resampling.LANCZOS) # resize the currently displayed image
        
        # Calculate delta time dynamically (varies with the resolution) to sync with 20s delatime 
        start = datetime.now()
        self.blend_images(resized_current_image, resized_image)  
        end = datetime.now()
        delta_time = (end - start).total_seconds()
        time.sleep(20.0 - delta_time*2) # wait for 20 s then reset
        self.blend_images(resized_image, resized_current_image)
        scenario.index += 1
        # Reset object/ scenario index if all images have been displayed (display all images inside the ai folders sequentially - largest interval between two identical images -> helps to preserve the illusion that the images are not pre-created)
        if scenario.index == len(scenario.image_list):
            scenario.index = 0
        logging.info(f'Crossfading and reset completed.')


    # Function: Crossfade two AI images
    def blend_images(self, from_image, to_image) -> None:
        alpha = .0
        while alpha < 1.0:
            img_blended = Image.blend(from_image, to_image, alpha = alpha)
            photo = ImageTk.PhotoImage(img_blended)
            self.label.config(image = photo)
            self.label.image = photo
            self.label.update()
            alpha += self.get_animation_speed()

    def get_app_size(self) -> tuple[int, int]:
        if self.attributes('-fullscreen'):
            width, height = self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        else:
            width, height = self.MIN_WIDTH, self.MIN_HEIGHT, 
        return width, height
    
    # set animation speed accordingly
    def get_animation_speed(self) -> float:
        if self.get_app_size()[0] > 2000:
            return .02
        elif self.get_app_size()[0] > 1000:
            return .01
        else:
            return 0.001
    
