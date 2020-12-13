from advent_lib import *
import re
from numpy import array as A

actions = lines(12)

ds = {
    "N": A([0, -1]),
    "E": A([1, 0]),
    "S": A([0, 1]),
    "W": A([-1, 0])
}
R = A([[0, -1],
       [ 1, 0]])
L = R.T

p = A([0, 0])
d = A([1, 0])

for action in actions:
    i, amt = re.match(r"(.)(\d+)", action).groups()
    r = int(amt)

    if i in ("N", "S", "E", "W"):
        p += r * ds[i]
    elif i == "L":
        for _ in range(r // 90):
            d = L @ d
    elif i == "R":
        for _ in range(r // 90):
            d = R @ d
    elif i == "F":
        p += r * d

print("Part1:", sum(abs(p)))

wp = A([10,-1])
p = A([0,0])

for action in actions:
    i, amt = re.match(r"(.)(\d+)", action).groups()
    r = int(amt)

    if i in ("N", "S", "E", "W"):
        wp += r*ds[i]
    elif i == "L":
        for _ in range(r // 90):
            wp = p + L @ (wp-p)
    elif i == "R":
        for _ in range(r // 90):
            wp = p + R @ (wp-p)
    elif i == "F":
        h = wp-p
        p += r*h
        wp += r*h

print("Part2:", sum(abs(p)))
