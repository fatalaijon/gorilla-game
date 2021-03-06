import tkinter as tk
import tkinter.ttk as ttk
# use ImageTk for improved PhotoImage class
from PIL import ImageTk


class GameCanvasElement:
    """An element on the game canvas, with attributes:

    x = x-coord of image
    y = y-coord of image
    canvas = reference to the game canvas
    canvas_object_id = id of the object, used to manipulate it using canvas
    is_visible = boolean flag if element is visible.

    By default the (x,y) coordinate are at the center of the image,
    but this can be changed by subclasses or calls to canvas.itemconfigure().
    """

    def __init__(self, canvas, x=0, y=0, **kwargs):
        self.x = x
        self.y = y
        # Modified: save reference to game_app instead of game_app.canvas
        #self.app = game_app
        self._canvas = canvas
        self.is_visible = True
        self.canvas_object_id = self.init_canvas_object(**kwargs)
        self.init_element()

    def init_canvas_object(self, **kwargs) -> int:
        """Initialize a graphical object to show on self.canvas.
        This method must return the canvas_object_id of the object.
        """
        return 0

    def init_element(self):
        """Initialize the state of the element.
        Use this method for things other than creating the canvas object.
        """
        pass

    @property
    def canvas(self):
        """Return a reference to the game app's canvas."""
        return self._canvas

    def show(self):
        self.is_visible = True
        self.canvas.itemconfigure(self.canvas_object_id, state=tk.NORMAL)

    def hide(self):
        self.is_visible = False
        self.canvas.itemconfigure(self.canvas_object_id, state=tk.HIDDEN)

    def render(self):
        if self.is_visible:
            self.canvas.coords(self.canvas_object_id, self.x, self.y)

    def update(self):
        pass

    def contains(self, x, y):
        """Test if the game element contains point x,y in its image or its 'space'.

        Returns: True if (x,y) is inside the object's image or region.
        """
        (xl,yl, xr,yr) = self.canvas.bbox(self.canvas_object_id)
        return xl <= x <= xr and min(yl,yr) <= y <= max(yl,yr)


class Text(GameCanvasElement):
    """Some text displayed on the game canvas."""

    def __init__(self, canvas, text, x=0, y=0, **kwargs):
        self.text = text
        super().__init__(canvas, x, y, **kwargs)

    def init_canvas_object(self, **kwargs):
        object_id = self.canvas.create_text(
                self.x,
                self.y,
                text=self.text,
                **kwargs)
        return object_id

    def set_text(self, text):
        self.text = text
        self._canvas.itemconfigure(self.canvas_object_id, text=text)

    def append_text(self, text):
        self.set_text(self.text + text)

    def set_color(self, color):
        self._canvas.itemconfigure(self.canvas_object_id, color=color)


class Sprite(GameCanvasElement):
    """A canvas element with an image."""

    def __init__(self, canvas, image_filename, x=0, y=0):
        self.image_filename = image_filename
        super().__init__(canvas, x, y)

    def init_canvas_object(self):
        #self.image = tk.PhotoImage(file=self.image_filename)
        self.image = ImageTk.PhotoImage(file=self.image_filename)
        object_id = self.canvas.create_image(
                self.x,
                self.y,
                image=self.image)
        return object_id

    @property
    def height(self):
        """Return the height of the Sprite's image."""
        return self.image.height() if self.image else 0

    @property
    def width(self):
        """Return the width of the Sprite's image."""
        return self.image.width() if self.image else 0


class GameApp(ttk.Frame):
    """Base class for a game.  This class creates a canvas
    and provides several call-back methods for initializing elements
    on the canvas, start/stop animation, and running the animation loop.
    """
    def __init__(self, parent, canvas_width, canvas_height, update_delay=33):
        super().__init__(parent, width=canvas_width, height=canvas_height)
        self.parent = parent
        self.update_delay = update_delay
        # row 0 is the canvas, row 1 for controls and text
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)

        self.grid(sticky=tk.NSEW)
        self.canvas = self.create_canvas(canvas_width, canvas_height)
        # The timer_id keeps a reference to the animation timer.
        # It is empty string if timer is stopped.
        self.timer_id = ""
        self.elements = []
        self.init_game()
        # bind callback for event handlers
        self.parent.bind('<KeyPress>', self.on_key_pressed)
        self.parent.bind('<KeyRelease>', self.on_key_released)

    def create_canvas(self, canvas_width, canvas_height) -> tk.Canvas:
        canvas = tk.Canvas(self,
                           borderwidth=0,
                           width=canvas_width,
                           height=canvas_height,
                           highlightthickness=0)
        canvas.grid(row=0, sticky=tk.NSEW)
        return canvas

    def add_element(self, element):
        """Add an element to list of animated elements. 
        Element should be an object with update() and render() methods,
        such as a GameCanvasElement.
        """
        if not element in self.elements:
            self.elements.append(element)

    def remove_element(self, element):
        """Remove an element from the canvas and list of animated elements."""
        if element in self.elements:
            self.elements.remove(element)
        self.canvas.delete(element.canvas_object_id)

    def animate(self):
        """Animate each element on the canvas.

        A subclass may override this to provide it's own animation.
        A subclass should be careful to set self.timer_id to the value
        returned by animate().
        """
        for element in self.elements:
            element.update()
            element.render()

        self.timer_id = self.after(self.update_delay, self.animate)

    def start(self):
        """Start the animation loop if not already running."""
        if not self.timer_id:
            self.timer_id = self.after(0, self.animate)

    def stop(self):
        """Stop the animation loop."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = ""

    def stopped(self) -> bool:
        """Test if the animation loop has been stopped."""
        return not self.timer_id

    def running(self) -> bool:
        """Return True if animation is running, False otherwise."""
        return self.timer_id != ""

    def init_game(self):
        pass

    def on_key_pressed(self, event):
        pass

    def on_key_released(self, event):
        pass
