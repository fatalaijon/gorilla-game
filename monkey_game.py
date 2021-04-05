import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import tkinter.simpledialog as dialog
import tkinter.messagebox as messagebox
from random import randint

from gamelib import Sprite, GameApp, Text
from banana import Banana
from building import BuildingFactory
from explosion import Explosion
import game_constants as config
# avoid circular imports
import monkey


class MonkeyGame(GameApp):
    """The main class for the Monkey game consists of a canvas
    with some game elements, e.g. monkeys, buildings, and a banana or two.
    """

    def __init__(self, *args):
        self.player_index = 1    # Index of player to take a turn, pre-updated by next_player()
        super().__init__(*args)

    def init_game(self):
        """This method is called by the superclass (GameApp) constructor
        to initialize game elements.
        """
        self.canvas['bg'] = config.CANVAS_COLOR
        self.clear_canvas()
        self.init_control_panel()
        self.init_game_objects()
        # handle mouse clicks (not actually used now)
        self.parent.bind("<Button-1>", self.on_click)
        # Set next player to take a turn and the animation state
        self.next_player()

    def init_game_objects(self):
        """Initial objects on the game canvas."""
        # draw buildings before gorillas   
        self.buildings = BuildingFactory.create_buildings(self.canvas)
        for bldg in self.buildings:  self.add_element(bldg)
        self.create_players()
        # craters are the holes left by explosions
        # keep track of them so that subsequent throws can pass through holes
        self.craters = []
        self.create_message_box()

    def clear_canvas(self):
        """Remove all objects from the canvas."""
        for id in self.canvas.find_all():
            self.canvas.delete(id)
        self.elements.clear()

    def create_players(self):
        """Create the players, consisting of monkeys and their bananas."""
        # save the players in an array so we can easily switch references
        self.players = []
        # Each player (monkey) gets a reusable banana to throw.
        # Reuse the same banana so it remembers it's initial speed and angle.
        center_building = len(self.buildings)//2
        for k in (0,1):
            # Randomly choose a building to stand on, such that player 0 is on
            # left and player 1 is on right.  Assumes buildings ordered left to right.
            bldg_number = randint(0, min(2,center_building-1))
            if k == 1: # player 1 count buildings from right edge
                bldg_number = len(self.buildings) -1 - bldg_number
            building = self.buildings[bldg_number]
            player_x = building.x + building.width//2
            player_y = building.top
            player = monkey.Monkey(self.canvas, 'images/monkey.png', player_x, player_y)
            player.name = f"Gorilla {k+1}"
            # player 1 throws banana to the left, player 0 throws to right (the default)
            if k == 1: player.banana.set_x_axis(tk.LEFT)
            self.players.append(player)
            # ??? add each monkey to the collection of game elements ???
            self.add_element(player)
            # NOTE: Don't add banana to game elements.
            # Updating banana is handled explicitly (drawn last).

    def create_message_box(self):
        self.message_box = Text(self.canvas,
                " "*16, 
                20, 40,  # show text in upper left corner of canvas
                fill="white",
                justify=tk.LEFT,
                anchor=tk.W,
                font=font.Font(family="Monospace",size=18)
                )

    def init_control_panel(self):
        """Create a row for controls and text messages."""
        textfont = font.Font(family="Arial", size=16, weight=font.NORMAL)
        # An iterator for getting the next grid column index
        column = iter(range(0,20))
        controls = ttk.Frame(self, name="controls", borderwidth=4, padding=5) 
        controls.grid(row=1, column=0)
        self.speed_text = tk.Label(controls, text="Speed: XX")
        #self.speed_text.grid(row=0, column=next(column))
        # Buttons to set the speed of toss
        self.buttonMinus = tk.Button(controls, text="-", 
                command=lambda : self.increase_speed(-1)
                )
        self.buttonPlus = tk.Button(controls, text="+",
                command=lambda : self.increase_speed(1)
                )
        # leave some space
        tk.Label(controls, text="  ")
        # Buttons to set the angle of toss
        self.angle_text = tk.Label(controls, text="Angle:  0")
        # up arrow \u2191, down arrow \u2193, triple up \u290A, triple down \u290B
        self.angleDown = tk.Button(controls, text="\u290B",
                command=lambda: self.increase_angle(-5)
                )
        self.angleUp = tk.Button(controls, text="\u290A",
                command=lambda : self.increase_angle(5)
                )
        # Button to throw banana
        tk.Label(controls, text="  ")
        self.throw_button = tk.Button(controls, text="Throw!",
                command = self.throw_banana)    
        # assign components to grid, add some padding to all components
        for component in controls.winfo_children():
            component['font'] = textfont
            component.grid(row=0, column=next(column))
            component.grid_configure(padx=5, pady=3)

    def increase_speed(self, amount):
        """Increase the speed by amount. Decreases speed if amount less than 0."""
        self.banana.speed += amount
        self.speed_text['text'] = f'Speed: {self.banana.speed:2d}'

    def increase_angle(self, degrees):
        """Increase the angle for throwing banana by degrees."""
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
            self.throw_banana()

    def on_click(self, event):
        """Handle mouse click event.  Create an explosion (for testing)."""
        pass

    def add_element(self, element):
        """Override GameApp.add_element to keep the monkeys (gorillas) on top
        of list of canvas elements, so they are drawn last.
        """
        super().add_element(element)
        if not isinstance(element, monkey.Monkey):
            self.canvas.tag_raise(config.GORILLA, element.canvas_object_id)

    def throw_banana(self):
        """ Throw a banana."""
        if not self.banana.is_moving:
            self.banana.reset()
            self.banana.start()
        # start the animation
        self.animation = self.throwing_banana
        # restart animation loop
        self.start()

    ##
    ## Animation actions for different states of the game
    ##
    def idle(self):
        """Waiting for player to take a turn."""
        pass

    def throwing_banana(self):
        """Banana flies through the air, maybe collides with something."""
        self.banana.update()
        self.banana.render()
        # Check if the banana hits something
        # 1. Hits a gorilla (monkey).  
        # This ends the game once the explosion stops.
        for player in self.players:
            if self.banana.hits(player):
                print(f"Boom! banana hits {player}")
                self.banana.stop()
                self.explosion = Explosion(self.canvas, self.banana.x, self.banana.y)
                self.explosion.hits = player
                # change state
                self.animation = self.exploding
                return

        for bldg in self.buildings:
            if self.banana.hits(bldg) and not self.in_crater(self.banana):
                # hits a building, but not a hole left by previous explosion
                print(f"Boom! banana hits {bldg}")
                self.banana.stop()
                self.explosion = Explosion(self.canvas, self.banana.x, self.banana.y)
                self.explosion.hits = bldg
                # change state
                self.animation = self.exploding
                return

        # If execution gets here, then the banana didn't hit anything.
        # It can keep moving, otherwise it stops when below screen
        # and next player's turn.
        if self.banana.is_moving:
            self.message_box.set_text(f"({self.banana.x:.0f},{self.banana.y:.0f})")
        else:
            # next player's turn
            self.stop()
            self.next_player()

    def exploding(self):
        """An explosion is occurring."""
        self.explosion.update()
        if self.explosion.is_exploding():
            return
        # done exploding, change the state
        self.craters.append(self.explosion)
        hit_object = self.explosion.hits
        self.stop()
        if isinstance(hit_object, monkey.Monkey):
            try:
                loser = self.players.index(hit_object)
                winner = self.players[1 - loser]
                self.game_over(winner)
                # if the method returns, start a new game
                self.init_game()
                return
            except ValueError as ex:
                print(ex)
        self.next_player()

    def game_over(self, winner: monkey.Monkey):
        msg = f"{winner.name} wins!\n\nPlay again?"
        newgame = messagebox.askyesno("Game Over", msg)
        if not newgame:
            quit(self)

    def animate(self):
        self.animation()
        if not self.stopped():
            self.timer_id = self.after(self.update_delay, self.animate)

    def in_crater(self, element) -> bool:
        """Test if element is inside a crater left by an explosion."""
        return any(crater.contains(element.x,element.y) for crater in self.craters)
    
    def next_player(self):
        """Select the next player to take a turn.
        This sets self.monkey, self.banana, and updates controls as side effects.
        """
        self.player_index = 1 - self.player_index
        self.player = self.players[self.player_index]
        self.banana = self.player.banana
        # call the update methods on controls so that the actual speed/angle 
        # of the current banana are shown
        self.increase_speed(0)
        self.increase_angle(0)
        self.message_box.set_text(f"{self.player.name}'s turn")
        self.animation = self.idle

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gorilla Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = MonkeyGame(root, config.CANVAS_WIDTH, config.CANVAS_HEIGHT, config.UPDATE_DELAY)
    #app.start()      # this calls animate
    root.mainloop()
