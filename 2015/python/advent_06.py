from common.advent_lib import *
import re
import numpy as np

inpt = lines(6)
grid = np.zeros((1000,1000), dtype=int)

for instr in inpt:
    op,x1,y1,x2,y2 = re.match(r"(turn off|turn on|toggle) (\d+),(\d+) through (\d+),(\d+)", instr).groups()
    x1,x2,y1,y2 = map(int, [x1,x2,y1,y2])
    for x,y in [(x,y) for x in range(x1,x2+1) for y in range(y1,y2+1)]:
        if op == "turn on":
            grid[x][y] = 1
        elif op == "turn off":
            grid[x][y] = 0
        elif op == "toggle":
            grid[x][y] = 1-grid[x][y]

print("Part 1:", grid.sum())

grid = np.zeros((1000,1000), dtype=int)

for instr in inpt:
    op,x1,y1,x2,y2 = re.match(r"(turn off|turn on|toggle) (\d+),(\d+) through (\d+),(\d+)", instr).groups()
    x1,x2,y1,y2 = map(int, [x1,x2,y1,y2])
    for x,y in [(x,y) for x in range(x1,x2+1) for y in range(y1,y2+1)]:
        if op == "turn on":
            grid[x][y] += 1
        elif op == "turn off":
            grid[x][y] = max(0, grid[x][y]-1)
        elif op == "toggle":
            grid[x][y] += 2

print("Part 2:", grid.sum())
