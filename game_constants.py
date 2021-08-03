"""
Named constants for values that configure the game.
Some source files contain constants specific to those objects.

Constants for building dimensions and colors are in building.py
"""
# Width and height of the game area, measured in pixels.
# This does not include the control panel at bottom.
# A 1080p display has 1920x1080 pixels. Typical laptop is 1366 x 768.
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
# Canvas background color.
# Use a color that is distinct from images of gorilla, banana, or buildings.
# For a list of all Tkinter colors and their names, see:
# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
# (that page also has a Python script you can run to create a color chart)
CANVAS_COLOR = "dark blue"
# Color of the player names and scores
SCOREBOARD_COLOR = "dark blue"
# Delay between animation updates, in millisecs.
UPDATE_DELAY = 60  # or 33 (33 ms yields 30 frames per second)
# Constant for force of gravity. Larger value makes things fall faster.
GRAVITY = 1
# maximum initial speed of banana toss. Cannot set speed higher than this.
MAX_BANANA_SPEED = 99
# A tag (string) used to identify gorilla objects on canvas
GORILLA = "gorilla"
