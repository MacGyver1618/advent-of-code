import sympy.ntheory

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

program = read_lines(23)
regs=defaultdict(int)
pc=0
muls=0
def evaluate():
    global pc,muls
    op,x,y=program[pc].split()
    y=regs[y] if y.isalpha() else int(y)
    if op=="set":
        regs[x]=y
    elif op=="sub":
        regs[x]-=y
    elif op=="mul":
        muls+=1
        regs[x]*=y
    elif op=="jnz":
        x=regs[x] if x.isalpha() else int(x)
        pc+=1 if x==0 else y
    if op!="jnz":
        pc += 1



while pc < len(program):
    evaluate()

part1 = muls
print("Part 1:", part1)

# The part 2 assembly translates to the following code:
# b=106700
# c=123700
# h=0
# while b <= c:
#     f=1
#     for d in range(2,b):
#         for e in range(2,b):
#             if d*e==b:
#                 f=0
#     if f==0:
#         h+=1
#     b+=17
# i.e. number of nonprimes in the range [106700..123700]
# with a step of 17

nonprimes=0
def get_const(line):
    return int(program[line].split()[-1])
lower_limit=get_const(0)*get_const(4)-get_const(5)
upper_limit=lower_limit-get_const(7)
step=get_const(30)
for n in range(lower_limit,upper_limit+1,-step):
    if not sympy.ntheory.isprime(n):
        nonprimes+=1

part2 = nonprimes
print("Part 2:", part2)
