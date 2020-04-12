from gamegui import *
from math import sin, cos, tan, pi

root = Window((400, 400), caption='Demo - Star')
canvas = draw.Canvas(root, (350, 350))

canvas.aacircle((175, 175), 170, color=(255, 0, 0))
canvas.aacircle((175, 175), 170, fill=False)

length = 165
pointlist = []
for n in range(1, 6, 2):
    pointlist.append((175+int(length*cos(72*pi/180*n-54*pi/180)), 175+int(length*-sin(72*pi/180*n-54*pi/180))))
for n in range(2, 5, 2):
    pointlist.append((175+int(length*cos(72*pi/180*n-54*pi/180)), 175+int(length*-sin(72*pi/180*n-54*pi/180))))
canvas.aapolygon(pointlist, color=(255, 255, 0))

length = length//(cos(36*pi/180)+sin(36*pi/180)*tan(72*pi/180))
pointlist.clear()
for n in range(1, 6):
    pointlist.append((175+int(length*cos(72*pi/180*n-18*pi/180)), 175+int(length*-sin(72*pi/180*n-18*pi/180))))
canvas.aapolygon(pointlist, color=(255, 255, 0))

canvas.place((25, 25))

mainloop()
