from tkinter import *
from math import *


class Drawn:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = self.draw()

    def draw(self):
        return None

    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)

    def drawing_remove(self):
        self.canvas.delete(self.id)


class Rectangle(Drawn):
    def __init__(self, x, y, canvas):
        self.dots = [x, y] * 2
        Drawn.__init__(self, canvas)
        self.click_flag = False

    def draw(self):
        return self.canvas.create_rectangle(self.dots, fill='brown', width=0)

    def change_dot(self, x, y):
        self.dots[2], self.dots[3] = x, y
        self.canvas.coords(self.id, self.dots)


class Player(Drawn):
    def __init__(self, x, y, canvas):
        self.x, self.y = x, y
        Drawn.__init__(self, canvas)
        self.velocity = [0, 0]
        self.wsad = [False] * 4

    def draw(self):
        radius = 10
        return self.canvas.create_oval(self.x - radius, self.y - radius,
                                       self.x + radius, self.y + radius,
                                       fill='yellow', width=1)

    def change_wsad(self, num, value):
        self.wsad[num] = value

    def apply_force(self):
        pass


class Beam(Drawn):
    def __init__(self, player, canvas):
        self.point_x, self.point_y = 0, 0
        self.player = player
        self.dots = [self.point_x, self.point_y, self.player.x, self.player.y]
        Drawn.__init__(self, canvas)
        self.view = pi / 6

    def change_point(self, x, y):
        self.point_x, self.point_y = x, y

    def draw(self):
        return self.canvas.create_polygon(self.dots, fill='white', width=0)

    def reshape(self):
        self.canvas.coords(self.id, self.dots)

    def change_view(self, event):
        if event.delta < 0:
            if self.view > pi / 24:
                self.view -= pi / 24
        elif event.delta > 0:
            if self.view < pi / 2:
                self.view += pi / 24


class BeamGame:
    def __init__(self):
        self.width, self.height = 800, 500
        self.root = Tk()
        self.root.geometry('+300+100')

        self.field = Canvas(self.root, width=self.width,
                            height=self.height, bg='silver')
        self.field.pack()

        self.player = Player(self.width / 2, self.height / 2, self.field)
        self.blocks: [Rectangle] = []
        self.beam = Beam(self.player, self.field)

        self.bind()

        self.step()

        self.root.mainloop()

    def step(self):
        self.root.after(100, self.step)

    def bind(self):
        self.root.bind('<Button-1>', self.click)
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<MouseWheel>', self.beam.change_view)
        self.root.bind('<space>', lambda _: self.blocks_clear())

        self.root.bind('<KeyPress-w>', lambda _: self.player.change_wsad(0, True))
        self.root.bind('<KeyRelease-w>', lambda _: self.player.change_wsad(0, False))
        self.root.bind('<KeyPress-s>', lambda _: self.player.change_wsad(1, True))
        self.root.bind('<KeyRelease-s>', lambda _: self.player.change_wsad(1, False))
        self.root.bind('<KeyPress-a>', lambda _: self.player.change_wsad(2, True))
        self.root.bind('<KeyRelease-a>', lambda _: self.player.change_wsad(2, False))
        self.root.bind('<KeyPress-d>', lambda _: self.player.change_wsad(3, True))
        self.root.bind('<KeyRelease-d>', lambda _: self.player.change_wsad(3, False))

    def click(self, event):
        if len(self.blocks) > 0 and not self.blocks[-1].click_flag:
            self.blocks[-1].click_flag = True
        else:
            if len(self.blocks) == 5:
                self.blocks[0].drawing_remove()
                del self.blocks[0]
            self.blocks.append(Rectangle(event.x, event.y, self.field))

    def motion(self, event):
        self.player.x, self.player.y = event.x, event.y
        if len(self.blocks) and not self.blocks[-1].click_flag:
            self.blocks[-1].change_dot(event.x, event.y)

    def blocks_clear(self):
        for block in self.blocks:
            block.drawing_remove()
            del block


def main():
    BeamGame()


if __name__ == '__main__':
    main()
