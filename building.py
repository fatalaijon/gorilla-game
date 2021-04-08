from gamelib import GameCanvasElement
import tkinter as tk
from random import random, randint

# Probability lights are on in a room in a building
PROB_LIGHT_ON = 0.8
LIGHT_WINDOW = "yellow2"
DARK_WINDOW = "gray35"
# Min and Max building height, as a fraction of the canvas height
BLDG_MIN_HEIGHT = 0.2
BLDG_MAX_HEIGHT = 0.7
# Building colors, of course
BLDG_COLORS = ["firebrick3", "cyan3", "gray80", "light slate gray", "navajo white" ]
# Arbitrary guess as to height/width of windows, rooms, and floors
WIN_HEIGHT = 16
WIN_WIDTH = WIN_HEIGHT//2
FLOOR_HEIGHT = 2*WIN_HEIGHT
ROOM_WIDTH = 2*WIN_WIDTH
# Minimum/maximum number of rooms (windows) per floor. 
# Must be wide enough for gorilla to stand on.
MIN_ROOMS = 5
MAX_ROOMS = 8


class BuildingFactory:
    """Factory for buildings, of course."""

    @classmethod
    def create_buildings(cls, canvas):
        """Create buildings that fill the width of a canvas. Heights of 
        buildings are randomly chosen not to exceed about 70% of canvas height.
        This method uses canvas['width'] and canvas['height'] to get the canvas size,
        since winfo_width() and winfo_height() don't return the correct sizes
        of the canvas if it hasn't been drawn yet.

        Returns:  list of Building objects
        """
        canvas_width = int(canvas['width'])
        canvas_height = int(canvas['height'])
        baseline = canvas_height
        min_bldg_width = MIN_ROOMS*ROOM_WIDTH
        x = 0
        buildings = []
        while x < canvas_width:
            width = ROOM_WIDTH*randint(MIN_ROOMS,MAX_ROOMS) + randint(0, WIN_WIDTH)
            # fill the width of canvas with complete buildings
            if x + width + min_bldg_width > canvas_width:
                # when remaining width is too small, expand bldg to fill the remaining space
                width = canvas_width - x
            # building height not necessarily a multiple of floor height,
            # so that windows in different buildings don't all line up
            height = int( canvas_height * ( BLDG_MIN_HEIGHT 
                            + random()*(BLDG_MAX_HEIGHT-BLDG_MIN_HEIGHT) )
                        )
            color = BuildingFactory.choose_color(buildings)
            bldg = Building(canvas, x, baseline, width, height, color)
            x = x + width
            buildings.append(bldg)
        return buildings

    @classmethod
    def choose_color(cls, buildings):
        """Choose a random color for the next building to draw,
        but avoid too many consecutive buildings of same color.
        """
        n = len(buildings) - 1
        color = BLDG_COLORS[randint(0, len(BLDG_COLORS) - 1)]
        # testing: use all colors sequentially
        #color = bldg_colors[n % len(bldg_colors)]
        if n >= 0 and color == buildings[n].color:
            # Boring. Too many buildings of same color.
            return BuildingFactory.choose_color(buildings)
        return color


class Building(GameCanvasElement):
    """A building shown on the canvas.
    It has a width, height, color, and some randomly lit windows.
    """

    def __init__(self, canvas, x, y, width, height, color):
        """Initialize a new building.
        Arguments:
            x - the left edge of the building
            y - the baseline of the building
            width - the building width
            height - the building height
            color - color of the building
        """
        self.width = width
        self.height = height
        self.color = color
        super().__init__(canvas, x, y)
        # called by GameCanvasElement onstructor
        #self.canvas_object_id = self.init_canvas_object()
    
    @property
    def top(self):
        """y coordinate of the top of the building."""
        return self.y - self.height

    def init_canvas_object(self):
        """Draw a building with windows."""
        xright = self.x + self.width
        ytop = self.y - self.height # coordinate system increases downward

        object_id = self.canvas.create_rectangle(self.x, self.y, xright, ytop, fill=self.color)
        self.make_windows(self.x, ytop)
        # return the object id
        return object_id

    def make_windows(self, xleft, ytop):
        """Draw windows in the building."""
        # How many floors can we fit only building?
        nfloors = self.height//FLOOR_HEIGHT
        # How many rooms per floor? (horizontal)
        nrooms = (self.width - WIN_WIDTH//2)//ROOM_WIDTH
        # In the original QBasic Gorilla game, the windows are aligned
        # starting from top of building, with excess space at the bottom
        for row in range(0,nfloors):
            # y coord of top edge of windows on this floor
            y = ytop + WIN_HEIGHT//2 + row*FLOOR_HEIGHT
            # x coord of individual windows
            for col in range(0, nrooms):
                x = xleft + WIN_WIDTH + col*ROOM_WIDTH 
                # randomly choose lights on (LIGHT_WINDOW) or off (DARK_WINDOW)
                color = LIGHT_WINDOW if random() < PROB_LIGHT_ON else DARK_WINDOW
                # draw the window
                self.canvas.create_rectangle(
                        x, y, 
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
