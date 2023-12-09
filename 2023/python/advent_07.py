import timeit

from common.advent_lib import *
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym

lines = read_lines(7)
cards=["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
hands=[[5],[4,1],[3,2],[3,1,1],[2,2,1],[2,1,1,1],[1,1,1,1,1]]

plays=[]
for line in lines:
    hand,bid=line.split()
    counter=Counter(hand)
    counts=sorted(counter.values(),reverse=True)
    plays+=[(hand,int(bid),counts)]

def key_fn(play):
    hand,bid,counts=play
    keys=map(cards.index,hand)
    return hands.index(counts), *keys

ranked=sorted(plays,key=key_fn,reverse=True)

part1 = sum(i*bid for i,(hand,bid,counts) in enumerate(ranked,start=1))
print("Part 1:", part1)

cards2=["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

def key_fn2(play):
    hand,*_=play
    jokers=hand.count("J")
    counts=sorted(Counter(hand.replace("J","")).values(),reverse=True)
    if counts:
        counts[0]+=jokers
    else:
        counts=[5]
    keys=map(cards2.index,hand)
    return hands.index(counts), *keys

ranked2=sorted(plays,key=key_fn2,reverse=True)

part2=sum(i*bid for i,(hand,bid,counts) in enumerate(ranked2,start=1))
print("Part 2:", part2)
