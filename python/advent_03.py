from advent_lib import *
import itertools as iter
import math

input = lines(3)

def slope(ystep, xstep):
    return sum([1 for (x,y) in zip(range(0,xstep*len(input),xstep), range(0,len(input),ystep)) if input[y][x % len(input[y])] == '#'])

print("Part 1:", slope(1,3))
print("part 2:", math.prod(slope(x,y) for (x,y) in [(1,1), (1,3), (1,5), (1,7), (2,1)]))
