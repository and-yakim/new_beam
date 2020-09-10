from functools import reduce
from tkinter import *
from math import pi
from abc import abstractmethod
import cmath


class Drawn:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = self.draw()

    @abstractmethod
    def draw(self):
        pass

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

    @staticmethod
    def complex_rectangle_sides(diagonal):
        if len(diagonal) >= 4:
            corners = diagonal[0:2] + [diagonal[0], diagonal[3]] \
                    + diagonal[2:4] + [diagonal[2], diagonal[1]]
            c_corners = [complex(corners[i], corners[i + 1]) for i in range(0, 7, 2)]
            return [(c_corners[i], c_corners[i - 1]) for i in range(4)]
        else:
            return []

    @property
    def complex_sides(self):
        return self.complex_rectangle_sides(self.dots)


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

    def _apply_force(self):
        force = [self.wsad[3] - self.wsad[2], self.wsad[1] - self.wsad[0]]
        if force[0] and force[1]:
            force[0] *= 0.7
            force[1] *= 0.7
        for i in range(2):
            self.velocity[i] += 0.5 * force[i]
            self.velocity[i] *= 0.9

    def apply_velocity(self):
        self._apply_force()
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.move(self.velocity[0], self.velocity[1])


class Beam(Drawn):
    def __init__(self, player, canvas):
        self.point_x, self.point_y = 0, 0
        self.player = player
        self.dots = [0] * 4
        Drawn.__init__(self, canvas)
        self.view = pi / 6

    def draw(self):
        return self.canvas.create_polygon(self.dots, fill='white', width=0)

    def change_point(self, x, y):
        self.point_x, self.point_y = x, y

    def change_view(self, event):
        if event.delta < 0:
            if self.view > pi / 24:
                self.view -= pi / 24
        elif event.delta > 0:
            if self.view < pi / 2:
                self.view += pi / 24

    @property
    def _view_direction(self):
        c_view = complex(self.point_x - self.player.x, self.point_y - self.player.x)
        return cmath.phase(c_view[1])

    def reshape(self, obstacles):
        self.dots = []
        self.canvas.coords(self.id, self.dots)


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

    @property
    def obstacles(self):
        blocks_sides = list(map(lambda block: block.complex_sides, self.blocks))
        field_sides = Rectangle.complex_rectangle_sides([0, 0, self.width, self.height])
        blocks_sides.append(field_sides)
        return reduce(lambda acc, side: acc + side, blocks_sides)

    def step(self):
        self.player.apply_velocity()
        self.beam.reshape(self.obstacles)
        self.root.after(10, self.step)

    def bind(self):
        key_binds = {
            '<Button-1>': self.click,
            '<Motion>': self.motion,
            '<MouseWheel>': self.beam.change_view,
            '<space>': lambda _: self.blocks_clear(),
            '<KeyPress-w>': lambda _: self.player.change_wsad(0, True),
            '<KeyRelease-w>': lambda _: self.player.change_wsad(0, False),
            '<KeyPress-s>': lambda _: self.player.change_wsad(1, True),
            '<KeyRelease-s>': lambda _: self.player.change_wsad(1, False),
            '<KeyPress-a>': lambda _: self.player.change_wsad(2, True),
            '<KeyRelease-a>': lambda _: self.player.change_wsad(2, False),
            '<KeyPress-d>': lambda _: self.player.change_wsad(3, True),
            '<KeyRelease-d>': lambda _: self.player.change_wsad(3, False)
        }
        for key in key_binds:
            self.root.bind(key, key_binds[key])

    def click(self, event):
        if len(self.blocks) > 0 and not self.blocks[-1].click_flag:
            self.blocks[-1].click_flag = True
        else:
            if len(self.blocks) == 5:
                self.blocks[0].drawing_remove()
                del self.blocks[0]
            self.blocks.append(Rectangle(event.x, event.y, self.field))

    def motion(self, event):
        x, y = event.x, event.y
        self.beam.change_point(x, y)
        if len(self.blocks) and not self.blocks[-1].click_flag:
            self.blocks[-1].change_dot(x, y)

    def blocks_clear(self):
        for block in self.blocks:
            block.drawing_remove()
        self.blocks = []


def main():
    BeamGame()


if __name__ == '__main__':
    main()
