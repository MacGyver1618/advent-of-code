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

lines = read_lines(2)
num=0
power=0
for line in lines:
    game,rest=line.split(": ")
    game_no=int(game.split()[1])
    sets=rest.split("; ")
    game=defaultdict(int)
    possible=True
    for _set in sets:
        colors={}
        draws=_set.split(", ")
        for draw in draws:
            count,color=draw.split()
            count=int(count)
            colors[color]=count
            game[color]=max(game[color],count)
            if color=="red" and count > 12:
                possible=False
            if color=="green" and count > 13:
                possible=False
            if color=="blue" and count > 14:
                possible=False
    power+=game["red"]*game["green"]*game["blue"]
    if possible:
        num+=game_no

part1 = num
print("Part 1:", part1)

part2 = power
print("Part 2:", part2)
