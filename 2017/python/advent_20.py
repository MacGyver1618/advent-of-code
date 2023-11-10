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

lines = read_lines(20)

def scan():
    particles=[]

    for line in lines:
        px,py,pz,vx,vy,vz,ax,ay,az=map(int,re.findall(r"-?\d+",line))
        p=A((px,py,pz))
        v=A((vx,vy,vz))
        a=A((ax,ay,az))
        particles+=[(p,v,a)]
    return particles

particles = scan()

for _ in range(1_000):
    for p,v,a in particles:
        v+=a
        p+=v

part1 = min(enumerate(particles),key=lambda p: manhattan_distance([0,0,0], p[1][0]))[0]
print("Part 1:", part1)

particles=scan()

for i in range(1_000):
    for p,v,a in particles:
        v+=a
        p+=v
    by_pos = Counter([tuple(p[0]) for p in particles])
    collisions = [pair[0] for pair in by_pos.most_common() if pair[1] > 1]
    collided = [tuple(map(tuple,particle)) for particle in particles if tuple(particle[0]) in collisions]
    particles = [particle for particle in particles if tuple(map(tuple,particle)) not in collided]


part2 = len(particles)
print("Part 2:", part2)
