from tkinter.constants import X
from gamelib import Sprite


class Monkey(Sprite):
    """A monkey that can throw bananas"""
    def __init__(self, game_app, image_filename, x=0, y=0):
        super().__init__(game_app, image_filename, x, y)

    def contains(self, x, y):
        """The point x,y is contained in the monkey's image if it
        hits any part of the `image.
        """
        w = self.image.width()
        h = self.image.height()
        dx = abs(x- self.x)
        dy = abs(y -self.y)
        if dx > w/2: return False
        if dy > w/2: return False
        # Exclude the 4 corners of bounding box of the image
        if dx > w/4 and dy > w/4: return False
        return True

    def init_element(self):
        # for debugging, draw a box around the monkey
        x = self.x
        y = self.y
        w = self.image.width()
        h = self.image.height()
        self.canvas.create_rectangle(x-w/2,y-h/2,x+w/2,y+h/2,outline='black')

    def __str__(self):
        return f"Monkey at (self.image.x,self.image.y)"