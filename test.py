import numpy as np
import math
from math import cos, sin
from math import radians as rad
import random


class sensor:
    def __init__(self, winkel, pos, radius):
        self.winkel = winkel
        self.posz = pos
        self.radius = radius
        self.posx = cos(rad(winkel)) * radius
        self.posy = sin(rad(winkel)) * radius

    def __str__(self):
        return f"{self.winkel} POSZ:{self.posz}"

    def xy_p(self):
        return f"x:{self.posx} y:{self.posy}"

    def martrix(self, alpa=0, x=1, y=1):
        xy = np.matrix([[self.posx],
                        [self.posy]])
        xy_trans = self.translation(x=x, y=y) * self.rotation(angel=alpa)
        xy = xy_trans * xy
        return xy

    def rotation(self, angel=0):
        rot = np.matrix([[cos(rad(angel)), -sin(rad(angel))],
                         [sin(rad(angel)), cos(rad(angel))]])
        return rot

    def translation(self, x, y):
        trans = np.matrix([[x, 0],
                           [0, y]])
        return trans


from tkinter import *

class tastleiste:
    def __init__(self, master):
        self.frame = Frame(master)
        self.b1 = Button(self.frame, text="1", command=lambda : test2.close(test2))
        self.b2 = Button(self.frame, text="2", command=lambda: test2(root))

    def pack_all(self, side):
        self.frame.pack(side=side)
        self.b1.pack(side=LEFT)
        self.b2.pack(side=LEFT)

class test2:
    def __init__(self, master):
        self.frame = Frame(master)
        self.test1 = Label(self.frame, text="test2")
        self.pack(BOTTOM)

    def pack(self, side):
        self.frame.pack(side=side)
        self.test1.pack()

    def close(self):
        self.frame.destroy()

class App:
    def __init__(self, master):
        self.tastleiste = tastleiste(master)
        self.tastleiste.pack_all(TOP)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()

