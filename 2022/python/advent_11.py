import sympy.ntheory

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

groups = full_input(11).split("\n\n")

monkeys = {}
all_mods = 1
for group in groups:
    lines = group.split("\n")
    no = int(lines[0].split()[1][:-1])
    items = to_nums(lines[1].split(": ")[1].split(", "))
    op = lines[2].split(": ")[1]
    if re.search(r"old [*] old", op):
        op = lambda x: x*x
    elif re.search(r"[*]", op):
        const = int(op.split()[-1])
        op = lambda x, const=const: const*x
    else:
        const = int(op.split()[-1])
        op = lambda x, const=const: const+x
    divisor = int(lines[3].split(" ")[-1])
    all_mods *= divisor
    if_true = int(lines[4].split()[-1])
    if_false = int(lines[5].split()[-1])
    monkeys[no] = (items, op, divisor, if_true, if_false)

def solve(part):
    inspections = [0 for _ in range(len(monkeys))]

    def throw_to(monkey, thing):
        things, *rest = monkeys[monkey]
        things.append(thing)

    for round in range(20 if part == 1 else 10000):
        for i in range(len(monkeys)):
            items, op, divisor, if_true, if_false = monkeys[i]
            for item in items:
                inspections[i] += 1
                item = op(item)
                if part == 1:
                    item //= 3
                else:
                    item %= all_mods
                if item % divisor == 0:
                    throw_to(if_true, item)
                else:
                    throw_to(if_false, item)
            items.clear()
    return product(sorted(inspections)[-2:])

# print("Part 1:", solve(1))
print("Part 2:", solve(2))
