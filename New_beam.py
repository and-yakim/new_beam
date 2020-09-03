from tkinter import *
from math import *


class Polygon:
    def __init__(self):
        pass


class Player:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.speed = 0
        self.view = pi / 6

    def draw(self, canvas, radius=10):
        canvas.create_oval(self.x - radius, self.y - radius,
                           self.x + radius, self.y + radius,
                           fill='yellow', width=1)


def main():
    root = Tk()
    root.geometry('+300+100')

    width, height = 800, 500
    field = Canvas(root, width=width, height=height, bg='silver')
    field.pack()

    player = Player(width / 2, height / 2)

    def step():
        player.draw(field)
        root.after(10, step)

    def bind():
        pass

    step()

    root.mainloop()


if __name__ == '__main__':
    main()
