from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
from numpy import array as A

inpt = lines(16)
my_idx = inpt.index("your ticket:")

rules = {}
for line in inpt[0:my_idx-1]:
    k, vs = line.split(": ")
    rs = vs.split(" or ")
    x1,x2 = rs[0].split("-")
    y1,y2 = rs[1].split("-")
    rules[k] = (int(x1), int(x2), int(y1), int(y2))

my_ticket = [*map(int, inpt[my_idx+1].split(","))]
nearby_tickets = []
for line in inpt[inpt.index("nearby tickets:")+1:]:
    nearby_tickets.append([*map(int, line.split(","))])

all_ranges = []
for rule in rules.values():
    min1,max1,min2,max2 = rule
    all_ranges.append((min1,max1))
    all_ranges.append((min2,max2))

invalid = 0
valid_tickets = []
for ticket in nearby_tickets:
    ticket_valid = True
    for field in ticket:
        valid_range_found = False
        for r in all_ranges:
            if field in range(r[0],r[1]+1):
                valid_range_found = True
                break
        if not valid_range_found:
            ticket_valid = False
            invalid += field
    if ticket_valid:
        valid_tickets.append(ticket)

print("Part 1:", invalid)


def possible_fields(nums):
    for k, (min1, max1, min2, max2) in rules.items():
        in_r1 = map(lambda x: min1 <= x <= max1,nums)
        in_r2 = map(lambda x: min2 <= x <= max2,nums)
        if func.reduce(oper.and_, [x or y for x,y in zip(in_r1,in_r2)]):
            yield k

fs = A(valid_tickets)
deciphered_rules = {}
Q = coll.deque(range(len(rules)))

while Q:
    cand = Q.popleft()
    field_values = fs[:,cand]
    possibles = [field for field in possible_fields(field_values) if field not in deciphered_rules.keys()]
    if len(possibles) == 1:
        deciphered_rules[possibles[0]] = cand
    else:
        Q.append(cand)

part2 = np.prod([my_ticket[v] for k,v in deciphered_rules.items() if k.startswith("departure")])

print("Part 2:", part2)
