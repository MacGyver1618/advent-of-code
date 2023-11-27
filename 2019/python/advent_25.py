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

machine = IntCodeMachine.from_day_input(25)

instructions=[
"west",
"take cake",
"west",
"south",
"take monolith",
"north",
"west",
"south",
"east",
"east",
"east",
"take mug",
"west",
"west",
"west",
"north",
"east",
"east",
"east",
"south",
"take coin",
"south",
"west",
"north",
"north",
"north",
"north"
]

for instruction in instructions:
    machine.run()
    output=machine.read_string()
    machine.input_line(instruction)

# This is a text adventure that is pretty easily solved interactively
# You could programmatically manipulate memory but that's easily more laborious
# And I'd need to create some memory manipulation / general debugging utility
# that would also be laborious

print("Part 1:", output.split()[-8])

print("Part 2:", "All done!")
