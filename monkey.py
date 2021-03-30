from tkinter.constants import X
from gamelib import Sprite

# show the bounding box around monkey image, for development
SHOW_BOUNDING_BOX = False

class Monkey(Sprite):
    """A monkey that can throw bananas"""
    def __init__(self, game_app, image_filename, x=0, y=0):
        super().__init__(game_app, image_filename, x, y)

    def contains(self, x, y):
        """The point x,y is contained in the monkey's image if it
        hits any part of the `image.
        """
        w = self.width
        h = self.height
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        if dx > w/2: return False
        if dy > h/2: return False
        # Exclude the 4 corners of bounding box of the image
        # This is empty space not occupied by the monkey
        if dx > w/4 and dy > h/4: return False
        return True

    def init_element(self):
        """For debugging, draw a box around the monkey."""
        if SHOW_BOUNDING_BOX:
            (xl,yl,xr,yr) = self.canvas.bbox(self.canvas_object_id)
            self.canvas.create_rectangle(xl, yl, xr, yr, outline='grey')

    def __str__(self):
        return f"Monkey at (self.image.x,self.image.y)"
