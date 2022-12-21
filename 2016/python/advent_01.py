import re

from common.advent_lib import *

inpt = read_lines(1)[0].split(", ")

p = 0
dir = 1
part2 = None
history = set()
history.add(p)
for i in inpt:
    d,a = re.split(r"(?<=[LR])", i)
    dir *= 1j if d == "L" else -1j
    dest = p+dir*int(a)
    while p != dest:
        p += dir
        if part2 == None and p in history:
            # print(p)
            part2 = p
        history.add(p)

print("Part 1:", int(abs(p.real)+abs(p.imag)))

print("Part 2:", int(abs(part2.real)+abs(part2.imag)))
