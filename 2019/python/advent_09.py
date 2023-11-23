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

program=[*map(int,read_lines(9)[0].split(","))]

machine = IntCodeMachine(program)
machine.input(1)
machine.run()

part1 = machine.read()
print("Part 1:", part1)

machine = IntCodeMachine(program)
machine.input(2)
machine.run()

part2 = machine.read()
print("Part 2:", part2)
