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

nodes = set()
graph = defaultdict(list)
flows = defaultdict(int)

for line in lines:
    v, r, vs = re.match(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)", line).groups()
    r = int(r)
    nodes.add(v)
    flows[v] = r
    graph[v] = list(vs.split(", "))

start = ("AA", 30, frozenset(), 0)

useful_nodes = set(node for node in nodes if flows[node] > 0)
trimmed_graph = defaultdict(list)

def trim_neighbors(state):
    node, target, time, seen = state
    for neighbor in graph[node]:
        if neighbor not in seen:
            if flows[neighbor] == 0 or neighbor == target:
                yield neighbor, target, time+1, frozenset([neighbor, *seen])

for node in ["AA", *useful_nodes]:
    for other in useful_nodes - {node}:
        path = bfs((node, other,0,frozenset(node)), lambda s, target=other: s[0] == target, trim_neighbors)
        if isinstance(path, deque):
            trimmed_graph[node].append((other, len(path)-1))

shortest_paths = dict()

for node in ["AA", *useful_nodes]:
    for other in useful_nodes - {node}:
        path = dijkstra(node, eq(other), lambda u: map(first, trimmed_graph[u]), lambda u, v: [w for p,w in trimmed_graph[u] if p == v][0])
        path = list(path)
        l = 0
        cur = path[0]
        for n in path[1:]:
            l += [w for p,w in trimmed_graph[cur] if p == n][0]
            cur = n
        shortest_paths[(node, other)] = l
        shortest_paths[(other, node)] = l

sorted_nodes = sorted(useful_nodes)

def to_int(s):
    return sum(1 << sorted_nodes.index(node) for node in s)
def canonical(path, max_length):
    cur = "AA"
    length = 0
    flow = 0
    total_flow = 0
    for i,node in enumerate(path):
        segment_length = shortest_paths[(cur, node)]+1
        if length + segment_length >= max_length:
            total_flow += (max_length-length)*flow
            path = path[:i]
            return total_flow, to_int(path), path
        length += segment_length
        total_flow += flow*segment_length
        flow += flows[node]
        cur = node
    total_flow += (max_length-length)*flow
    return total_flow, to_int(path), path

perms = set(canonical(perm, 30) for perm in it.permutations(useful_nodes, 5))
print(f"Part 1: {max(first(perm) for perm in perms)}")
perms = set(canonical(perm, 26) for perm in it.permutations(useful_nodes, 6))
part2 = max(pa+pb for (pa,a_int,a),(pb,b_int,b) in it.combinations(perms, 2) if not a_int & b_int)
print(f"Part 2: {part2}")
