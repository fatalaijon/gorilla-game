import tkinter as tk

class Building:
    """A building shown on the canvas.
    It has a width, height, color, and some randomly drawn windows.
    """

    def __init__(self, canvas: tk.Canvas, x, y, width, height, color):
        """Initialize a new building.
        Arguments:
            x - the center of the building
            y - the baseline of the building
            width - the building width
            height - the building height
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.init_canvas_object()

    def init_canvas_object(self):
        xl = self.x - self.width/2
        xr = self.x + self.width/2
        ytop = self.y - self.height # coordinate system increased down
        self.id = self.canvas.create_rectangle(xl, self.y, xr, ytop, fill=self.color)
        # return the object_id
        return id
