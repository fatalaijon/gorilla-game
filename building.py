from gamelib import GameCanvasElement
import tkinter as tk
from random import random, randint

# Probability lights are on in a room in a building
PROB_LIGHTS = 0.8
LIGHT_WINDOW = "yellow2"
DARK_WINDOW = "gray40"
# Total guess as to height/width of windows, rooms, and floors
WIN_HEIGHT = 16
WIN_WIDTH = int(0.5*WIN_HEIGHT)
FLOOR_HEIGHT = 2*WIN_HEIGHT
ROOM_WIDTH = 2*WIN_WIDTH

class BuildingFactory:
    """Factory for buildings, of course."""

    @classmethod
    def create_buildings(cls, canvas):
        """Create buildings that fill the width of a canvas. Heights of 
        buildings are randomly chosen not to exceed about 70% of canvas height.
        This method uses canvas['width'] and canvas['height'] to get the canvas,
        since winfo_width() and winfo_height() don't return the correct sizes
        of the canvas hasn't been drawn yet.

        Returns:  list of Building objects
        """
        canvas_width = int(canvas['width'])
        canvas_height = int(canvas['height'])
        baseline = canvas_height
        # random colors for buildings
        bldg_colors = ["firebrick2", "cyan3", "gray80" ]
        x = 0
        buildings = []
        while x < canvas_width:
            width = ROOM_WIDTH*randint(5,9)
            # height not necessarily a multiple of floor height,
            # so windows don't all line up
            height = int( (0.4+random())*canvas_height/2 )
            color = bldg_colors[randint(0,len(bldg_colors)-1)]
            # cludge: don't use same color more than twice together
            bldg = Building(canvas, x, baseline, width, height, color)
            x = x + width
            buildings.append(bldg)
        return buildings

class Building(GameCanvasElement):
    """A building shown on the canvas.
    It has a width, height, color, and some randomly drawn windows.
    """

    def __init__(self, canvas, x, y, width, height, color):
        """Initialize a new building.
        Arguments:
            x - the left edge of the building
            y - the baseline of the building
            width - the building width
            height - the building height
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.canvas_object_id = self.init_canvas_object()
        self.is_visible = True

    # override canvas property from GameCanvasElement
    @property
    def canvas(self):
        return self._canvas
    
    @property
    def top(self):
        """y coordinate of the top of the building."""
        return self.y - self.height

    def init_canvas_object(self):
        # right edge of building
        xr = self.x + self.width
        ytop = self.y - self.height # coordinate system increases downward

        id = self.canvas.create_rectangle(self.x, self.y, xr, ytop, fill=self.color)
        self.make_windows(self.x, ytop)
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
                x = xleft + WIN_WIDTH + col*ROOM_WIDTH 
                # randomly choose lights on (LIGHT_WINDOW) or off (DARK_WINDOW)
                color = LIGHT_WINDOW if random() < PROB_LIGHTS else DARK_WINDOW
                # draw the window
                self.canvas.create_rectangle(x, y, 
                                             x+WIN_WIDTH, y+WIN_HEIGHT, 
                                             fill=color
                                             )
    def contains(self, x, y):
        return self.x < x < (self.x + self.width) and self.y-self.height < y < self.y

    def render(self):
        # no need to redraw or update a building
        pass

    def __str__(self):
        return f'{self.color} building'