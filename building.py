from gamelib import GameCanvasElement, GameApp
import tkinter as tk

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
        ytop = self.y - self.height # coordinate system increased down
        id = self.canvas.create_rectangle(xl, self.y, xr, ytop, fill=self.color)
        # return the object_id
        return id

    def contains(self, x, y):
        return abs(x - self.x) < self.width/2 and self.y-self.height < y < self.y

    def render(self):
        pass

    def __str__(self):
        return f'{self.color} building'