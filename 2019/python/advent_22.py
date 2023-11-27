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

lines = read_lines(22)
deck=deque(range(10007))
for line in lines:
    if line=="deal into new stack":
        deck.reverse()
    elif line.startswith("cut"):
        deck.rotate(-int(line.split()[-1]))
    elif line.startswith("deal with increment"):
        L=len(deck)
        skip=int(line.split()[-1])
        new_deck=deck.copy()
        i=0
        while deck:
            new_deck[i]=deck.popleft()
            i+=skip
            i%=L
        deck=new_deck


part1 = [i for i,c in enumerate(deck) if c==2019][0]
print("Part 1:", part1)

CARDS=119315717514047
SHUFFLES=101741582076661

skip=1
start=0
for line in lines[::-1]:
    if line.startswith("deal into"):
        skip = (-skip)%CARDS
        start=(CARDS-start-1)%CARDS
    elif line.startswith("deal with"):
        increment=int(line.split()[-1])
        skip = (skip*sym.mod_inverse(increment,CARDS))%CARDS
        start = (start*sym.mod_inverse(increment,CARDS))%CARDS
    elif line.startswith("cut"):
        amount=int(line.split()[-1])
        start=(start+amount)%CARDS

start *= (pow(skip, SHUFFLES, CARDS) - 1) * sym.mod_inverse(skip - 1, CARDS)
skip = pow(skip,SHUFFLES,CARDS)
part2 = (2020*skip+start)%CARDS
print("Part 2:", part2)
