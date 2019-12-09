from advent_lib import *
import itertools as iter

input = [line.split(",") for line in lines(3)]
wires = []

dirs = {
    'U': ( 0, 1),
    'D': ( 0,-1),
    'R': ( 1, 0),
    'L': (-1, 0)
    }

def next_point(point, inst):
    dir = inst[0]
    amt = int(inst[1:])
    diff = tuple(map(lambda x: x*amt, dirs[dir]))
    return tuple([sum(x) for x in zip(point, diff)])

for wire in input:
    segments = []
    p1 = (0,0)
    for inst in wire:
        p2 = next_point(p1, inst)
        segments.append((p1, p2))
        p1 = p2
    wires.append(segments)

def is_vertical(line):
    (p1, p2) = line
    (x1, y1) = p1
    (x2, y2) = p2
    return x1 == x2

def is_horizontal(line):
    (p1, p2) = line
    (x1, y1) = p1
    (x2, y2) = p2
    return y1 == y2

def in_bounds(num, range):
    (min, max) = range
    return num > min and num < max

def intersect(horiz, vert):
    ((a1, y), (a2, _)) = horiz
    ((x, b1), (_, b2)) = vert
    if in_bounds(x, (a1,a2)) and in_bounds(y, (b1, b2)):
        return (x,y)
    else:
        return None

def intersection_of(pair):
    (w1, w2) = pair
    if is_horizontal(w1) and is_horizontal(w2):
        return None
    if is_vertical(w1) and is_vertical(w2):
        return None
    if is_horizontal(w1) and is_vertical(w2):
        return intersect(w1, w2)
    if is_vertical(w1) and is_horizontal(w2):
        return intersect(w2, w1)

intersections = []

for pair in iter.product(wires[0], wires[1]):
    intersection = intersection_of(pair)
    if intersection is not None:
        intersections.append(intersection)

def dist(point):
    return sum(map(abs, point))

print(list(map(dist, intersections)))
