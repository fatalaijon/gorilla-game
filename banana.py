import tkinter as tk
import math
from gamelib import Sprite
from monkey_game import CANVAS_WIDTH, CANVAS_HEIGHT, GRAVITY
from util import trace

class Banana(Sprite):
    """A banana that can be thrown at a player.  

    Before it is thrown, a banana has an initial speed and a direction
    that can be set as properties self.speed and self.angle.
    After the banna is thrown (and until it lands) it's velocity 
    is updated each time that update() is called, and cannot be altered
    externally.
    The banana remembers it's initial speed and direction for next throw.
    """
    # maximum initial speed of banana
    MAX_SPEED = 99

    def __init__(self, game_app, image_filename, x=0, y=0):
        super().__init__(game_app, image_filename, x, y)
        # create images for a spinning banana, by rotating existing image
        from PIL import Image
        image = Image.open(image_filename)
        self.images = [image]
        for angle in range(45,360,45):
            self.images.append( image.rotate(angle) )

    def init_element(self):
        self.vx = 0
        self.vy = 0

        self.start_x = self.x
        self.start_y = self.y
        # starting speed
        self._speed = 10
        # starting angle is in degrees
        self._angle = 0

        self.is_moving = False
        # image_index controls image selection (for animation)
        self.image_index = 0
        self.hide()
    
    @property
    def speed(self):
        """Get the initial speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        """Set the initial speed for next toss of banana.
        
        The speed must be between 0 and MAX_SPEED.
        """
        if 0 <= value <= Banana.MAX_SPEED:
            self._speed = value
    
    @property
    def angle(self):
        """Get the initial angle in degrees. 0 is horizontal."""
        return self._angle
    
    @angle.setter
    def angle(self, degrees):
        """Set the initial angle in degrees above horizontal."""
        self._angle = degrees

    def update(self):
        if self.is_moving:
            self.x += self.vx
            self.y -= self.vy
            self.vy -= GRAVITY
            # choose next image
            self.image_index = (self.image_index+1) % len(self.images)
            # paste function provided by ImageTk.PhotoImage class,
            # but it is "very slow" according to docs
            # pasted image must be same size as original image
            self.image.paste(self.images[self.image_index])

            if self.y > CANVAS_HEIGHT or not (0 <= self.x <= CANVAS_WIDTH):
                self.stop()
                self.hide()

    def reset(self):
        self.stop()
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0
        self.vy = 0

    def start(self):
        """Throw the banana, using the initial speed and angle."""
        self.show()
        self.is_moving = True
        angle = math.radians(self._angle)
        self.vx = math.cos(angle)*self._speed
        self.vy = math.sin(angle)*self._speed

    def stop(self):
        self.is_moving = False
    
    def hits(self, element) -> bool:
        """Test if the banana hits a game element."""
        if not self.is_moving:
            # a hit can occur only _after_ the banana is thrown
            return False
        x = self.x
        y = self.y
        # use actual image bounds or tighten to min as done here?
        r = min(self.image.width(), self.image.height())
        if element.contains(x,y): return True
        if element.contains(x+r,y) or element.contains(x-r,y): return True
        if element.contains(x,y-r) or element.contains(x,y+r): return True
        return False
    
    def __str__(self):
        return f"Banana at (self.x:.0f,self.y:.0f)"