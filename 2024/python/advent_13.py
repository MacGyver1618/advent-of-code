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

instrs=full_input(13).strip().split("\n\n")

part1=0
part2=0
for instr in instrs:
    ax,ay,bx,by,px,py=parse_ints(instr)
    N=(ay*px-ax*py)//(ay*bx-ax*by)
    M=(px-N*bx)//ax
    if M*ax+N*bx==px and M*ay+N*by==py:
        part1+=3*M+N
    px+=10000000000000
    py+=10000000000000
    N=(ay*px-ax*py)//(ay*bx-ax*by)
    M=(px-N*bx)//ax
    if M*ax+N*bx==px and M*ay+N*by==py:
        part2+=3*M+N

print("Part 1:", part1)
print("Part 2:", part2)
