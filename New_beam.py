from tkinter import *
from math import *


WIDTH, HEIGHT = 800, 500


class Rectangle:
    def __init__(self, x, y, canvas):
        self.canvas: Canvas = canvas
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
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.point_x, self.point_y = 0, 0
        self.speed = 0
        self.view = pi / 6

    def change_point(self, x, y):
        self.point_x, self.point_y = x, y

    def draw(self, canvas, radius=10):
        canvas.create_oval(self.x - radius, self.y - radius,
                           self.x + radius, self.y + radius,
                           fill='yellow', width=1)


def mouse_wheel(event, player):
    if event.delta == -120:
        if player.teta > pi / 24:
            player.teta -= pi / 24
    if event.delta == 120:
        if player.teta < pi / 2:
            player.teta += pi / 24


def motion(event, player, blocks):
    player.x, player.y = event.x, event.y
    if len(blocks) and not blocks[-1].click_flag:
        blocks[-1].change_dot(event.x, event.y)


def click(event, blocks, canvas):
    if len(blocks) > 0 and not blocks[-1].click_flag:
        blocks[-1].click_flag = True
    else:
        if len(blocks) == 5:
            blocks[0].drawing_del()
            del blocks[0]
        blocks.append(Rectangle(event.x, event.y, canvas))


def main():
    root = Tk()
    root.geometry('+300+100')

    field = Canvas(root, width=WIDTH, height=HEIGHT, bg='silver')
    field.pack()

    player = Player(WIDTH / 2, HEIGHT / 2)
    blocks: [Rectangle] = []

    root.bind('<Button-1>', lambda event: click(event, blocks, field))
    root.bind('<Motion>', lambda event: motion(event, player, blocks))
    root.bind('<MouseWheel>', lambda event: mouse_wheel(event, player))
    root.bind('<space>', lambda _: blocks.clear())

    player.draw(field)

    root.mainloop()


if __name__ == '__main__':
    main()
