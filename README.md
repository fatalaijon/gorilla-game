## Gorilla Game

A Python re-implementation of the classic Basic Gorilla game.

![game screenshot](images/gorilla-game.png)

## How to Play

Run `monkey_game.py` in a Python 3.6 or newer interpretter:
```shell
python3 monkey_game.py
```

The goal is to throw a banana that hits the other gorilla.

Use the Up/Down arrow keys to change the angle of banana toss; +/- keys to change the speed of banana toss. Press SPACE to toss a banana. Alternatively, you can press buttons at the bottom of screen for these actions.

The game remembers each player's previously selected banana speed and angle.


## Changes to Starter Code


In `gamelib.GameApp`:
* `create_canvas()` returns the canvas reference instead of setting `self.canvas`.
* add methods `add_element(element)` and `remove_element(element)` so subclasses don't need to directly modify the elements attribute
* `contains(x, y)` returns True if a game element contains point (x,y). This method is needed to detect collision between banana and a game element.
* `start()` sets a reference to the id returned by `after` so animation can be cancelled.
* `stop()` new method to stop animation using the timer id
* `running()` test if the animation loop is running
* `self.timer_id` new attribute to keep track of timer id

In `gamelib.GameCanvasElement` 
* add `**kwargs` parameter to `__init__` and pass this parameter to `init_canvas_object`. This enables passing additional named arguments to Canvas widget constructors.  I used this to create Text with alignment.
* method `init_canvas_object(**kwargs)` returns the object id (int) instead of setting it as a side-effect.  This fixes warnings from VSCode about unknown symbol `self.canvas_object_id`.
* make `canvas` a property that returns `self._canvas`

In `gamelib.Sprite`
* add properties `width` and `height` as convenience to get the Sprite's image width and height

Source code
* Rename `monkeys.py` to `monkey_game.py`.
* Move images to `images` subdirectory.

## Images and Animation

For a better implementation of PhotoImage:
```python
from PIL import ImageTk, Image

img1 = ImageTk.PhotoImage(Image.open('myimage.png'))
# or pass image data to constructor:
img2 = ImageTk.PhotoImage(image_data)
```
documentation claims that `ImageTk.PhotoImage` is a 
"Tkinter-compatible photo image."
The `ImageTk.PhotoImage` constructor also accepts `file=` and `data=`
parameters to initialize the photo image object.

The `PIL.Image` class has a method to rotate an image.
We can use this to create rotated bananas for animation:
```python
image = Image.open("images/banana.png")
# an array to store images
self.images = [image]
# add rotated version of the original image
for angle in range(45,360,45):
     self.images.append( image.rotate(angle) )
```

Then use the `paste(image)` method of ImageTk.PhotoImage to change the image:
```
paste(image)
    Paste Image object into a PhotoImage. `image` must have the same dimensions
    as the original image.
```

While the banana is moving, in the Banana's `update` method "paste" 
the next image from the sequence.  This makes the banana appear to spin as it moves.

 
## Dialog Box

When a gorilla wins, the game shows a dialog box asking if user wants to play again.
An easy way to do this is using `tkinter.messagebox`:
```python
from tkinter import messagebox

message = "Play\nagain?"
reply = messagebox.askyesno("This is the title", message)
if reply:
    print("play another game")
else:
    quit()
```

The documentation claims these are modal dialogs, but since there's no reference to a parent object, I don't see how.
