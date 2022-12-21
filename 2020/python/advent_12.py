from common.advent_lib import *
import re
from numpy import array

actions = read_lines(12)

ds = {
    "N": (0,-1),
    "E": (1,0),
    "S": (0,1),
    "W": (-1,0),
}

p = (0,0)
d = (1,0)

for action in actions:
    (i, s) = re.match(r"(.)(\d+)", action).groups()
    amt = int(s)
    x,y = p
    dx,dy = (0,0)

    if i in ("N", "S", "E", "W"):
        dx, dy = ds[i]
        dx *= amt
        dy *= amt
    elif i == "L":
        for _ in range(amt//90):
            a,b = d
            d = (1*b,-1*a)
    elif i == "R":
        for _ in range(amt//90):
            a,b = d
            d = (-1*b,1*a)
    elif i == "F":
        dx, dy = d
        dx *= amt
        dy *= amt
    p = (x+dx, y+dy)

x,y = p
part1 = abs(x)+abs(y)
print("Part1:", part1)

wp = (10,-1)
p = (0,0)
d = (1,0)

for action in actions:
    (i, s) = re.match(r"(.)(\d+)", action).groups()
    amt = int(s)
    x,y = p
    wx,wy = wp
    dx,dy = (0,0)
    dwx = wx-x
    dwy = wy-y

    if i in ("N", "S", "E", "W"):
        dx, dy = ds[i]
        dx = amt*dx
        dy = amt*dy
        wp = (wx+dx, wy+dy)
    elif i == "L":
        for _ in range(amt//90):
            dwx,dwy = (1*dwy,-1*dwx)
        wp = (x+dwx, y+dwy)
    elif i == "R":
        for _ in range(amt//90):
            dwx,dwy = (-1*dwy,1*dwx)
        wp = (x+dwx, y+dwy)
    elif i == "F":
        dx = amt*dwx
        dy = amt*dwy
        p = (x+dx, y+dy)
        wp = (wx+dx, wy+dy)

x,y = p
part2 = abs(x)+abs(y)
print("Part2:", part2)