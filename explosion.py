from tkinter.constants import X
from gamelib import GameCanvasElement


class Explosion(GameCanvasElement):
    """An explosion that destroys other objects as it expands,
    then contracts to nothing, leaving destruction behind.
    """
    # how much to grow or contract the explosion per time step
    EXPANSION_RATE = 10
    # number of steps to expand = number of steps to contact
    STEPS = 10
    def __init__(self, game_app, x=0, y=0):
        """Create an explosion centered at x, y."""
        self.radius = Explosion.EXPANSION_RATE
        self.step = 0
        # super constructor will call-back to init_canvas_object
        super().__init__(game_app, x, y)
        print("STEPS", Explosion.STEPS)
        print("EXPANSION_RATE", Explosion.EXPANSION_RATE)


    def contains(self, x, y):
        """Test if (x,y) is contained in the explosion.
        This is sort of irrelevant.
        """
        return False

    def init_canvas_object(self):
        # for debugging, draw a box around the monkey
        r = self.radius
        id = self.canvas.create_oval(self.x-r, self.y-r,self.x+r,self.y+r,
                    fill='red',
                    width=1,          # bprder width
                    outline="yellow"
                    )
        return id

    def update(self):
        """Update explosion, add one step to expansion,
        or contract one step.
        This uses the property:
        width = width of border drawn around oval.  1/2 of border 
           is inside the oval and 1/2 is drawn outside the oval.
        """
        self.step += 1
        if self.step < Explosion.STEPS:
            # expand the explosion by increasing the size of the border
            self.radius += Explosion.EXPANSION_RATE
            self.canvas.itemconfigure(self.canvas_object_id,
                    width=self.radius,
                    fill='red',
                    outline='tan'
                    )
            
        elif self.step == Explosion.STEPS:
            # at maximum size, replace explosion with a burned out
            # fireball of same size
            # first draw an oval having color of canvas background
            # and same size as the maximized oval.
            # Make original explosion invisible
            self.canvas.itemconfigure(self.canvas_object_id,
                    fill='',
                    outline='',
                    width=0
                    )
            # new oval in color of background
            r = self.EXPANSION_RATE * Explosion.STEPS/2
            self.canvas.create_oval(
                    self.x-r, self.y-r, self.x+r, self.y+r,
                    fill=self.canvas['bg'],
                    outline=self.canvas['bg'] 
                    )
            # burned out explosion
            self.canvas_object_id = self.canvas.create_oval(
                self.x-r, self.y-r, self.x+r, self.y+r,
                fill='tan4'
                )
        elif self.step < 2*Explosion.STEPS:
            # contract to nothing by creating a border in the color 
            # of the canvas background color
            #borderwidth = (self.step - Explosion.STEPS)*Explosion.EXPANSION_RATE   
            scale = 1 - (self.step - Explosion.STEPS)/Explosion.STEPS
            self.canvas.scale(self.canvas_object_id,
                    self.x,
                    self.y,
                    scale,
                    scale
                    )
            """
            # this using scaling to reduce the image,
            # but it didn't work as I hoped.
            self.canvas.scale(self.canvas_object_id,
                    self.x,
                    self.y,
                    scale,
                    scale
                    )
            """
        elif self.step == 2*Explosion.STEPS:
            # make it blend into canvas background
            self.canvas.itemconfigure(self.canvas_object_id,
                    fill=self.canvas['bg']
                    )
        else:
            # explosion has burned out. remove it
            self.app.remove_element(self)

        if self.step <= 2*Explosion.STEPS:
            print("step", self.step, "radius", self.radius)

    def render(self):
        """Render the explosion is done in update."""
        pass

    def __str__(self):
        return f"Explosion at (self.image.x,self.image.y)"
    
    @property
    def width(self):
        return self.radius
    
    @property
    def height(self):
        return self.radius