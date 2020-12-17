from advent_lib import *
import re
import functools as func
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(11)[0]

abc = "abcdefghijklmnopqrstuvwxyz"
triples = list(map("".join, zip(abc, abc[1:], abc[2:])))

def is_valid(pw):
    has_triple = any(map(pw.count, triples))
    no_ambiguous = not re.findall(r"[iol]", pw)
    two_doubles = re.findall(r"(.)\1.*((?!\1).)\2", pw)
    return has_triple and no_ambiguous and two_doubles

def increment(pw):
    next = list(reversed(pw))
    for i,char in enumerate(pw[-1::-1]):
        val = abc.index(char)
        next[i] = abc[(val + 1) % 26]
        if val < 25:
            return "".join(reversed(next))
    return str(reversed(next))

part1 = it2.first_true(it2.iterate(increment, inpt), pred=is_valid)
print("Part 1:", part1)

part2 = it2.first_true(it2.iterate(increment, increment(part1)), pred=is_valid)
print("Part 2:", part2)
