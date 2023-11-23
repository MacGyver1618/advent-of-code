from common.advent_lib import *
from intcode import IntCodeMachine
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

program = [int(n) for n in read_lines(2)[0].split(",")]

def init_with(a,b):
    new_program = program.copy()
    new_program[1]=a
    new_program[2]=b
    return new_program
machine = IntCodeMachine(init_with(12,2))
machine.run()
part1 = machine.val_at(0)
print("Part 1:", part1)

try:
    for a in range(100):
        for b in range(100):
            machine = IntCodeMachine(init_with(a,b))
            machine.run()
            result = machine.val_at(0)
            if result == 19690720:
                part2 = 100*a+b
                raise Exception
except Exception:
    pass

print("Part 2:", part2)
