import tkinter as tk
from gamelib import Sprite
import game_constants as config
from banana import Banana

# show the bounding box around monkey image, for development
SHOW_BOUNDING_BOX = False

class Monkey(Sprite):
    """A monkey that can throw bananas.
    Each monkey owns a reusable banana, so that the banana remembers
    it initial speed and angle between throws.
    """
    def __init__(self, canvas, image_filename, x=0, y=0):
        super().__init__(canvas, image_filename, x, y)
        self._name = "Monkey"
        # every monkey has a banana, of course
        # The initial position of each banana is above the monkey's head
        banana_x = x
        banana_y = y - self.height - 10  # 10 pixels above monkey
        self._banana = Banana(canvas, 'images/banana.png', banana_x, banana_y)

    def init_element(self):
        # Adjust y for height of image so that y is at bottom of image
        self.canvas.itemconfigure(self.canvas_object_id,
                    anchor=tk.S    # self.y is at the bottom of monkey image.
                    )
        # add a tag for identifying and selecting monkeys on the canvas
        self.canvas.addtag_withtag(config.GORILLA, self.canvas_object_id)
        if SHOW_BOUNDING_BOX:
            (xl, yl, xr, yr) = self.canvas.bbox(self.canvas_object_id)
            self.canvas.create_rectangle(xl, yl, xr, yr, outline='grey')

    def contains(self, x, y):
        """The point x,y is contained in the monkey's image if it
        hits any part of the image.  Exclude empty space at corners.
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

    def move_to(self, x, y):
        """Move the player's image to canvas (x,y).
        This also moves the starting position of a banana toss.
        """
        dx = x - self.x
        dy = y - self.y
        # canvas.move parameters are offsets (deltas) from current positioin
        self.canvas.move(self.canvas_object_id, dx, dy)
        self.x = x
        self.y = y
        # move the banana too, of course.
        self.canvas.move(self.banana.canvas_object_id, dx, dy)
        self.banana.start_x += dx
        self.banana.start_y += dy

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def banana(self):
        return self._banana

    @banana.setter
    def banana(self, value):
        """Set the Monkey's banana. The argument must be a Banana reference."""
        self._banana = value
        
    def __str__(self):
        return f"{self._name}"
