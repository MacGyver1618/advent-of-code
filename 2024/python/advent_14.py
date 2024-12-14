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

lines = read_lines(14)
R = 103
C = 101

visual=True

robots=[]
for line in lines:
    robots+=[parse_ints(line)]

inited=False
last_written=[]
def print_grid():
    global inited, last_written
    if not inited:
        sys.stdout.write("\033[2J\033[H\033[90m")
        for k in range(R):
            sys.stdout.write(f"\033[{k}H")
            sys.stdout.write("."*C)
        sys.stdout.write("\033[39m")
        inited=True
    sys.stdout.write("\033[90m")
    for r,c in last_written:
        sys.stdout.write(f"\033[{r};{c}H.")
    sys.stdout.write("\033[93m")
    last_written=[]
    for c,r,*_ in robots:
        sys.stdout.write(f"\033[{r};{c}H*")
        last_written.append((r,c))
    sys.stdout.write("\033[39m")
    sys.stdout.flush()
    time.sleep(0.001)

part2=0
part1=1
for _ in range(8159):
    if part2==100:
        part1*=sum(1 for (px,py,vx,vy) in robots if px<50 and py<51)
        part1*=sum(1 for (px,py,vx,vy) in robots if px>50 and py<51)
        part1*=sum(1 for (px,py,vx,vy) in robots if px<50 and py>51)
        part1*=sum(1 for (px,py,vx,vy) in robots if px>50 and py>51)
    for i,robot in enumerate(robots):
        px,py,vx,vy=robot
        robots[i]=((px+vx)%C,(py+vy)%R,vx,vy)
    if visual:
        print_grid()
    part2+=1
if not visual:
    print_grid()
sys.stdout.write(f"\033[{R}H")
print("Part 1:", part1)
print("Part 2:", part2)
