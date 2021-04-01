from gamelib import GameCanvasElement, GameApp
import tkinter as tk
from random import random

# Probability lights are on in a room in a building
PROB_LIGHTS = 0.8
LIGHT_WINDOW = "yellow2"
DARK_WINDOW = "gray40"
# Total guess as to height/width of windows, rooms, and floors
WIN_HEIGHT = 16
WIN_WIDTH = int(0.5*WIN_HEIGHT)
FLOOR_HEIGHT = 2*WIN_HEIGHT
ROOM_WIDTH = 2*WIN_WIDTH

class Building(GameCanvasElement):
    """A building shown on the canvas.
    It has a width, height, color, and some randomly drawn windows.
    """

    def __init__(self, game_app: GameApp, x, y, width, height, color):
        """Initialize a new building.
        Arguments:
            x - the center of the building
            y - the baseline of the building
            width - the building width
            height - the building height
        """
        self.app = game_app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.canvas_object_id = self.init_canvas_object()
        self.is_visible = True

    def init_canvas_object(self):
        xl = self.x - self.width/2
        xr = self.x + self.width/2
        ytop = self.y - self.height # coordinate system increases downward

        id = self.canvas.create_rectangle(xl, self.y, xr, ytop, fill=self.color)
        self.make_windows(xl, ytop)
        # return the object_id
        return id

    def make_windows(self, xleft, ytop):    
        # How many floors can we fit only building?
        nfloors = self.height//FLOOR_HEIGHT
        # How many rooms per floor? (horizontal)
        nrooms = (self.width - WIN_WIDTH//2)//ROOM_WIDTH
        # In the original QBasic Gorilla game floors are aligned
        # starting from top of building, with excess space at the bottom
        for row in range(0,nfloors):
            # y coord of top edge of windows on this floor
            y = ytop + WIN_HEIGHT//2 + row*FLOOR_HEIGHT
            # x coord of individual windows
            for col in range(0, nrooms):
                x = xleft + WIN_WIDTH//2 + col*ROOM_WIDTH 
                # randomly choose lights on (yellow) or off (dark grey)
                color = LIGHT_WINDOW if random() < PROB_LIGHTS else DARK_WINDOW
                # draw a window
                self.canvas.create_rectangle(x, y, 
                                             x+WIN_WIDTH, y+WIN_HEIGHT, 
                                             fill=color
                                             )
    def contains(self, x, y):
        return abs(x - self.x) < self.width/2 and self.y-self.height < y < self.y

    def render(self):
        pass

    def __str__(self):
        return f'{self.color} building'