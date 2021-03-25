from gamelib import Sprite


class Monkey(Sprite):
    """A monkey that can throw bananas"""
    def __init__(self, game_app, image_filename, x=0, y=0):
        super().__init__(game_app, image_filename, x, y)

    def intersects(self, x, y):
        """The point x,y intersects the monkey's image if it
        hits any part of the `image.
        """
        w = self.image.width()
        h = self.image.height()
        dx = abs(x- self.x)
        dy = abs(y -self.y)
        if dx > w/2: return False
        if dy > w/2: return False
        # Exclude the 4 corners of bounding box of the image
        if dx > w/4 and dy > w/4: return False
        return True
        
