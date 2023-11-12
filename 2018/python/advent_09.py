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

lines = read_lines(9)
players,marbles=map(int,re.findall(r"\d+",lines[0]))
def play_game(players,marbles):
    Q=deque()
    scores=defaultdict(int)
    player=0
    for marble in range(marbles):
        if marble%23 == 0 and marble>0:
            scores[player]+=marble
            Q.rotate(7)
            scores[player]+=Q.pop()
            Q.rotate(-1)
        else:
            Q.rotate(-1)
            Q.append(marble)
        player=(player+1)%players
    return max(scores.values())

part1 = play_game(players,marbles)
print("Part 1:", part1)

part2 = play_game(players,marbles*100)
print("Part 2:", part2)
