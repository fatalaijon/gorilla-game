import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import tkinter.constants as tk_constants
import math

from gamelib import Sprite, GameApp, Text
import banana  # for Banana class
import monkey  # for Monkey class
import building
import explosion

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
# use a color that does not appear in the images for monkey or banana
CANVAS_COLOR = "medium blue"

UPDATE_DELAY = 60  # 33
GRAVITY = 1


class MonkeyGame(GameApp):
    """The main class for the Monkey game consists of a canvas
    with some game elements, e.g. monkeys, buildings, and a banana.
    """

    def init_game(self):
        """This method is called by the superclass (GameApp) constructor
        to initialize game elements.
        """
        self.create_sprites()
        self.init_control_panel()
        self.canvas['bg'] = CANVAS_COLOR
        # call the update methods so that the actual speed/angle are shown on labels
        self.increase_speed(0)
        self.increase_angle(0)
        # handle mouse clicks
        self.parent.bind("<Button-1>", self.on_click)
        # craters are the holes left by explosions
        # keep track of them so that subsequent throws of a banana
        # can pass through the hole.
        self.craters = []

    def create_sprites(self):
        
        self.monkey = monkey.Monkey(self, 'images/monkey.png', 100, 450)
        self.enemy = monkey.Monkey(self, 'images/monkey.png', 700, 450)
        # Monkey 1 throws the banana, so banana starts above monkey's head
        mx = self.monkey.x
        my = self.monkey.y - self.monkey.height/2 - 10 # 10 pixels above monkey
        self.banana = banana.Banana(self, 'images/banana.png', mx, my)
        # initial speed and angle of throw
        self.banana.angle = 60
        self.banana.speed = 20
        # NOTE: banana is not a game element, don't add to elements.
        self.add_element(self.monkey)
        self.add_element(self.enemy)
        self.textbox = Text(self, 
                f"({self.banana.x:.0f},{self.banana.y:.0f})", 
                80, 40,  # show text in upper left corner of canvas
                fill="white",
                justify=tk.LEFT,
                font=font.Font(family="Monospace",size=18)
                )
        # y-coordinte of the baseline of building
        baseline = 500
        self.create_buildings(baseline)

    def create_buildings(self, baseline):
        bldg = building.Building(self, 300, baseline, 120, 200, "red")
        self.add_element(bldg)

    def init_control_panel(self):
        """Create a row for controls and text messages."""
        controls = ttk.Frame(self, name="controls", borderwidth=4, padding=5) 
        controls.grid(row=1, column=0)
        self.speed_text = tk.Label(controls, text="Speed: XX")
        self.speed_text.grid(row=0, column=0)
        self.buttonMinus = tk.Button(controls, text="-", command=lambda : self.increase_speed(-1))
        self.buttonMinus.grid(row=0, column=1)
        self.buttonPlus = tk.Button(controls, text="+", command=lambda : self.increase_speed(1))
        self.buttonPlus.grid(row=0, column=2)
        # leave some space
        tk.Label(controls, text="  ").grid(row=0, column=3)
        # set the angle for throwing banana
        self.angle_text = tk.Label(controls, text="Angle:  0")
        self.angle_text.grid(row=0, column=4)
        # up arrow \u2191, down arrow \u2193, triple up \u290A, triple down \u290B
        self.angleDown = tk.Button(controls, text="\u290B", command=lambda: self.increase_angle(-5))
        self.angleDown.grid(row=0, column=5)
        self.angleUp = tk.Button(controls, text="\u290A", command=lambda : self.increase_angle(5))
        self.angleUp.grid(row=0, column=6)        
        # add some padding to all components
        fnt = font.Font(family="Monospace", weight=font.NORMAL, size=14)
        for component in controls.winfo_children():
            component.grid_configure(padx=5, pady=3)

    def increase_speed(self, amount):
        """Increase the speed by amount. Decreases speed if amount less than 0."""
        self.banana.speed += amount
        self.speed_text['text'] = f'Speed: {self.banana.speed:2d}'

    def increase_angle(self, degrees):
        """Increase the angle for throwing banana by degrees."""
        MIN_ANGLE = 0   # if gorillas are on buildings, may need to allow negative angle
        MAX_ANGLE = 90  # throwing vertically is suicide
        #TODO Make banana responsible for checking bounds of angle,
        # as done for speed.
        if MIN_ANGLE <= degrees + self.banana.angle <= MAX_ANGLE:
            self.banana.angle += degrees
            self.angle_text['text'] = f"Angle: {self.banana.angle:2d}"

    def on_key_pressed(self, event):
        # print("Key Pressed:", event)
        if event.char == '+':
            self.increase_speed(1)
        elif event.char == '-':
            self.increase_speed(-1)
        elif event.keysym == "Up":
            self.increase_angle(5)
        elif event.keysym == "Down":
            self.increase_angle(-5)
        elif event.char == ' ':
            # throw a banana
            if not self.banana.is_moving:
                self.banana.reset()
                self.banana.start()

    def on_click(self, event):
        """Handle mouse click event.  Create an explosion (for testing)."""
        print(f"Click at ({event.x},{event.y})")
        x = event.x
        y = event.y
        # Only create explosion if mouse clicked on canvas
        if y < 0 or y > self.canvas.winfo_height():
            print("Not on canvas")
            return
        widget = self.canvas.winfo_containing(x,y)
        if widget:
            print(f"{widget} at ({x},{y})")
        bomb = explosion.Explosion(self, x, y)
        self.add_element(bomb)

    def animate(self):
        """Override GameApp.animate in order to check for collisions."""
        for element in self.elements:
            element.update()
            element.render()
        # Update the banana last
        self.banana.update()
        self.banana.render()
        self.textbox.set_text(f"({self.banana.x:.0f},{self.banana.y:.0f})")
        # Check if the banana hits something

        # If banana "hits" a crater left by a previous explosion,
        # it should pass through (nothing there).
        if self.in_crater(self.banana):
            # a hole left by an explosion
            pass
        else:
            # Look for an intersecting game object
            for element in self.elements:
                if self.banana.hits(element):
                    print(f"Boom! banana hits {element}")
                    self.banana.stop()
                    bomb = explosion.Explosion(self, self.banana.x, self.banana.y)
                    self.add_element(bomb)
                    # add it to the list of craters, too
                    self.craters.append(bomb)
                    break
        
        self.after(self.update_delay, self.animate)

    def in_crater(self, element) -> bool:
        """Test if element is inside a crater left by an explosion."""
        for crater in self.craters:
            # old explosions leave a hole that banana can pass threw
            if crater.contains(element.x, element.y):
                return True
        return False
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gorilla Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = MonkeyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
