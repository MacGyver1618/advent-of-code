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
import math

lines = read_lines(23)
program=[]
pc=0
regs={'a':0,'b':0,'c':0,'d':0}
for line in lines:
    program+=[line.split()]

def is_valid(instr):
    op,*args=instr
    if op=="cpy":
        return args[1] in "abcd"
    if op in ["inc","dec"]:
        return args[0] in "abcd"
    return True

def evaluate(instr):
    global pc
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
    elif op == "tgl":
        x,=args
        x=regs[x] if x in regs else int(x)
        target=pc+x
        if 0<=target<len(program):
            tog_op,*tog_args=program[target]
            if len(tog_args)==1:
                tog_op = "dec" if tog_op == "inc" else "inc"
            else:
                tog_op = "cpy" if tog_op == "jnz" else "jnz"
            toggled = [tog_op,*tog_args]
            if is_valid(toggled):
                program[target]=toggled
        pc+=1

regs["a"]=7
while pc < len(program):
    evaluate(program[pc])

print("Part 1:", regs["a"])

# The program assembunny code does three things:
# 1) Calculates factorial of "a"
# 2) Toggles instructions 2,4,6,8 away from the toggle i.e.
#    a) l25: inc c -> dec c
#    b) l23: inc d -> dec d
#    c) l21: jnz 70 d -> cpy 70 d (or whatever the constant in your input)
#    d) l19: jnz 1 c -> cpy 1 c
# 3) adds the product of the constants on lines 20 and 21
print("Part 2:", math.factorial(12)+int(program[19][1])*int(program[20][1]))
