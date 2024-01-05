import numpy as np
import numpy as np
import math
from math import cos, sin
from math import radians as rad, degrees as deg
import random
import json
from statistics import mean
import time
import threading


class sensor:
    def __init__(self, winkel, pos, radius):
        self.winkel = winkel
        self.posz = pos
        self.radius = radius
        self.posx = cos(rad(winkel)) * radius
        self.posy = sin(rad(winkel)) * radius

    def __str__(self):  # wird bei pirnt ausgeführt
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


class probe:
    def __init__(self):
        self.s = []
        with open("options.json", "r") as f:
            config_file = json.load(f)
        self.anzahl = int(config_file["anzahl"])
        self.radius = float(config_file["radius"])
        self.lenght = float(config_file["length"])
        self.ball_radius = float(config_file["ball_radius"])
        self.tip_x ,self.tip_y ,self.tip_z = 0,0,0

    def winkel_zx(self):
        usedi = []
        winkel = []
        for n in range(self.anzahl):
            try:
                usedi.index(n)
            except:
                a = self.s[n].winkel
                sa = sin(rad(a))
                if a == 90 or a == 270:
                    None
                else:
                    for i in range(self.anzahl):
                        if sa == sin(rad(self.s[i].winkel)) and i != n:
                            usedi.append(i)
                            winkel.append(self.winkel(self.s[i].posz, self.s[n].posz, self.s[n].posx))
        self.xz_winkel = mean(winkel)
        return self.xz_winkel

    def winkel_zy(self):
        usedi = []
        winkel = []
        for n in range(self.anzahl):
            try:
                usedi.index(n)
            except:
                a = self.s[n].winkel
                sa = round(cos(rad(a)), 10)
                if a == 0 or a == 180:
                    None
                else:
                    for i in range(self.anzahl):
                        if sa == round(cos(rad(self.s[i].winkel)), 10) and i != n:
                            usedi.append(i)
                            winkel.append(self.winkel(self.s[i].posz, self.s[n].posz, self.s[n].posy))
        self.zy_winkel = mean(winkel)
        return self.zy_winkel

    def winkel(self, z1, z2, l):
        alpha = math.degrees(math.atan((z1 - z2) / (2 * l)))
        return alpha

    def z(self):
        z = 0
        for n in range(len(self.s)):
            z += self.s[n].posz
        z = z/(n+1)
        return z

    def tip_displacement(self):
        self.tip_x = sin(rad(self.winkel_zx())) * self.lenght
        self.tip_y = sin(rad(self.winkel_zy())) * self.lenght
        self.tip_z = (self.lenght - cos(rad(self.zy_winkel)) * (cos(rad(self.xz_winkel)) * self.lenght)) + self.z()

p = probe()

class background(threading.Thread):
    def run(self, *args):
        self.stop = False
        self.n = 0
        while self.stop == False:
            self.n += 1
            p.tip_displacement()
            time.sleep(0.000001)



b = background()

def stop():
    b.stop = True

radius = 5
p.s.append(sensor(0, 0.08727532, radius))
p.s.append(sensor(45, 0.12342595, radius))
p.s.append(sensor(90, 0.08727532, radius))
p.s.append(sensor(135, 0, radius))
p.s.append(sensor(180, -0.08727532, radius))
p.s.append(sensor(225, -0.12342595, radius))
p.s.append(sensor(270, -0.08727532, radius))
p.s.append(sensor(315, -0, radius))




# time1 = time.time()
# a = 1000
# for n in range(a):
#  p.winkel_zy()
#  p.winkel_zx()
# time2 = time.time()
# print(1/((time2-time1)/a))
#
'''
s = []
anzahl = 8
radius = 9.225

def rand():
  r = random.uniform(-0.001,0.001)
  return 0

s.append(sensor(0, 0.08727532+rand() , radius))
s.append(sensor(45, 0.12342595+rand() , radius))
s.append(sensor(90, 0.08727532 , radius))
s.append(sensor(135, 0 , radius))
s.append(sensor(180, -0.08727532 , radius))
s.append(sensor(225, -0.12342595 , radius))
s.append(sensor(270, -0.08727532 , radius))
s.append(sensor(315, -0 , radius))

def angel(z1,z2,l):
  alpha = math.degrees(math.atan((z1-z2)/(2*l)))
  return alpha

alpha = []
beta = []

alpha.append(angel(s[0].posz, s[4].posz, s[0].posx))
alpha.append(angel(s[1].posz, s[3].posz, s[1].posx))
alpha.append(angel(s[7].posz, s[5].posz, s[7].posx))

beta.append(angel(s[1].posz, s[7].posz, s[1].posy))
beta.append(angel(s[2].posz, s[6].posz, s[2].posy))
beta.append(angel(s[3].posz, s[5].posz, s[3].posy))

def avrage(list):
  i = 0
  a = 0
  for n in range(len(list)):
    a += list[n]
    i = n+1
  a = a/i
  return a

def z():
  z=0
  for n in range(anzahl):
    z += s[n].posz
    z = z/anzahl
  return z

def xyz_out(a_x, a_y, l, k):
  x = sin(rad(a_x))*l
  y = sin(rad(a_y))*l
  z = (cos(rad(a_x))*l+cos(rad(a_y))*l)/2
  return x,y,z


print(avrage(alpha).__round__(5))
print(avrage(beta).__round__(5))
print(z().__round__(5))
print(xyz_out(avrage(alpha),avrage(beta),18.8,4))
'''
