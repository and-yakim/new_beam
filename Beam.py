from tkinter import *
from math import *
from time import time


class Polygon:
    def __init__(self, x1, y1, x3, y3, flag):
        self.poly = [[x1, y1], [x1, y3], [x3, y3], [x3, y1]]
        self.flag = flag

    def draw(self):
        if not self.flag:
            self.poly[1] = [self.poly[0][0], self.poly[2][1]]
            self.poly[3] = [self.poly[2][0], self.poly[0][1]]
        field.create_polygon(self.poly, fill='brown', width=0)


class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.x_m, self.y_m = 0, 0
        self.v_x, self.v_y = 0, 0
        self.coef, self.speed = 0.9, 0.8
        self.teta = pi / 6
        self.w, self.s = False, False
        self.a, self.d = False, False

    def force(self):
        kx, ky = 0, 0
        if self.w:
            ky -= self.speed
        if self.s:
            ky += self.speed
        if self.a:
            kx -= self.speed
        if self.d:
            kx += self.speed
        if kx != 0 and ky != 0:
            k = sqrt(kx ** 2 + ky ** 2)
            kx *= self.speed / k
            ky *= self.speed / k
        self.v_x += kx
        self.v_y += ky

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        l = self.speed * self.coef / (1 - self.coef)
        if self.x > width - l:
            self.x -= 2 * (self.x - width + l)
            self.v_x *= -1
        elif self.x < l:
            self.x += 2 * (l - self.x)
            self.v_x *= -1
        if self.y > height - l:
            self.y -= 2 * (self.y - height + l)
            self.v_y *= -1
        elif self.y < l:
            self.y += 2 * (l - self.y)
            self.v_y *= -1
        self.v_x *= self.coef if abs(self.v_x) > 0.2 else 0
        self.v_y *= self.coef if abs(self.v_y) > 0.2 else 0

    def draw(self):
        field.create_oval((self.x - side // 2), (self.y - side // 2),
                          (self.x + side // 2), (self.y + side // 2),
                          fill='yellow', width=1)

    def beam(self):
        segments = [[0, 0, 0, height], [0, height, 0, -height],
                    [0, height, width, 0], [width, height, -width, 0],
                    [width, height, 0, -height], [width, 0, 0, height],
                    [width, 0, -width, 0], [0, 0, width, 0]]
        for i in block:
            for j in range(len(i.poly)):
                segments += [[i.poly[j - 1][0], i.poly[j - 1][1],
                              i.poly[j][0] - i.poly[j - 1][0], i.poly[j][1] - i.poly[j - 1][1]],
                             [i.poly[j][0], i.poly[j][1],
                              i.poly[j - 1][0] - i.poly[j][0], i.poly[j - 1][1] - i.poly[j][1]]]
        for i in segments:
            i[0] -= self.x
            i[1] -= self.y
        pm_seg = list(map(lambda x: [x[0] - x[2] * 0.001, x[1] - x[3] * 0.001], segments))
        sx, sy = self.x_m - self.x, self.y_m - self.y
        pm_seg += [[sx * cos(-self.teta) - sy * sin(-self.teta),
                    sx * sin(-self.teta) + sy * cos(-self.teta), 0],
                   [sx * cos(self.teta) - sy * sin(self.teta),
                    sx * sin(self.teta) + sy * cos(self.teta), 1]]
        beam_dots = []
        for k in segments:
            s0x, s0y = k[0], k[1]
            m = [1, s0x, s0y]
            for i in segments:
                six, siy = i[0], i[1]
                bx, by = i[2], i[3]
                if s0x * by == s0y * bx:
                    continue
                taui = (six * s0y - s0x * siy) / (s0x * by - bx * s0y)
                if 0 < taui < 1:
                    if s0x != 0:
                        ti = (six + bx * taui) / s0x
                    else:
                        ti = (siy + by * taui) / s0y
                    if 0 < ti < m[0]:
                        m = [ti, s0x * ti, s0y * ti]
            beam_dots.append([m[1], m[2]])
        for k in pm_seg:
            s0x, s0y = k[0], k[1]
            m = []
            for i in segments:
                six, siy = i[0], i[1]
                bx, by = i[2], i[3]
                if s0x * by == s0y * bx:
                    continue
                taui = (six * s0y - s0x * siy) / (s0x * by - bx * s0y)
                if 0 < taui < 1:
                    if s0x != 0:
                        ti = (six + bx * taui) / s0x
                    else:
                        ti = (siy + by * taui) / s0y
                    if len(m) == 0:
                        if ti > 0:
                            m = [ti, s0x * ti, s0y * ti]
                    elif 0 < ti < m[0]:
                        m = [ti, s0x * ti, s0y * ti]
            if len(k) == 3:
                beam_dots.append([m[1], m[2], k[2]])
            else:
                beam_dots.append([m[1], m[2]])
        left_poly, right_poly = [], []
        u_p, l_p = [], []
        for i in beam_dots:
            if i[0] > 0:
                right_poly.append(i)
            elif i[0] < 0:
                left_poly.append(i)
            else:
                if i[1] < 0:
                    u_p.append(i)
                else:
                    l_p.append(i)
        right_poly.sort(reverse=True, key=(lambda x: x[1] / x[0]))
        left_poly.sort(reverse=True, key=(lambda x: x[1] / x[0]))
        beam_dots = l_p + right_poly + u_p + left_poly
        sides = [0, 0]
        for i in range(len(beam_dots)):
            if len(beam_dots[i]) == 3:
                if beam_dots[i][2] == 0:
                    sides[0] = i
                else:
                    sides[1] = i
        if sides[0] > sides[1]:
            beam_dots = beam_dots[sides[1]:sides[0] + 1]
        else:
            beam_dots = beam_dots[sides[1]:] + beam_dots[:sides[0] + 1]
        beam_dots.append([0, 0])
        beam_dots = list(map(lambda x: [x[0] + self.x, x[1] + self.y], beam_dots))
        if self.teta < pi / 48:
            return
        field.create_polygon(beam_dots, fill='white', width=0)


def grid_draw():
    for i in range(side, width, side):
        field.create_line(i, 0, i, height, fill='blue')
    for j in range(side, height, side):
        field.create_line(0, j, width, j, fill='blue')


def blocks_draw():
    if len(block) > 0 and not block[-1].flag:
        block[-1].poly[2][0], block[-1].poly[2][1] = source.x_m, source.y_m
    for i in block:
        i.draw()


def motion(event):
    source.x_m, source.y_m = event.x, event.y


def click(event):
    if len(block) == 6:
        del block[0]
    if len(block) == 0 or block[-1].flag:
        block.append(Polygon(source.x_m, source.y_m, source.x_m, source.y_m, False))
    else:
        block[-1].flag = True


def space(event):
    block.clear()


def mouse_wheel(event):
    if event.delta == -120:
        if source.teta > pi / 24:
            source.teta -= pi / 24
    if event.delta == 120:
        if source.teta < pi / 2:
            source.teta += pi / 24


def direction(button):
    if button == 0:
        source.w = True
    if button == 4:
        source.w = False
    if button == 1:
        source.s = True
    if button == 5:
        source.s = False
    if button == 2:
        source.a = True
    if button == 6:
        source.a = False
    if button == 3:
        source.d = True
    if button == 7:
        source.d = False


def render():
    global t
    source.force()
    source.move()
    field.delete('all')
    source.beam()
    grid_draw()
    blocks_draw()
    source.draw()
    t1 = time()
    fps = int(1 / (t1 - t))
    root.title('FPS = ' + str(fps))
    t = t1
    root.after(10, render)


t = time()
width, height, side = 800, 500, 20


root = Tk()
root.geometry('+300+100')
field = Canvas(root, width=width, height=height, bg='silver')
field.pack()
source = Player(width // 2, height // 2)
block = [Polygon(200, 200, 250, 275, True), Polygon(500, 300, 550, 375, True)]
render()
root.bind('<Button-1>', click)
root.bind('<Motion>', motion)
root.bind('<space>', space)
root.bind('<MouseWheel>', mouse_wheel)
root.bind('<KeyPress-w>', lambda event: direction(0))
root.bind('<KeyRelease-w>', lambda event: direction(4))
root.bind('<KeyPress-s>', lambda event: direction(1))
root.bind('<KeyRelease-s>', lambda event: direction(5))
root.bind('<KeyPress-a>', lambda event: direction(2))
root.bind('<KeyRelease-a>', lambda event: direction(6))
root.bind('<KeyPress-d>', lambda event: direction(3))
root.bind('<KeyRelease-d>', lambda event: direction(7))
root.mainloop()
