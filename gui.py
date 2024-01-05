import sys
import tkinter
import a_serial
import numpy as np
import math
from math import cos, sin
from math import radians as rad
import random
import schiefe_ebene
from schiefe_ebene import sensor
import json

# Die Class Sensor wird jetzt aus schiefe_ebene.py geholt
"""
class sensor:
    def __init__(self, winkel, pos, radius):
        self.winkel = winkel
        self.posz = pos
        self.radius = radius
        self.posx = cos(rad(winkel))*radius
        self.posy = sin(rad(winkel))*radius

    def __str__(self):
        return f"{self.winkel} POSZ:{self.posz}"

    def xy_p(self):
        return f"x:{self.posx} y:{self.posy}"

    def martrix(self, alpa=0, x=1,y=1):
        xy = np.matrix([[self.posx],
                        [self.posy]])
        xy_trans = self.translation(x=x,y=y) * self.rotation(angel=alpa)
        xy = xy_trans * xy
        return xy

    def rotation(self, angel=0):
        rot = np.matrix([[cos(rad(angel)), -sin(rad(angel))],
                         [sin(rad(angel)), cos(rad(angel))]])
        return rot

    def translation(self, x, y):
        trans = np.matrix([[x,0],
                          [0,y]])
        return trans
"""

# größe des zeichenbereiches
global frame_width, frame_hight, window_with ,window_hight
window_hight = 720
window_with = window_hight*16/9
frame_hight = window_hight*0.6
frame_width = window_hight*0.6

from tkinter import *
from tkinter import messagebox


class App:
    def __init__(self, master):
        self.frame = Frame(master)
        self.canvasframe = Frame(master, borderwidth=1, highlightthickness=1, highlightbackground="grey")
        self.stausframe = Frame(master)
        self.graph = Frame(master,borderwidth=1, highlightthickness=1, highlightbackground="grey")
        # self.e1 = Scale(self.frame, from_=1, to=16, orient=HORIZONTAL) #anzahl der Sensoren
        self.a1 = Label(self.frame)  # Anzahl der Sensoren
        self.a2 = Label(self.frame)  # Radius
        self.e2 = Scale(self.frame, from_=0, to=360, orient=HORIZONTAL)  # rodation der Sensoren
        self.e3_x = Scale(self.frame, from_=0, to=5, orient=HORIZONTAL, resolution=0.1)  # denung in x
        self.e3_y = Scale(self.frame, from_=0, to=5, orient=VERTICAL, resolution=0.1)  # denung in y
        self.e4_r = Entry(self.frame, name="9,225")  # radius eingabe
        self.text = Label(self.frame)  # ausgabe hilfe debug
        self.grafik = Canvas(self.canvasframe, width=frame_width, height=frame_hight)  # grafik ausgabe
        self.t_verbindung = Label(self.stausframe, text="Verbindung: ")
        self.b_verbinden = Button(self.stausframe, text="Verbinden", command=self.verbinden)
        self.in_conectet = Canvas(self.stausframe, width=30, height=30)  # bereich der status aus gabe
        self.pos_c = Canvas(self.stausframe, width=100, height=80, borderwidth=1, highlightthickness=1,
                            highlightbackground="grey")  # zeigt die xyz position
        self.touch = Button(self.stausframe, text="touch", command=self.touch)
        self.pos_text = Label(self.stausframe)
        self.pack()  # sorgt dafür das alle ellmente angezeigt werden
        self.settings()  # lät die optionen
        self.frame.after(1, self.loop)  # startet den loop für die Frame generigung
        self.n = 0

    def verbinden(self):
        a_serial.stop()
        a_serial.go()

    def touch(self):
        a_serial.t.write("touch")

    def loop(self):  # aktualliset das Bild alle 16ms
        self.n += 1
        self.show_text()
        self.in_update()
        self.draw()
        self.xyz()
        self.frame.after(16,self.loop)

    def settings(self):
        # öffnet die .json um die optionen zu holen
        with open("options.json", "r") as f:
            config_file = json.load(f)
        self.anzahl = int(config_file["anzahl"])
        self.radius = float(config_file["radius"])

    def show_text(self):
        self.text.configure(text=str(self.e4_r.get()))
        self.settings()
        self.a1.configure(text=str(f"Anzahl: {self.anzahl}"))
        self.a2.configure(text=str(f"Radius: {self.radius}"))

    def set_sensor(self):
        self.settings()
        for n in range(self.anzahl):
            w = 360 / self.anzahl
            ''' 1. Sensorwert in Probe setzen 
                2. Sensorwert in Probe auf null setzen
                3. Neuen sensor in Probe erstellen wert 0
                4. Neuen Sensor in Probe erstellen mit messert'''
            try:
                schiefe_ebene.p.s[n] = sensor(w * n, 0, self.radius)
            except IndexError:
                try:
                    schiefe_ebene.p.s[n] = sensor(w * n, 0, self.radius)
                except:
                    schiefe_ebene.p.s.append(sensor(w * n, 0, self.radius))
            except:
                schiefe_ebene.p.s.append(sensor(w * n, 0, self.radius))
            # print(schiefe_ebene.p.s[n].martrix())

    def draw(self):
        def circle(x, y, r, z=0):
            if z < 0:
                color = '#{:02x}{:02x}{:02x}'.format(min(int(255 * math.fabs(z)*30),255), 0, 0)
            elif z > 0:
                color = '#{:02x}{:02x}{:02x}'.format(0, min(int(255 * math.fabs(z))*10,255), 0)
            else:
                color = '#{:02x}{:02x}{:02x}'.format(0, 0, 0)
            id = self.grafik.create_oval(x - r, y - r, x + + r, y + r, outline=color, fill=color)
            return id

        def cross(x, y, r, angel, color="black"):
            id0 = self.grafik.create_line(x - r * sin(rad(angel)), y - r * cos(rad(angel)), x + r * sin(rad(angel)),
                                          y + r * cos(rad(angel)), fill=color)
            id1 = self.grafik.create_line(x - r * sin(rad(90 - angel)), y + r * cos(rad(90 - angel)),
                                          x + r * sin(rad(90 - angel)), y - r * cos(rad(90 - angel)), fill=color)
            return id0, id1

        self.grafik.delete("all")

        for n in range(self.anzahl):
            circle(schiefe_ebene.p.s[n].martrix(self.e2.get(), x=self.e3_x.get())[0, 0] * 5,
                   schiefe_ebene.p.s[n].martrix(self.e2.get(), y=self.e3_y.get())[1, 0] * 5, 4,
                   schiefe_ebene.p.s[n].posz)
        cross(0, 0, 10, 0)

    def xyz(self):
        def cross(x, y, r, angel, color="black"):
            id0 = self.pos_c.create_line(x - r * sin(rad(angel)), y - r * cos(rad(angel)), x + r * sin(rad(angel)),
                                         y + r * cos(rad(angel)), fill=color)
            id1 = self.pos_c.create_line(x - r * sin(rad(90 - angel)), y + r * cos(rad(90 - angel)),
                                         x + r * sin(rad(90 - angel)), y - r * cos(rad(90 - angel)), fill=color)
            return id0, id1

        self.pos_c.delete("all")
        cross(40, 40, 6, 45, "grey")
        x, y, z = schiefe_ebene.p.tip_x, schiefe_ebene.p.tip_y, schiefe_ebene.p.tip_z
        cross(40 + x * 40, 40 + y * 40, 6, 0)
        self.pos_c.create_line(81, 40 + z * 20, 100, 40 + z * 20)
        self.pos_text.configure(text=f"X: {x:.5f}\nY: {y:.5f}\nZ: {z:.5f}", justify="left")

    def in_update(self):
        def circle(x, y, r):
            match a_serial.t.verbindung:
                case 1:
                    color = 'green'
                    self.b_verbinden.configure(state=DISABLED)

                case 0:
                    color = 'red'
                    self.b_verbinden.configure(state=NORMAL, fg='black')

                case 2:
                    color = 'orange'
                    self.b_verbinden.configure(state=DISABLED)

            id = self.in_conectet.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
            return id

        self.in_conectet.delete("all")
        circle(15, 15, 10)

    def pack(self):  # packed alle Bilder
        self.frame.grid(row=0, column=0, sticky=NW)
        self.stausframe.grid(row=0, column=1, sticky=W)
        self.stausframe.columnconfigure(1, weight=5)
        self.canvasframe.grid(row=1, column=0, columnspan=2, sticky=N)
        self.graph.grid(row=0, column=2, rowspan=2)

        self.e3_y.set(2)
        self.e3_y.pack(side=RIGHT)
        # self.e1.pack(side=TOP)
        # self.e1.set(8)
        self.a1.pack(side=TOP)
        self.a2.pack(side=TOP)
        self.e2.pack(side=TOP)
        self.e3_x.set(2)
        self.e3_x.pack(side=TOP)
        self.e4_r.pack(side=BOTTOM)
        self.text.pack()

        self.grafik.pack()
        self.grafik.configure(scrollregion=(-frame_width / 2, -frame_hight / 2, frame_width / 2, frame_hight / 2))

        self.t_verbindung.grid(row=0, column=0, sticky=W)
        self.in_conectet.grid(row=0, column=1, sticky=W)
        self.b_verbinden.grid(row=1, column=0, sticky=W)
        self.touch.grid(row=1, column=1)
        self.pos_c.grid(row=2, column=0, columnspan=2, sticky=W)
        self.pos_text.grid(row=3, column=0, sticky=W)

    def on_closing(self):  # wird beim schließen ausgefürt
        try:
            a_serial.stop()  # stoppt die Hintergrungaufgabe
            a_serial.exit()
            schiefe_ebene.stop()
            print(schiefe_ebene.b.n)
            print(app.n)
            print(a_serial.t.n)
        except:
            None
        root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # verknüpft das schließen mit der funktion on_closing
    schiefe_ebene.b.start()
    root.mainloop()
