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

lines = read_lines(8)

nodes={}
instrs=lines[0]
for line in lines[2:]:
    n,l,r=re.findall(r"[A-Z]{3}",line)
    nodes[n]=(l,r)

def find_steps(start,end):
    cur=start
    steps=0
    i=0
    while cur!=end and steps < 100_000:
        instr=instrs[i]
        cur=nodes[cur]["LR".index(instr)]
        i+=1
        i%=len(instrs)
        steps+=1
    return steps

time,part1 = timed(lambda:find_steps("AAA","ZZZ"))
print(f"Part 1: {part1} {pretty_time(time)}")

def part2():
    steps=[]
    starts=[node for node in nodes if node[-1]=="A"]
    ends=[node for node in nodes if node[-1]=="Z"]
    for start in starts:
        for end in ends:
            cur_steps=find_steps(start,end)
            if cur_steps!=100_000:
                steps+=[cur_steps]
    return math.lcm(*steps)

time,part2=timed(part2)
print(f"Part 2: {part2} {pretty_time(time)}")
