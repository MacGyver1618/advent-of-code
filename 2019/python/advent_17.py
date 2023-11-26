import time

from common.advent_lib import *
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

from intcode import IntCodeMachine

machine=IntCodeMachine.from_day_input(17)
machine.run()
s="".join(chr(c) for c in machine.read_all())

grid=[[c for c in line] for line in s.strip().split("\n")]
R=len(grid)
C=len(grid[0])

def is_intersection(r,c):
    if r in (0,R-1):
        return False
    if c in (0,C-1):
        return False
    return all(grid[_r][_c] == "#" for _r,_c in ((r,c),(r-1,c),(r+1,c),(r,c-1),(r,c+1)))

tot=0
for r in range(R):
    for c in range(C):
        if is_intersection(r,c):
            tot+=r*c

part1 = tot
print("Part 1:", part1)

visual=False

machine = IntCodeMachine.from_day_input(17)
machine.set_val(0,2)
machine.input_line("A,B,B,C,B,C,B,C,A,A")
machine.input_line("L,6,R,8,L,4,R,8,L,12")
machine.input_line("L,12,R,10,L,4")
machine.input_line("L,12,L,6,L,4,L,4")
machine.input_line("y" if visual else "n")
machine.run()

output=machine.read_all()
part2=output[-1]
print("Part 2:", part2)

if visual:
    input("Start playback by pressing enter")
    visual_stream="".join(chr(c) for c in output[:-1])
    frames=visual_stream.split("\n\n")
    for frame in frames:
        print(frame)
        print()
        time.sleep(1/4)
