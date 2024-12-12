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
import time

lines = read_lines(12)
grid=Grid(lines)
raw=grid.raw_grid
R = len(lines)
C = len(lines[0])

populated=set()
areas=set()
tot=0
#colors=deque([91,92,93,94,95,96,31,32,33,34,35,36])
#sys.stdout.write("\033[3J\033[?25h\033[90m\033[H")
#sys.stdout.write("\n".join("."*C+str(r) for r in range(R)))
#sys.stdout.flush()
for r in range(R):
    for c in range(C):
        if (r,c) not in populated:
            #colors.rotate(1)
            #sys.stdout.write(f"\033[{colors[0]}m")
            area=set()
            perimeter=0
            start=(r,c)
            Q=deque([start])
            area.add(start)
            while Q:
                cur=Q.popleft()
                r1,c1=cur
                v1=raw[r1][c1]
                #sys.stdout.write(f"\033[{r1+1};{c1+1}H{v1}")
                #sys.stdout.flush()
                #time.sleep(0.001)
                for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                    r2,c2=r1+dr,c1+dc
                    n=(r2,c2)
                    if n in area:
                        continue
                    if 0<=r2<R and 0<=c2<C:
                        v2=raw[r2][c2]
                        if v2==v1:
                            area.add(n)
                            Q.append(n)
                        else:
                            perimeter+=1
                    else:
                        perimeter+=1
            surface_area=len(area)
            tot+=surface_area*perimeter
            populated.update(area)
            areas.add(frozenset(area))

#sys.stdout.write(f"\033[{R+1};1H\033[?25h\033[39m")
#sys.stdout.flush()

part1 = tot
print("Part 1:", part1)

part2=0
for area in areas:
    sides=0
    for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:#L,D,R,U
        visited=set()
        oriented_edges=[(r,c) for (r,c) in sorted(area) if (r+dr,c+dc) not in area]
        for node in oriented_edges:
            r,c=node
            if node in visited:
                continue
            sides+=1
            nr,nc=abs(dc),abs(dr)
            while node in oriented_edges:
                visited.add(node)
                rr,cc=node
                node=rr+nr,cc+nc
    part2+=len(area)*sides

print("Part 2:", part2)
