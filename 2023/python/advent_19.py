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

workflows, parts = full_input(19)[:-1].split("\n\n")

graph={}

for workflow in workflows.split("\n"):
    name,rest=workflow.split("{")
    rules=[]
    for rule in rest[:-1].split(","):
        if ":" in rule:
            pred,target=rule.split(":")
            rules+=[(pred,target)]
        else:
            rules+=[('True', rule)]
    graph[name]=rules

part1 = 0

for part in parts.split("\n"):
    x,m,a,s=map(int,re.findall(r"\d+",part))
    p={"x":x,"m":m,"a":a,"s":s}
    wf="in"
    while wf not in "AR":
        rs=graph[wf]
        for r in rs:
            pred=r[0]
            if pred=="True" or eval(f"p['{pred[0]}']{pred[1:]}"):
                wf=r[1]
                break
    if wf == "A":
        part1+=x+m+a+s

print("Part 1:", part1)

paths=[]
n="in"
tot=0
stack=deque()
stack.append(("in",deque([("in","True")]))) # node, came_from
while stack:
    cur,history=stack.pop()
    if cur=="A":
        paths.append(history)
        continue
    for n in graph[cur]:
        pred,name=n
        if name != "R":
            h2=history.copy()
            h2+=[(name,pred)]
            stack.append((n[1],h2))

def constrain(pred,allowed):
    if pred=="True":
        return allowed
    key=pred[0]
    sym=pred[1]
    val=int(pred[2:])
    lo,hi=allowed[key]
    if sym==">":
        lo=max(lo,val+1)
        allowed[key][0]=lo
    elif sym=="<":
        hi=min(hi,val)
        allowed[key][1]=hi
    return allowed

def invert(preds,allowed):
    for pred,_ in preds:
        key=pred[0]
        sym=pred[1]
        val=int(pred[2:])
        lo,hi=allowed[key]
        if sym==">":
            hi=min(hi,val+1)
            allowed[key][1]=hi
        elif sym=="<":
            lo=max(lo,val)
            allowed[key][0]=lo
    return allowed

tot=0
for path in paths:
    allowed={"x":[1,4001],"m":[1,4001],"a":[1,4001],"s":[1,4001]}
    for i in range(1,len(path)):
        n1,_=path[i-1]
        n2,p=path[i]
        precursor_chain=[p[0] for p in graph[n1]]
        pos=precursor_chain.index(p)
        invert(graph[n1][:pos],allowed)
        constrain(p,allowed)
    vol=1
    for dim in "xmas":
        start,end=allowed[dim]
        vol*=end-start
    tot+=vol

part2=tot
print("Part 2:", part2)
