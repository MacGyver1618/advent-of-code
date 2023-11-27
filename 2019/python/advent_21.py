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

machine=IntCodeMachine.from_day_input(21)
instructions = [
    "NOT A J",
    "NOT C T",
    "AND D T",
    "OR J T",
    "NOT T T",
    "NOT T J",
    "WALK"
]
for instruction in instructions:
    machine.input_line(instruction)
machine.run()
part1 = machine.read_all()[-1]
print("Part 1:", part1)

machine=IntCodeMachine.from_day_input(21)
instructions = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND H J",
    "OR E J",
    "AND D J",
    "RUN"
]
for instruction in instructions:
    machine.input_line(instruction)
machine.run()
part2 = machine.read_all()[-1]
print("Part 2:", part2)
