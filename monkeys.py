import tkinter as tk

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 1

class Banana(Sprite):
    def init_element(self):
        self.vx = 0
        self.vy = 0

        self.start_x = self.x
        self.start_y = self.y
        self.start_vx = 0
        self.start_vy = 0

        self.is_moving = False
        self.hide()

    def set_speed(self, vx, vy):
        self.vx = vx
        self.vy = vy

        self.start_vx = vx
        self.start_vy = vy

    def update(self):
        if self.is_moving:
            self.x += 5
            self.y -= self.vy
            self.vy -= GRAVITY

            if self.y > CANVAS_HEIGHT:
                self.stop()
                self.hide()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

        self.vx = self.start_vx
        self.vy = self.start_vy

        self.stop()

    def start(self):
        self.show()
        self.is_moving = True

    def stop(self):
        self.is_moving = False


class MonkeyGame(GameApp):
    def create_sprites(self):
        self.banana = Banana(self, 'banana.png', 100, 400)
        self.banana.set_speed(15, 25)

        self.monkey = Sprite(self, 'monkey.png', 100, 400)
        self.enemy = Sprite(self, 'monkey.png', 700, 400)

        self.elements.append(self.banana)
        self.elements.append(self.monkey)
        self.elements.append(self.enemy)

        self.speed_text = Text(self, 'Speed: XX', 40, 20)
        
        self.elements.append(self.speed_text)

    def update_speed_text(self):
        self.speed_text.set_text(f'Speed: {self.speed}')
        
    def init_game(self):
        self.create_sprites()

        self.speed = 3
        self.update_speed_text()

    def on_key_pressed(self, event):
        if event.char == '+':
            if self.speed < 10:
                self.speed += 1
                self.update_speed_text()
                
        if event.char == '-':
            if self.speed > 1:
                self.speed -= 1
                self.update_speed_text()

        if event.char == ' ':
            if not self.banana.is_moving:
                self.banana.set_speed(3 * self.speed, 5 * self.speed)
                self.banana.reset()
                self.banana.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = MonkeyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
