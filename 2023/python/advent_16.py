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

lines = read_lines(16)
R=len(lines)
C=len(lines[0])
rs=[*range(R)]
cs=[*range(C)]

beams=[(0,1)]
energized= {0}

def char_at(pos):
    c,r=map(int,[pos.real,pos.imag])
    return lines[r][c]

def in_bounds(pos):
    c,r=map(int,[pos.real,pos.imag])
    return 0<=r<R and 0<=c<C

def neighbors(beam):
    pos, _dir = beam
    char = char_at(pos)
    added=[]
    match char:
        case "|":
            if _dir.real == 0:
                added +=[(pos+_dir, _dir)]
            else:
                added +=[(pos+1j, 1j)]
                added +=[(pos-1j, -1j)]
        case "-":
            if _dir.imag == 0:
                added +=[(pos+_dir, _dir)]
            else:
                added +=[(pos+1, 1)]
                added +=[(pos-1, -1)]
        case "/":
            _dir = -complex(_dir.imag, _dir.real)
            added +=[(pos+_dir, _dir)]
        case "\\":
            _dir = complex(_dir.imag, _dir.real)
            added +=[(pos+_dir, _dir)]
        case ".":
            added +=[(pos+_dir, _dir)]
    return [n for n in added if in_bounds(n[0])]

visited=bfs((0,1),lambda _:False,neighbors)

part1 = len({n[0] for n in visited})
print("Part 1:", part1)

starts=[]
starts+=[(c,1j) for c in cs]
starts+=[(c+(R-1)*1j,-1j) for c in cs]
starts+=[(r*1j,1) for r in rs]
starts+=[(r*1j+(C-1),-1) for r in rs]
part2=0
for start in starts:
    visited=bfs(start,lambda _:False,neighbors)
    uniq=len({n[0] for n in visited})
    part2=max(part2,uniq)
print("Part 2:", part2)


# printed=False
# def print_grid(beam):
#     global printed
#     sys.stdout.write("\033[0;0H\033[34m")
#     if not printed:
#         printed=True
#         for r in range(min(R,25)):
#             sys.stdout.write(lines[r].replace("."," ")+"\n")
#
#     pos,_dir=beam
#     r,c=map(int,[pos.imag,pos.real])
#     if r<25:
#         if char_at(pos) != ".":
#             sys.stdout.write(f"\033[{r+1};{c+1}H\033[93m{char_at(pos)}\033[34m")
#         else:
#             sys.stdout.write(f"\033[{r+1};{c+1}H\033[93m{'↑↓←→'[[-1j, 1j, -1, 1].index(_dir)]}\033[34m")
#         sys.stdout.flush()
#
# print("\033[?12l")
# print("\033[0;0H"," "*130,sep="")
