from common.advent_lib import *
import re
import functools as func
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(13)
prefs = {}
people = set()
for line in inpt:
    a,sgn,amt,b = re.match(r"(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+)\.",line).groups()
    w = (-1)*int(amt) if sgn == "lose" else int(amt)
    people.add(a)
    people.add(b)
    prefs[(a,b)] = w

def happiness():
    for perm in it.permutations(people):
        hap = 0
        for a,b in [(a,b) for a,b in zip(perm, (perm[1:]+perm))]:
            hap += prefs[(a,b)] + prefs[(b,a)]
        yield hap

print("Part 1:", max(happiness()))

for p in people:
    prefs[("Joni",p)] = 0
    prefs[(p,"Joni")] = 0
people.add("Joni")

print("Part 2:", max(happiness()))
