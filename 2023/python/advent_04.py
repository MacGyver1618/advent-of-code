import math

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

lines = read_lines(4)

tot=0
card_count={(i+1):1 for i in range(len(lines))}
for line in lines:
    card_no,rest=line.split(": ")
    card_no=int(card_no.split()[1])
    wins,drawn=rest.split(" | ")
    common=len({*wins.split()}.intersection({*drawn.split()}))
    if common:
        tot+=2**(common - 1)
    for i in range(common):
        card_count[card_no + i + 1]+=card_count[card_no]

part1 = tot
print("Part 1:", part1)

part2=sum(card_count.values())
print("Part 2:", part2)

