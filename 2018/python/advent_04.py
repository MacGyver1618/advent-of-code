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
import datetime

lines = read_lines(4)
events=[]
for line in lines:
    ts,event=re.match(r"\[([0-9 :-]+)\] ([\w #]+)",line).groups()
    ts=datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M")
    events+=[(ts,event)]

events=sorted(events,key=first)
guards=defaultdict(lambda:defaultdict(int))
for ts,event in events:
    if "Guard" in event:
        guard=int(re.findall(r"\d+",event)[0])
    elif "asleep" in event:
        nap_started=ts
    elif "wakes" in event:
        cur=nap_started
        nap_ended=ts
        while cur < nap_ended:
            guards[guard][cur.minute]+=1
            cur = cur+datetime.timedelta(minutes=1)

sleepiest=max(guards.items(),key=lambda g: sum(g[1].values()))

guard_no=sleepiest[0]
minute=max(sleepiest[1].items(),key=second)[0]
part1 = guard_no*minute
print("Part 1:", part1)

sleepiest=max(guards.items(),key=lambda g: max(g[1].values()))
guard_no=sleepiest[0]
minute=max(sleepiest[1].items(),key=second)[0]
part2 = guard_no*minute

print("Part 2:", part2)
