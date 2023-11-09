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

lines = read_lines(25)
program=[]
for line in lines:
    program+=[line.split()]

def evaluate(instr):
    global pc, out
    op,*args=instr
    if op == "cpy":
        x,y=args
        regs[y]=regs[x] if x in regs else int(x)
        pc+=1
    elif op =="inc":
        x,=args
        regs[x]+=1
        pc += 1
    elif op == "dec":
        x,=args
        regs[x]-=1
        pc += 1
    elif op == "jnz":
        x,y=args
        x=regs[x] if x in regs else int(x)
        y=regs[y] if y in regs else int(y)
        pc += y if x else 1
    elif op == "out":
        x,=args
        out+=[regs[x] if x in regs else int(x)]
        pc +=1

num=0
while True:
    print(num)
    pc=0
    regs={"a":num,"b":0,"c":0,"d":0}
    seen=set()
    out = []
    while pc < len(program):
        state=tuple([pc,*regs.values()])
        if state in seen:
            break
        else:
            seen.add(state)
        evaluate(program[pc])
    print(out)
    print([0,1]*(len(out)//2))
    input()
    if out == [0,1]*(len(out)//2):
        break
    num += 1

print("Part 1:", num)
print("Part 2:", "All Done!")
