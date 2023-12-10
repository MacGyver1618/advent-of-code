import time

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

lines = read_lines(10)

start=-1
neighbors=defaultdict(list)
dirs={
    "S":[1,1j],
    "-":[1,-1],
    "|":[1j,-1j],
    "F":[1,1j],
    "J":[-1,-1j],
    "L":[1,-1j],
    "7":[-1,1j],
}

def parse():
    global start
    for r,line in enumerate(lines):
        for c,char in enumerate(line):
            p=c+1j*r
            if char=="S":
                start=p
            if char in dirs:
                neighbors[p]+=[p+d for d in dirs[char]]

R=len(lines)
C=len(lines[0])
s,_=timed(parse)
print(f"Parse took {pretty_time(s)}")

s,loop=timed(lambda:dfs(start,lambda _: False, lambda p: neighbors[p]))
part1=len(loop)//2
print(f"Part 1: {part1} ({pretty_time(s)})")

def in_bounds(p):
    return 0<=p.real<C and 0<=p.imag<R

def char_at(p):
    if in_bounds(p):
        return lines[int(p.imag)][int(p.real)]
    return " "

history=[]
outside=set()
def part2():
    global history,outside
    high_row=int(min(p.imag for p in loop))
    left_col=int(min(p.real for p in loop if p.imag==high_row))

    start=left_col+1j*high_row
    pos=start
    _dir=-1j
    history+=[(pos,_dir)]
    while True:
        on_left = pos + _dir * -1j
        if in_bounds(on_left) and on_left not in loop:
            outside.add(on_left)
        char=char_at(pos)
        if char in "7LFJS":
            _dir=complex(_dir.imag,_dir.real)
            if char in "FJS":
                _dir*=-1
            history+=[(pos,_dir)]
            on_left = pos + _dir * -1j
            if in_bounds(on_left) and on_left not in loop:
                outside.add(on_left)
        _next=pos+_dir
        history+=[(pos,_dir)]
        if _next==start:
            break
        pos=_next


    def neighbor_fn(p):
        for d in 1,-1,1j,-1j:
            n=p+d
            if in_bounds(n) and n not in loop and n not in outside:
                yield n

    Q=deque(outside)
    while Q:
        cell=Q.popleft()
        flooded=bfs(cell, lambda _:False, neighbor_fn)
        outside.update(flooded)

    return R*C-len(outside)-len(loop)

exectime,result=timed(part2)
print(f"Part 2: {result} ({pretty_time(exectime)})")


printed=False
color="default"
oldp,oldd=None,None
sys.stdout.write('\033[?12l')
sys.stdout.flush()

def draw_char(p,d,r,c):
    global color
    char=char_at(c+1j*r)
    o=""
    pos=c+1j*r
    if pos==p:
        o+=f"\033[93m{'↑↓←→'[[-1j,1j,-1,1].index(d)]}\033[34m"
        color="default"
    elif pos in outside or not in_bounds(pos):
        if color != "red":
            o+="\033[31m"
            color="red"
        o+="O"
    elif pos not in loop:
        if color != "green":
            o+="\033[32m"
            color="green"
        o+="I"
    else:
        if color != "default":
            o+="\033[34m"
            color="default"
        o+="─│┌┐└┘┌"["-|F7LJS".index(char)]
    return o
Rmin,Rmax,Cmin,Cmax=0,25,0,80

def close_to_border(p):
    return not (Rmin+3<=p.imag<=Rmax-3 and Cmin+3<=p.real<=Cmax-3)

def print_grid(p,_dir):
    global printed,oldp,oldd,Rmin,Rmax,Cmin,Cmax
    if not printed:
        oldp,oldd=p,_dir
        printed=True
        os=[]
        for r in range(Rmin,Rmax+1):
            o=""
            for c in range(Cmin,Cmax+1):
               o+=draw_char(p,d,r,c)
            os+=[o]
        sys.stdout.write("\n".join(os))
        sys.stdout.flush()
    elif close_to_border(p):
        oldp+=oldd
        match oldd:
            case 1: Cmin+=1; Cmax+=1
            case -1: Cmin-=1; Cmax-=1
            case 1j: Rmin+=1; Rmax+=1
            case -1j: Rmin-=1; Rmax-=1
        os=[]
        sys.stdout.write("\033[0;0H")
        for r in range(Rmin,Rmax+1):
            o=""
            for c in range(Cmin,Cmax+1):
                o+=draw_char(p,d,r,c)
            os+=[o]
        sys.stdout.write("\n".join(os))
    else:
        r,c=int(oldp.imag),int(oldp.real)
        print(f"\033[{r-Rmin+1};{c-Cmin+1}H{draw_char(p,_dir,r,c)}", end="", flush=True)
        r,c=int(p.imag),int(p.real)
        print(f"\033[{r-Rmin+1};{c-Cmin+1}H{draw_char(p,_dir,r,c)}", end="", flush=True)
        sys.stdout.write("\033[0;0H")
        oldp,oldd=p,_dir


visual=False
if visual:
    for p,d in history:
        print_grid(p,d)
        time.sleep(1/60)