import tkinter as tk
import tkinter.ttk as ttk
# use ImageTk for improved PhotoImage class
from PIL import ImageTk

class GameCanvasElement:
    """An element on the game canvas, with attributes:

    x = x-coord of approximate center of image
    y = y-coord of approximate center of image
    canvas = reference to the game canvas
    canvas_object_id = id of the object, used to manipulate it using canvas
    is_visible = boolean flag if element is visible
    """
    def __init__(self, game_app, x=0, y=0):
        self.x = x
        self.y = y
        self.canvas: tk.Canvas = game_app.canvas

        self.is_visible = True

        self.canvas_object_id = self.init_canvas_object()
        self.init_element()

    def show(self):
        self.is_visible = True
        self.canvas.itemconfigure(self.canvas_object_id, state=tk.NORMAL)

    def hide(self):
        self.is_visible = False
        self.canvas.itemconfigure(self.canvas_object_id, state=tk.HIDDEN)

    def render(self):
        if self.is_visible:
            self.canvas.coords(self.canvas_object_id, self.x, self.y)

    def init_canvas_object(self) -> int:
        """Initialize a graphical object to show on self.canvas.
        Your code must return the canvas_object_id.
        """
        return 0

    def init_element(self):
        """Initialize the state of the element.
        Use this method for things other than creating the canvas object.
        """
        pass

    def update(self):
        pass

    def contains(self, x, y):
        """Test if the game element contains point x,y in its image or its 'space'.
        
        Returns: True if (x,y) is inside the object's image or region.
        """
        return False


class Text(GameCanvasElement):
    def __init__(self, game_app, text, x=0, y=0, **kwargs):
        self.text = text
        self.x = x
        self.y = y
        self.canvas = game_app.canvas
        self.is_visible = True
        self.canvas_object_id = self.init_canvas_object(**kwargs)

    def init_canvas_object(self, **kwargs):
        object_id = self.canvas.create_text(
                    self.x, 
                    self.y,
                    text=self.text,
                    **kwargs)
        return object_id

    def set_text(self, text):
        self.text = text
        self.canvas.itemconfigure(self.canvas_object_id, text=text)
    
    def append_text(self, text):
        self.set_text(self.text + text)
        
    def set_color(self, color):
        self.canvas.itemconfigure(self.canvas_object_id, color=color)
        

class Sprite(GameCanvasElement):
    """A canvas element with an image."""
    def __init__(self, game_app, image_filename, x=0, y=0):
        self.image_filename = image_filename
        super().__init__(game_app, x, y)

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
        return self.image.height()

    @property
    def width(self):
        """Return the width of the Sprite's image."""
        return self.image.width()


class GameApp(ttk.Frame): 
    def __init__(self, parent, canvas_width=800, canvas_height=500, update_delay=33):
        super().__init__(parent)
        self.parent = parent
        self.update_delay = update_delay
        # row 0 is the canvas, row 1 for controls and text
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)

        self.grid(sticky=tk.NSEW)
        self.canvas = self.create_canvas(canvas_width, canvas_height)

        self.elements = []
        self.init_game()

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
        """Add an element to the canvas. Element should be an object
        with update() and render() methods.
        """
        if not element in self.elements:
            print("Append element", element)
            self.elements.append(element)

    def remove_element(self, element):
        """Remove an element from the canvas."""
        self.elements.remove(element)

    def animate(self):
        """Animate each element on the canvas.
        
        A subclass may override this to provide it's own animation.
        """
        for element in self.elements:
            element.update()
            element.render()

        self.after(self.update_delay, self.animate)

    def start(self):
        self.after(0, self.animate)

    def init_game(self):
        pass

    def on_key_pressed(self, event):
        pass

    def on_key_released(self, event):
        pass
