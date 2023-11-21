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

lines = read_lines(19)

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
IP=int(lines[0].split()[-1])
regs=[0]*6

def evaluate(program, regs):
    op,*args=program[regs[IP]].split()
    a,b,c=map(int,args)
    return program_table[op](a,b,c,regs)

while regs[IP]<len(lines):
    new_regs=evaluate(lines[1:],regs)
    new_regs[IP]+=1
    regs=new_regs

part1 = regs[0]
print("Part 1:", part1)

regs=[0]*6
regs[0]=1

def pretty_regs(regs):
    expanded_regs=[f"{reg:8d}" for reg in regs]
    return f"[{', '.join(expanded_regs)}]"

def pretty_op(instr):
    op,*args=instr.split()
    a,b,c=map(int,args)
    return f"{op} {a:2d} {b:2d} {c:2d}"

breakpoints=["regs[5]==10551329"]
def run_program(program, regs,ip,breakpoints=[]):
    breakpoint_triggered=False
    while regs[ip]<len(program):
        print(f"ip={regs[ip]:2d} {pretty_regs(regs)} {pretty_op(program[regs[ip]])}")
        for bp in breakpoints:
            if eval(bp):
                breakpoint_triggered=True
        if breakpoint_triggered:
            _input=input("Command: ")
            while _input:
                if _input=="clear":
                    breakpoint_triggered=False
                else:
                    if _input.split()[0] not in program_table.keys():
                        _input=input(f"Not a valid command ({_input}):")
                    else:
                        op,*args=_input.split()
                        a,b,c=map(int,args)
                        regs = program_table[op](a,b,c,regs)

        new_regs=evaluate(program, regs)
        # input()
        new_regs[ip]+=1
        regs=new_regs

# The assembly code does an inefficient search of divisors of N
# if register 0 bit is set, N = 10551329, else N = 929
# The reverse engineered algorithm is as follows:
#
# N = 10551329 if $0 else 929
# sum_of_divisors = 0
# for i in range(1,N):
#   for j in range(1,N):
#       if i*j=N:
#           sum_of_divisors+=i
# $0 = sum_of_divisors

part2 = sum(sym.divisors(10551329))
print("Part 2:", part2)
