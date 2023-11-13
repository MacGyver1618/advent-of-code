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

examples,program = re.split(r"(?<=\n)\n\n\n",full_input(16))
examples=re.split(r"(?<=\n)\n",examples)
program=program.split("\n")[:-1]

instruction_examples=defaultdict(list)

for example in examples:
    before,instruction,after=example.rstrip().split("\n")
    regs_before=[int(t) for t in re.findall(r"\d+(?=[,\]])", before)]
    op,a,b,c=map(int,instruction.split())
    regs_after=[int(t) for t in re.findall(r"\d+(?=[,\]])", after)]
    instruction_examples[op]+=[(op,a,b,c,regs_before,regs_after)]

def addr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]+new_regs[b]
    return new_regs

def addi(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]+b
    return new_regs

def mulr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]*new_regs[b]
    return new_regs

def muli(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]*b
    return new_regs

def banr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]&new_regs[b]
    return new_regs

def bani(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]&b
    return new_regs

def borr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]|new_regs[b]
    return new_regs

def bori(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]|b
    return new_regs

def setr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]
    return new_regs

def seti(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=a
    return new_regs

def gtir(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=int(a>new_regs[b])
    return new_regs

def gtri(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=int(new_regs[a]>b)
    return new_regs

def gtrr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=int(new_regs[a]>new_regs[b])
    return new_regs

def eqir(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=int(a==new_regs[b])
    return new_regs

def eqri(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=int(new_regs[a]==b)
    return new_regs

def eqrr(a,b,c,regs):
    new_regs=regs.copy()
    new_regs[c]=int(new_regs[a]==new_regs[b])
    return new_regs

candidates_by_opcode = defaultdict(list)
all_ops=[addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr]

for opcode,op_examples in instruction_examples.items():
    for op in all_ops:
        if all(op(a,b,c,regs_before)==regs_after for _,a,b,c,regs_before,regs_after in op_examples):
            candidates_by_opcode[opcode]+=[op]

multimatches=0
for example in [item for sublist in instruction_examples.values() for item in sublist]:
    op,a,b,c,before,after=example
    if sum(1 for op in all_ops if op(a,b,c,before)==after)>=3:
        multimatches+=1


while [v for v in candidates_by_opcode.values() if len(v)>1]:
    all_found=[]
    for k,v in candidates_by_opcode.items():
        if len(v)==1:
            found=v[0]
            all_found+=[found]
    for found in all_found:
        for v in candidates_by_opcode.values():
            if found in v and len(v)>1:
                v.remove(found)
ops={k:v[0] for k,v in candidates_by_opcode.items()}

part1 = multimatches
print("Part 1:", part1)

regs=[0,0,0,0]
for line in program:
    op,a,b,c=map(int,line.split())
    regs=ops[op](a,b,c,regs)
part2=regs[0]
print("Part 2:", part2)
