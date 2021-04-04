import tkinter as tk
from gamelib import Sprite
import game_constants as config

# show the bounding box around monkey image, for development
SHOW_BOUNDING_BOX = False

class Monkey(Sprite):
    """A monkey that can throw bananas"""
    def __init__(self, game_app, image_filename, x=0, y=0):
        super().__init__(game_app, image_filename, x, y)
        self._name = "Monkey"
        # Adjust y for height of image so that y is at bottom of image

    def init_element(self):
        self.canvas.itemconfigure(self.canvas_object_id,
                    anchor=tk.S
                    )
        # add a tag for identifying and selecting monkeys on the canvas
        self.canvas.addtag_withtag(config.GORILLA, self.canvas_object_id)
        if SHOW_BOUNDING_BOX:
            (xl, yl, xr, yr) = self.canvas.bbox(self.canvas_object_id)
            self.canvas.create_rectangle(xl, yl, xr, yr, outline='grey')

    def contains(self, x, y):
        """The point x,y is contained in the monkey's image if it
        hits any part of the `image.
        """
        w = self.width
        h = self.height
        # More reliable to use canvas.bbox(self.canvas_object_id)
        # instead of relying on our own notion of image location.
        (xl, yl, xr, yr) = self.canvas.bbox(self.canvas_object_id)
        dx = abs(x - (xl+xr)/2)
        dy = abs(y - (yl+yr)/2)
        if dx > w/2: return False
        if dy > h/2: return False
        # Exclude the 4 corners of bounding box of the image
        # This is empty space not occupied by the monkey image
        if dx > w/4 and dy > h/4: return False
        return True

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    def __str__(self):
        return f"Monkey at ({self.x},{self.y})"
