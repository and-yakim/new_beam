from tkinter import *


class Dot:
    def __init__(self, x, y, canvas):
        self.x, self.y = x, y
        self.canvas = canvas
        self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill='black')


class Triangulation:
    def __init__(self):
        self.width, self.height = 800, 500
        self.root = Tk()
        self.root.geometry('+300+100')

        self.field = Canvas(self.root, width=self.width,
                            height=self.height, bg='silver')
        self.field.pack()
        self.dots = []

        self.root.bind('<Button-1>', self.click)

        self.root.mainloop()

    def 

    def click(self, event):
        self.dots.append(Dot(event.x, event.y, self.field))


def main():
    Triangulation()


if __name__ == '__main__':
    main()
