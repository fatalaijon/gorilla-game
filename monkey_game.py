import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import tkinter.constants as tk_constants
import math
from random import random, randint
from typing import List, Tuple, Any

from gamelib import Sprite, GameApp, Text
from banana import Banana  # for Banana class
import monkey  # for Monkey class
import building
import explosion

import game_constants as config

class MonkeyGame(GameApp):
    """The main class for the Monkey game consists of a canvas
    with some game elements, e.g. monkeys, buildings, and a banana.
    """

    def init_game(self):
        """This method is called by the superclass (GameApp) constructor
        to initialize game elements.
        """
        print("Canvas size:", 
              f"{self.canvas['width']} x {self.canvas['height']}")
        self.init_control_panel()
        self.canvas['bg'] = config.CANVAS_COLOR
        # buildings before gorillas
        baseline = int(self.canvas['height'])
        self.create_buildings(baseline)
        self.create_sprites()
        self.create_message_box()
        # handle mouse clicks
        self.parent.bind("<Button-1>", self.on_click)
        # craters are the holes left by explosions
        # keep track of them so that subsequent throws of a banana
        # can pass through the hole.
        self.craters = []
        # Set the player to take a turn
        self.monkey = None
        self.next_player()


    def create_sprites(self):
        # save the gorillas in an array so we can easily switch references
        self.players: List[Any] = [
                (monkey.Monkey(self, 'images/monkey.png', 100, 450), None),
                (monkey.Monkey(self, 'images/monkey.png', 700, 450), None)
                ]
        # Each gorilla (monkey) gets a reusable banana to throw.
        # Reuse the same banana so it remembers it's initial speed and angle.
        
        for k in (0,1):
            # The initial position of each banana is above the gorilla's head
            player = self.players[k][0]
            player.name = f"Gorilla {k+1}"
            mx = player.x
            my = player.y - player.height/2 - 10  # 10 pixels above monkey
            mybanana = Banana(self, 'images/banana.png', mx, my)
            # initial speed and angle of throw
            mybanana.angle = 60
            mybanana.speed = 20
            # player 1 throws banana to the left
            if k == 1: mybanana.set_x_axis(tk.LEFT)
            # replace player with tuple (monkey,banana)
            self.players[k] = (player, mybanana)
            # Also add each gorilla to collection of game elements
            self.add_element(player)
            # NOTE: Don't add banana to game elements.
            # Updating banana is handled explicitly (drawn last).

    def create_message_box(self):
        self.message_box = Text(self,
                " "*16, 
                100, 40,  # show text in upper left corner of canvas
                fill="white",
                justify=tk.LEFT,  # but it doesn't work!
                font=font.Font(family="Monospace",size=18)
                )

    def create_buildings(self, baseline):
        bldg_colors = ["firebrick2", "cyan2", "gray75" ]
        x = 0
        while x < int(self.canvas['width']):
            width = building.ROOM_WIDTH*randint(5,9)
            # height not necessarily a multiple of floor height,
            # so windows don't all line up
            height = int((0.2+random())*int(self.canvas['height'])/2)
            color = bldg_colors[randint(0,len(bldg_colors)-1)]
            bldg = building.Building(self, x, baseline, width, height, color)
            self.add_element(bldg)
            x = x + width


    def init_control_panel(self):
        """Create a row for controls and text messages."""
        textfont = font.Font(family="Arial", size=16, weight=font.NORMAL)
        controls = ttk.Frame(self, name="controls", borderwidth=4, padding=5) 
        controls.grid(row=1, column=0)
        self.speed_text = tk.Label(controls, text="S peed: XX")
        self.speed_text.grid(row=0, column=0)
        self.buttonMinus = tk.Button(controls, text="-", 
                command=lambda : self.increase_speed(-1)
                )
        self.buttonMinus.grid(row=0, column=1)
        self.buttonPlus = tk.Button(controls, text="+",
                command=lambda : self.increase_speed(1)
                )
        self.buttonPlus.grid(row=0, column=2)
        # leave some space
        tk.Label(controls, text="  ").grid(row=0, column=3)
        # set the angle for throwing banana
        self.angle_text = tk.Label(controls, text="Angle:  0")
        self.angle_text.grid(row=0, column=4)
        # up arrow \u2191, down arrow \u2193, triple up \u290A, triple down \u290B
        self.angleDown = tk.Button(controls, text="\u290B",
                command=lambda: self.increase_angle(-5)
                )
        self.angleDown.grid(row=0, column=5)
        self.angleUp = tk.Button(controls, text="\u290A",
                command=lambda : self.increase_angle(5)
                )
        self.angleUp.grid(row=0, column=6)        
        # add some padding to all components
        for component in controls.winfo_children():
            component['font'] = textfont
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
            # start the animation
            self.start()

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
        """Override GameApp.animate in order to check for collisions and start/stop animation."""
        for element in self.elements:
            element.update()
            element.render()
        # Update the banana last
        self.banana.update()
        self.banana.render()
        
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
        
        if self.banana.is_moving:
            self.message_box.set_text(f"({self.banana.x:.0f},{self.banana.y:.0f})")   

        # Stop the animation when a) banana not moving AND b) bomb not exploding
        if self.banana.is_moving or any([crater.is_exploding() for crater in self.craters]):
            # keep animating
            pass
        else:
            self.stop()

        if self.running():
            self.timer_id = self.after(self.update_delay, self.animate)
        else:
            # next player's turn
            self.next_player()
        

    def in_crater(self, element) -> bool:
        """Test if element is inside a crater left by an explosion."""
        for crater in self.craters:
            # old explosions leave a hole that banana can pass threw
            if crater.contains(element.x, element.y):
                return True
        return False
    
    def next_player(self):
        """Select the next player to take turn. This sets self.monkey,
        self.banana, and updates controls as side effect.
        """
        index = 1 if self.monkey == self.players[0][0] else 0
        (self.monkey, self.banana) = self.players[index]
        # call the update methods so that the actual speed/angle 
        # of the banana are shown
        self.increase_speed(0)
        self.increase_angle(0)
        self.message_box.set_text(f"{self.monkey.name} turn")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gorilla Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = MonkeyGame(root, config.CANVAS_WIDTH, config.CANVAS_HEIGHT, config.UPDATE_DELAY)
    #app.start()      # this calls animate
    root.mainloop()
