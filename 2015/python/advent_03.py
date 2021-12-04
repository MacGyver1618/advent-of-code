from common.advent_lib import *
from numpy import array as A

inpt = lines(3)[0]

p = A([0,0])
presents = {}

presents[tuple(p)] = 1

for c in inpt:
    if c == '^':
        p += A([0,1])
    elif c == 'v':
        p -= (0,1)
    elif c == '>':
        p += (1,0)
    elif c == '<':
        p -= (1,0)
    presents[tuple(p)] = presents.get(tuple(p), 0) + 1

print("Part 1:", len(presents))

p1 = A([0,0])
p2 = A([0,0])
presents = {}

presents[tuple(p1)] = 2

for i,c in enumerate(inpt):
    if i % 2 == 0:
        if c == '^':
            p1 += (0,1)
        elif c == 'v':
            p1 -= (0,1)
        elif c == '>':
            p1 += (1,0)
        elif c == '<':
            p1 -= (1,0)
        presents[tuple(p1)] = presents.get(tuple(p1), 0) + 1
    else:
        if c == '^':
            p2 += (0,1)
        elif c == 'v':
            p2 -= (0,1)
        elif c == '>':
            p2 += (1,0)
        elif c == '<':
            p2 -= (1,0)
        presents[tuple(p2)] = presents.get(tuple(p2), 0) + 1
print("Part 2:", len(presents))
