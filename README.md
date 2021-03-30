## Gorilla Game

A re-implementation of the classic Basic Gorilla game.

*Because students shouldn't have all the fun.*

## Changes to Starter Code

In `gamelib.GameCanvasElement` 
* method `init_canvas_object()` must return the object id (int).  This fixes warnings from VSCode about unknown symbol `self.canvas_object_id`, and avoids depending on a side-effect.

In `gamelib.GameApp`:
* `create_canvas()` returns the canvas reference instead of setting `self.canvas`.
* add methods `add_element(element)` and `remove_element(element)` so subclasses don't need to directly modify the elements attribute
* `contains(x, y)` returns True if a game element contains point (x,y). This method is needed to detect collision between banana and a game element.

In `gamelib.Sprite`
* add properties `width` and `height` as convenience to get the Sprite's image width and height

Rename `monkeys.py` to `monkey_game.py`.

## Images

For a better implementation of PhotoImage:
```python
from PIL import ImageTk, Image

img1 = ImageTk.PhotoImage(Image.open('myimage.png'))
img2 = ImageTk.PhotoImage(image_data)
```
documentation claims that `ImageTk.PhotoImage` is a 
"Tkinter-compatible photo image."
The `ImageTk.PhotoImage` constructor also accepts `file=` and `data=`
parameters to initialize the photo image object.

It has a `paste(image)` method that we can use to change the image:
```
paste(image)
    Paste Image object into a PhotoImage. `image` must have the same dimensions
    as the original image.
```
This is how we make the banana appear to spin as it moves.

 
