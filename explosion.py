import math
from tkinter.constants import X
from gamelib import GameCanvasElement


class Explosion(GameCanvasElement):
    """An explosion that destroys other objects as it expands,
    then contracts to nothing, leaving a hole behind.
    """
    # how much to grow or contract the explosion per time step
    EXPANSION_RATE = 4
    # number of steps to expand = number of steps to contact
    STEPS = 10
    # Cludge!  canvas.itermconfigure(id, fill=color, outline=color)
    # throws exception if I specify colors as hex strings, e.g. 'xff0000' for red.
    # As a work-around, specify colors by name for each step 0..STEPS
    COLORS = [
              'yellow', 'yellow', 
              'orange red','red', 'red', 'red2','red3',
              'sienna3','sienna4',
              'brown4','saddle brown']

    def __init__(self, game_app, x=0, y=0):
        """Create an explosion centered at x, y."""
        self.radius = Explosion.EXPANSION_RATE
        self.step = 0
        # object that was hit to cause explosion
        self.hits = None
        # super constructor will call-back to init_canvas_object
        super().__init__(game_app, x, y)

    def contains(self, x, y):
        """Test if (x,y) is contained in the explosion.
        This is used so bananas can pass through the holes left
        by previous explosions.
        """
        r = math.hypot(x - self.x, y - self.y)
        return r <= self.radius

    def init_canvas_object(self):
        r = self.radius
        id = self.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r,
                    fill=self.color_for_step(0)
                    )
        return id

    def update(self):
        """Update explosion, expand or contract one step.
        This uses the property:
        width = width of border drawn around oval.  1/2 of border 
           is inside the oval and 1/2 is drawn outside the oval.
        """
        self.step += 1
        if self.step < Explosion.STEPS:
            # expand the explosion by increasing the size of the border
            self.radius += Explosion.EXPANSION_RATE
            color = self.color_for_step(self.step)
            self.canvas.itemconfigure(self.canvas_object_id,
                    width=2*self.radius,  # width is 1/2 inside, 1/2 outside
                    outline=color
                    )
            
        elif self.step == Explosion.STEPS:
            # When explosion reaches its maximum size, replace the
            # explosion with a burned out fireball that contracts.
            self.canvas.delete(self.canvas_object_id)
            # Size of new oval in color of canvas background
            self.radius = self.EXPANSION_RATE * Explosion.STEPS
            r = self.radius
            # First draw an oval having the color of canvas background
            # and same size as the maximized explosion.
            self.canvas.create_oval(
                    self.x-r, self.y-r, self.x+r, self.y+r,
                    fill=self.canvas['bg'],
                    outline=self.canvas['bg'] 
                    )
            # Cover it with a burned out explosion.
            color = self.color_for_step(self.step)
            self.canvas_object_id = self.canvas.create_oval(
                self.x-r, self.y-r, self.x+r, self.y+r,
                fill=color
                )
        elif self.step < 2*Explosion.STEPS:
            # Contract to nothing.
            # Can be done by increase border width or scaling the image,
            # but scaling the image works better and is simpler.
            scale = 1 - (self.step - Explosion.STEPS)/Explosion.STEPS
            self.canvas.scale(self.canvas_object_id,
                    self.x,
                    self.y,
                    scale,
                    scale
                    )
        elif self.step == 2*Explosion.STEPS:
            # Last step. Remove the burned out explosion.
            self.canvas.delete(self.canvas_object_id)
            # remove it from GameApp so it won't be updated again
            # Not necessary.
            #self.app.remove_element(self)

    def color_for_step(self, step):
        """Color to use for explosion at a given step during expansion."""

        """
        This code changes the color by decreasing RED and increasing G & B.
        But itemconfigure throws exception when I specify colors as 'xRRGGBB'.

        R_START = 255
        R_FINISH = 128
        GB_START = 0
        GB_FINISH = 60
        red = int(R_START + (R_FINISH - R_START)*step/Explosion.STEPS)
        gb  = int(GB_START + (GB_FINISH - GB_START)*step/Explosion.STEPS)
        hexcolor = hex((red<<16) + (gb<<8) + gb)
        # tkinter throws exception of hex string begins with 0 (expects 'xRRGGBB')
        if hexcolor[0] == '0': 
            return hexcolor[1:]
        return hexcolor
        """
        return Explosion.COLORS[min(step,len(Explosion.COLORS)-1)]

    def render(self):
        """Rendering done in update, but this method is needed to override
        the default render in GameCanvasElement.
        """
        pass

    def is_exploding(self):
        """Test if the explosion is still occurring."""
        return self.step < 2*Explosion.STEPS

    def __str__(self):
        return f"Explosion at (self.image.x,self.image.y)"
    
    @property
    def width(self):
        return self.radius
    
    @property
    def height(self):
        return self.radius
