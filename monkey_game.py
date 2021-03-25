import tkinter as tk
from tkinter import ttk
from tkinter.constants import W
import tkinter.font as font
import math

from gamelib import Sprite, GameApp, Text
import banana  # for Banana class
import monkey  # for Monkey class
import building

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
# use a color that does not appear in Sprite image for monkey or banana
CANVAS_COLOR = "medium blue"

UPDATE_DELAY = 33
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
        self.update_speed(0)
        self.increase_angle(0)

    def create_sprites(self):
        self.monkey = monkey.Monkey(self, 'monkey.png', 100, 400)
        self.enemy = monkey.Monkey(self, 'monkey.png', 700, 400)
        # Monkey 1 throws the banana, so banana starts above monkey's head
        mx = self.monkey.x
        my = self.monkey.y - self.monkey.height/2 - 10 # 10 pixels above monkey
        self.banana = banana.Banana(self, 'banana.png', mx, my)
        # initial speed and angle of throw
        self.banana.angle = 60
        self.banana.speed = 20

        self.add_element(self.banana)
        self.add_element(self.monkey)
        self.add_element(self.enemy)
        # y-coordinte of the baseline of building (a pure guess)
        ybase = 500
        self.create_buildings(ybase)

    def create_buildings(self, baseline):
        building.Building(self.canvas, 300, baseline, 80, 200, "red")

    def init_control_panel(self):
        """Create a row for controls and text messages."""
        controls = ttk.Frame(self, name="controls", borderwidth=4, padding=5) 
        controls.grid(row=1, column=0)
        self.buttonMinus = tk.Button(controls, text="-", command=lambda : self.update_speed(-1))
        self.buttonMinus.grid(row=0, column=0)
        self.speed_text = tk.Label(controls, text="Speed: XX")
        self.speed_text.grid(row=0, column=1)
        self.buttonPlus = tk.Button(controls, text="+", command=lambda : self.update_speed(1))
        self.buttonPlus.grid(row=0, column=2)
        # leave some space
        tk.Label(controls, text="   ").grid(row=0, column=3)
        # set the angle for throwing banana
        # up arrow \u2191, down arrow \u2193, triple up \u290A, triple down \u290B
        self.angleDown = tk.Button(controls, text="\u290B", command=lambda: self.increase_angle(-5))
        self.angleDown.grid(row=0, column=4)
        self.angle_text = tk.Label(controls, text="Angle:  0")
        self.angle_text.grid(row=0, column=5)
        self.angleUp = tk.Button(controls, text="\u290A", command=lambda : self.increase_angle(5))
        self.angleUp.grid(row=0, column=6)        
        # add some padding to all components
        fnt = font.Font(family="Monospace", weight=font.NORMAL, size=14)
        for component in controls.winfo_children():
            component.grid_configure(padx=5, pady=3)
            component['font'] = fnt

    def update_speed(self, amount):
        """Increase the speed by amount. Decreases speed if amount less than 0."""
        MAX_SPEED = 50
        if 1 <= amount + self.banana.speed <= MAX_SPEED:
            self.banana.speed += amount
            self.speed_text['text'] = f'Speed: {self.banana.speed:2d}'
        if self.banana.speed <= 1:
            self.buttonMinus["state"] = tk.DISABLED
        else:
            self.buttonMinus["state"] = tk.NORMAL
        if self.banana.speed >= MAX_SPEED:
            self.buttonPlus["state"] = tk.DISABLED
        else:
            self.buttonPlus["state"] = tk.NORMAL

    def increase_angle(self, degrees):
        """Increase the angle for throwing banana by degrees."""
        MIN_ANGLE = 0   # if gorillas are on buildings, may need to allow negative angle
        MAX_ANGLE = 90  # throwing vertically is suicide
        if MIN_ANGLE <= degrees + self.banana.angle <= MAX_ANGLE:
            self.banana.angle += degrees
            self.angle_text['text'] = f"Angle: {self.banana.angle:2d}"

    def on_key_pressed(self, event):
        if event.char == '+':
            self.update_speed(1)
        elif event.char == '-':
            self.update_speed(-1)
        elif event.char == ' ':
            if not self.banana.is_moving:
                self.banana.reset()
                self.banana.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gorilla Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = MonkeyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
