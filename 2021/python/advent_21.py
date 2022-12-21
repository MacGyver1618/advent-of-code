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

inpt = read_lines(21)
p1start = int(inpt[0].split()[-1])
p2start = int(inpt[1].split()[-1])

p1score = 0
p2score = 0
p1pos = p1start
p2pos = p2start

throws = 0

while True:
    throws += 3
    p1pos = (p1pos + (3*throws-6) % 100 + 2) % 10 + 1
    p1score += p1pos
    if p1score >= 1000:
        part1 = p2score * throws
        break
    throws += 3
    p2pos = (p2pos + (3*throws-6) % 100 + 2) % 10 + 1
    p2score += p2pos
    if p2score >= 1000:
        part1 = p1score * throws
        break

print("Part 1:", part1)

rolls = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

start = (p1start-1, 0, p2start-1, 0)
memo = {}

def find_wins(state):
    p1,s1,p2,s2 = state
    if s2 >= 21:
        return (0,1)
    if state in memo:
        return memo[state]
    p1_wins, p2_wins= (0,0)
    for i in [1,2,3]:
        for j in [1,2,3]:
            for k in [1,2,3]:
                p1_new = (p1+i+j+k) % 10
                s1_new = s1 + p1_new + 1
                w1, w2 = find_wins((p2, s2, p1_new, s1_new))
                p1_wins += w2
                p2_wins += w1
    memo[state] = p1_wins, p2_wins
    return p1_wins, p2_wins



part2 = max(find_wins(start))
print("Part 2:", part2)
