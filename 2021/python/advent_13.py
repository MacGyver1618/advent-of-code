from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(13)

dots = set()
part1 = ""
for line in inpt:
    if not line:
        continue
    if not line.startswith("fold"):
        x,y = line.split(",")
        dots.add((int(x),int(y)))
    else:
        dim, coord = re.match(r"fold along (x|y)=(\d+)", line).groups()
        coord = int(coord)
        new_dots = set()
        for x,y in dots:
            if dim == 'x' and x > coord:
                new_dots.add((2*coord-x,y))
            elif dim == 'y' and y > coord:
                new_dots.add((x,2*coord-y))
            else:
                new_dots.add((x,y))
        if not part1:
            part1 = len(new_dots)
        dots = new_dots

for y in range(0, inc(max(map(second, dots)))):
    print("".join(["#" if (x,y) in dots else " " for x in (range(0, inc(max(map(first, dots)))))]))

print("Part 1:", part1)

print("Part 2:", "see above")
