"""
Named constants for values that configure the game.
Some source files contain constants specific to those objects,
such as building dimensions in buildings.py.
"""
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
# Canvas background color.
# Preferrably a dark color that does not appear in images of monkey, banana, 
# or buildings.
CANVAS_COLOR = "medium blue"
# Delay between animation updates, in millisecs.
UPDATE_DELAY = 60  # 33
# Constant for force of gravity. Larger value makes things fall faster.
GRAVITY = 1
# A tag (string) used to identify gorilla objects on canvas
GORILLA = "gorilla"