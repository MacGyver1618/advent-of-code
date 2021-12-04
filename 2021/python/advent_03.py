from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(3)

bits = [0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(12):
    for line in inpt:
        bits[i] += int(line[i])

most_common = ["1" if b >= 500 else "0" for b in bits]
least_common = ["1" if b < 500 else "0" for b in bits]

gamma   = int("".join(most_common), 2)
epsilon = int("".join(least_common), 2)

part1 = gamma*epsilon
print("Part 1:", part1)

oxygen_gen = inpt.copy()
for i in range(12):
    ones,zeros = 0,0
    for line in oxygen_gen:
        ones += 1 if line[i] == "1" else 0
        zeros += 1 if line[i] == "0" else 0
    most_common = "1" if ones >= zeros else "0"
    oxygen_gen = [x for x in oxygen_gen if x[i] == most_common]
    if len(oxygen_gen) == 1:
        oxygen_gen = int(oxygen_gen[0],2)
        break

scrubber = inpt.copy()
for i in range(12):
    ones,zeros = 0,0
    for line in scrubber:
        ones += 1 if line[i] == "1" else 0
        zeros += 1 if line[i] == "0" else 0
    least_common = "1" if ones < zeros else "0"
    scrubber = [x for x in scrubber if x[i] == least_common]
    if len(scrubber) == 1:
        scrubber = int(scrubber[0],2)
        break

part2 = scrubber*oxygen_gen
print("Part 2:", part2)
