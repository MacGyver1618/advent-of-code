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
import math

lines = read_lines(14)

edges=set()
recipes={}
for line in lines:
    reagents,prod=line.split(" => ")
    prod_amt,prod_type=prod.split()
    reagents=[(b,int(a)) for a,b in [reagent.split() for reagent in reagents.split(", ")]]
    recipes[prod_type]=(int(prod_amt),reagents)
    for reagent,_ in reagents:
        edges.add((reagent,prod_type))

ore_cost=0
Q=deque([("FUEL",1)])
while Q:
    cur,amt=Q.popleft()
    if cur=="ORE":
        ore_cost+=amt
    else:
        _yield,reagents = recipes[cur]
        times=math.ceil(amt/_yield)
        for reagent,demand in reagents:
            Q.append((reagent,times*demand))
            # TODO handle amount update


def calculate_demand(_type, amount, surplus):
    if _type == "ORE":
        return amount
    elif amount <= surplus[_type]:
        surplus[_type] -= amount
        return 0
    else:
        amount -= surplus[_type]
        surplus[_type] = 0
        _yield,reagents = recipes[_type]
        times = math.ceil(amount/_yield)
        demand = sum(calculate_demand(reagent, amt*times, surplus) for reagent,amt in reagents)
        remaining = _yield*times-amount
        surplus[_type] += remaining
        return demand

part1 = calculate_demand("FUEL",1, defaultdict(int))
print("Part 1:", part1)

def demand_for(amount):
    return calculate_demand("FUEL",amount,defaultdict(int))

fuelmin=1
fuelmax=part1
demand=demand_for(fuelmax)
while demand < 1e12:
    fuelmin=fuelmax
    fuelmax*=2
    demand=demand_for(fuelmax)
while fuelmin < fuelmax-1:
    midpoint=(fuelmin+fuelmax)//2
    demand=demand_for(midpoint)
    if demand > 1e12:
        fuelmax=midpoint
    elif demand < 1e12:
        fuelmin=midpoint

part2=fuelmin
print("Part 2:", part2)
