import collections

from common.advent_lib import *
import re
import more_itertools as it2
import functools as ft
import json

inpt = read_lines(22)[2:]

# x y size used avail use%

nodes = set()
coords = set()
capacities = {}

lr = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
for line in inpt:
    node = tuple(map(int, re.match(lr, line).groups()))
    nodes.add(node)
    capacities[node[:2]] = node[2:]

def viable_pairs(ns):
    result = set()
    for a, (_, need, _, used) in ns.items():
        for b, (_, _, avail, _) in ns.items():
            if used > 0 and a != b and avail >= need:
                result.add((a,b))
    return result

def possible_moves(ns):
    result = [pair for pair in viable_pairs(ns) if manhattan_distance(*map(ft.partial(it2.take,2), pair)) == 1]
    return result

data_location = (max(map(second, nodes)), 0)

print("Part 1:", len(viable_pairs(capacities)))

state = (data_location, frozenset(map(tuple, capacities.items())))

def neighbors(s):
    p, caps = s
    for m in possible_moves(dict(caps)):
        caps = dict(caps)
        a, b = m
        if a == p:
            p = b
        a_size, a_used, a_avail, a_pct = caps[a]
        b_size, b_used, b_avail, b_pct = caps[b]
        caps[a] = (a_size, 0, a_size, 0)
        caps[b] = (b_size, a_used + b_used, b_size - a_used - b_used, 100*(a_used + b_used) // b_size)
        yield p, frozenset(map(tuple, caps.items()))

def heur_fn(s):
    a, caps = s
    max_free = 0
    t = 0,0
    for item in caps:
        print(item)
        input()
        b,(_,_,avail,_) = item
        if avail > max_free:
            t = b
    return manhattan_distance(a, (0,0)) + manhattan_distance(a,t)

path = a_star(state, lambda s: s[0] == (0,0), neighbors, lambda x,y: 1, heur_fn)
part2 = len(path)

print("Part 2:", part2)
