from common.advent_lib import *
import re
from numpy import array

actions = lines(12)

ds = {
    "N": -1j,
    "E": 1,
    "S": 1j,
    "W": -1,
}

p = 0
d = 1

for action in actions:
    (i, s) = re.match(r"(.)(\d+)", action).groups()
    amt = int(s)

    if i in ("N", "S", "E", "W"):
        p += amt*ds[i]
    elif i == "L":
        d *= (-1j)**(amt//90)
    elif i == "R":
        d *= 1j**(amt//90)
    elif i == "F":
        p += amt*d

print("Part 1:", int(abs(p.real)+abs(p.imag)))

wp = 10-1j
p = 0
d = 1

for action in actions:
    (i, s) = re.match(r"(.)(\d+)", action).groups()
    amt = int(s)

    if i in ("N", "S", "E", "W"):
        wp += amt*ds[i]
    elif i == "L":
        wp = p + (wp-p)*(-1j)**(amt//90)
    elif i == "R":
        wp = p + (wp-p)*1j**(amt//90)
    elif i == "F":
        d = wp-p
        p += amt*d
        wp += amt*d

print("Part 2:", int(abs(p.real)+abs(p.imag)))