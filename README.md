## Gorilla Game

A re-implementation of the classic Basic Gorilla game.

*Because students shouldn't have all the fun.*

## Changes to Starter Code

In `gamelib.GameCanvasElement` the method `init_canvas_object()` must return the object id (int).  This fixes a lot of warnings from VSCode about unknown symbol `self.canvas_object_id`.

In `gamelib.GameApp`, `create_canvas()` returns the canvas reference
instead of setting `self.canvas`.

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
parameters to initialize the phto image object.

It also has this method:
```
paste(image)
    Paste Image object into a PhotoImage. `image` must have the same dimensions.
```

 
