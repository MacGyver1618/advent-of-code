from collections import defaultdict
import re

from common.advent_lib import *

inpt = lines(24)

dirs = {
    "e":  A([-1,0,1]),
    "w":  A([1,0,-1]),
    "se": A([0,-1,1]),
    "sw": A([1,-1,0]),
    "ne": A([-1,1,0]),
    "nw": A([0,1,-1])
}

grid = defaultdict(lambda: False)

for line in inpt:
    instrs = re.split(r"(?=[nswe])(?<![ns])",line)[1:]
    p = A([0,0,0])
    for instr in instrs:
        p += dirs[instr]
    grid[tuple(p)] = not grid[tuple(p)]

part1 = sum([1 for p in grid.values() if p == True])
print("Part 1:", part1)


tiles = set([k for k,v in grid.items() if v == True])

for _ in range(100):
    neighbors = defaultdict(lambda: 0)
    for point in tiles:
        p = A(point)
        for n in dirs.values():
            neighbors[tuple(p+n)] += 1
    nextgen = set()
    for k,v in neighbors.items():
        if k in tiles and 0 < v <= 2:
            nextgen.add(k)
        elif k not in tiles and v == 2:
            nextgen.add(k)
    tiles = nextgen

part2 = len(tiles)
print("Part 2:", part2)