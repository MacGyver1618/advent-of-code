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

program = read_lines(18)
pc=0
regs=defaultdict(int)
history=[]
while pc < len(program):
    op,*args=program[pc].split()
    if op=="snd":
        x,=args
        x = regs[x] if x.isalpha() else int(x)
        history+=[x]
    elif op=="set":
        x,y=args
        regs[x]=regs[y] if y.isalpha() else int(y)
    elif op=="add":
        x,y=args
        y = regs[y] if y.isalpha() else int(y)
        regs[x]+=y
    elif op=="mul":
        x,y=args
        y = regs[y] if y.isalpha() else int(y)
        regs[x]*=y
    elif op=="mod":
        x,y=args
        y = regs[y] if y.isalpha() else int(y)
        regs[x]%=y
    elif op=="rcv":
        x,=args
        x = regs[x] if x.isalpha() else int(x)
        if x != 0:
            part1=history[-1]
            break
    elif op=="jgz":
        x,y=args
        x = regs[x] if x.isalpha() else int(x)
        y = regs[y] if y.isalpha() else int(y)
        pc += y if x > 0 else 1
    if op != "jgz":
        pc += 1

# print("Part 1:", part1)

def run(pc, regs, send_queue, receive_queue):
    while pc < len(program):
        op,*args=program[pc].split()
        if op=="snd":
            x,=args
            x = regs[x] if x.isalpha() else int(x)
            send_queue.append(x)
            regs["send_count"]+=1
        elif op=="set":
            x,y=args
            regs[x]=regs[y] if y.isalpha() else int(y)
        elif op=="add":
            x,y=args
            y = regs[y] if y.isalpha() else int(y)
            regs[x]+=y
        elif op=="mul":
            x,y=args
            y = regs[y] if y.isalpha() else int(y)
            regs[x]*=y
        elif op=="mod":
            x,y=args
            y = regs[y] if y.isalpha() else int(y)
            regs[x]%=y
        elif op=="rcv":
            x,=args
            if receive_queue:
                regs[x]=receive_queue.popleft()
            else:
                return pc,regs,send_queue, receive_queue
        elif op=="jgz":
            x,y=args
            x = regs[x] if x.isalpha() else int(x)
            y = regs[y] if y.isalpha() else int(y)
            pc += y if x > 0 else 1
        if op != "jgz":
            pc += 1

    return pc, regs, send_queue, receive_queue

PC,REGS,SEND,RECEIVE=0,1,2,3
def is_waiting(machine):
    pc, _, send, receive=machine
    return program[pc].split()[0] == "rcv" and not receive and not send

regs_1 = defaultdict(int)
regs_2 = defaultdict(int)
regs_1["p"]=0
regs_2["p"]=1
send_1=deque()
send_2=deque()
machine_1 = run(0, regs_1, send_1, send_2)
machine_2 = run(0, regs_2, send_2, send_1)
while not is_waiting(machine_1) or not is_waiting(machine_2):
    machine_1 = run(*machine_1)
    machine_2 = run(*machine_2)

part2 = machine_2[REGS]["send_count"]

print("Part 2:", part2)
