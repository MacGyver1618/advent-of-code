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

lines = read_lines(21)

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

def setr(a,_,c,regs):
    new_regs=regs.copy()
    new_regs[c]=new_regs[a]
    return new_regs

def seti(a,_,c,regs):
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

program_table = {f.__name__:f for f in [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]}
def pretty_regs(regs):
    expanded_regs=[f"{reg:8d}" for reg in regs]
    return f"[{', '.join(expanded_regs)}]"

def pretty_op(instr):
    op,*args=instr.split()
    a,b,c=map(int,args)
    return f"{op} {a:8d} {b:8d} {c:8d}"

def evaluate(program, regs, ip):
    op,*args=program[regs[ip]].split()
    a,b,c=map(int,args)
    return program_table[op](a,b,c,regs)

def run_program(program, regs,ip,final_instruction=None):
    final_instruction=final_instruction or len(program)
    while regs[ip] < final_instruction:
        new_regs=evaluate(program, regs, ip)
        new_regs[ip]+=1
        regs=new_regs
    return regs[-1]

# The program evaluates until instruction 28 "eqrr 5 0 1"
# which is the only place register 0 is accessed. If the comparison succeeds,
# the program exits. Therefore, the only place the program can exit is at line 28
# and the earliest time it can exit is when the program first reaches instruction #28.
# Thus, at this point, register 5 contains the correct answer.

program=lines[1:]
ip = int(lines[0].split()[-1])
part1 = run_program(lines[1:], [0] * 6, ip, final_instruction=28)
print("Part 1:", part1)

N = int(lines[8].split()[1])
p = int(lines[12].split()[2])

# The code, when reverse engineered, is this:

def generate(N, p):
    b = 2**16
    n=N
    while True:
        n += b % 256
        n %= 2**24
        n *= p
        n %= 2**24
        if b < 256:
            yield n
            b = n | 2**16
            n=N
        else:
            b //= 256

gen = generate(N, p)
seen = []
while True:
    n = next(gen)
    if n in seen:
        break
    seen += [n]

part2=seen[-1]
print("Part 2:", part2)
