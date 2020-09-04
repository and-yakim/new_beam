from tkinter import *
from math import *


class Rectangle:
    def __init__(self, x, y, canvas):
        self.canvas = canvas
        self.dots = [x, y] * 2
        self.id = self.draw()
        self.click_flag = False

    def draw(self):
        return self.canvas.create_rectangle(self.dots, fill='brown', width=0)

    def change_dot(self, x, y):
        self.dots[2], self.dots[3] = x, y
        self.canvas.coords(self.id, self.dots)

    def drawing_del(self):
        self.canvas.delete(self.id)


class Player:
    def __init__(self, x, y, canvas):
        self.x, self.y = x, y
        self.canvas = canvas
        self.point_x, self.point_y = 0, 0
        self.speed = 0
        self.view = pi / 6

    def change_point(self, x, y):
        self.point_x, self.point_y = x, y

    def draw(self, radius=10):
        self.canvas.create_oval(self.x - radius, self.y - radius,
                           self.x + radius, self.y + radius,
                           fill='yellow', width=1)


class BeamGame:
    def __init__(self):
        self.width, self.height = 800, 500

        self.root = Tk()
        self.root.geometry('+300+100')

        self.field = Canvas(self.root, width=self.width, height=self.height, bg='silver')
        self.field.pack()

        self.player = Player(self.width / 2, self.height / 2, self.field)
        self.blocks: [Rectangle] = []

        self.root.bind('<Button-1>', self.click)
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<MouseWheel>', self.mouse_wheel)
        self.root.bind('<space>', self.blocks.clear)

        self.player.draw()

        self.root.mainloop()

    def mouse_wheel(self, event):
        if event.delta == -120:
            if self.player.view > pi / 24:
                self.player.view -= pi / 24
        if event.delta == 120:
            if self.player.view < pi / 2:
                self.player.view += pi / 24

    def motion(self, event):
        self.player.x, self.player.y = event.x, event.y
        if len(self.blocks) and not self.blocks[-1].click_flag:
            self.blocks[-1].change_dot(event.x, event.y)

    def click(self, event):
        if len(self.blocks) > 0 and not self.blocks[-1].click_flag:
            self.blocks[-1].click_flag = True
        else:
            if len(self.blocks) == 5:
                self.blocks[0].drawing_del()
                del self.blocks[0]
            self.blocks.append(Rectangle(event.x, event.y, self.field))


def main():
    BeamGame()


if __name__ == '__main__':
    main()
