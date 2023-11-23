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

program=[*map(int,read_lines(7)[0].split(","))]

max_signal=float("-inf")
for perm in it.permutations([0,1,2,3,4]):
    signal=0
    for phase in perm:
        machine = IntCodeMachine(program)
        machine.input(phase)
        machine.input(signal)
        machine.run()
        signal=machine.read()
    if signal > max_signal:
        max_signal = signal

part1 = max_signal
print("Part 1:", part1)


max_signal=float("-inf")
for perm in it.permutations([5,6,7,8,9]):
    signal=0
    machines=[IntCodeMachine(program) for _ in range(5)]
    for i,phase in enumerate(perm):
        machines[i].input(phase)
    i=0
    while True:
        if machines[i].finished():
            break
        machines[i].input(signal)
        machines[i].run()
        signal=machines[i].read()
        i = (i+1)%5
    if signal > max_signal:
        max_signal = signal

part2 = max_signal
print("Part 2:", part2)
