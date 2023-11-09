import collections
import functools as func
import itertools as it
import operator as op
import queue

from heapdict import heapdict
from numpy import array as A

def full_input(day):
    return str(open(f"../input/{day:02d}.txt").read())

def read_lines(day):
    return [line.rstrip() for line in open(f"../input/{day:02d}.txt").readlines()]

def to_nums(string_arr):
    return list(map(int, string_arr))

def intersection(iterable):
    return set(func.reduce(set.intersection, [set(i) for i in iterable]))

def union(iterable):
    return set(func.reduce(set.union, [set(i) for i in iterable]))

def powerset(iterable):
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))

def product(iterable):
    return func.reduce(lambda a,x: a*x, iterable)

def first(iterable):
    return list(iterable)[0]

def second(iterable):
    return list(iterable)[1]

directions = {
    "N": A([0, -1]),
    "E": A([1, 0]),
    "S": A([0, 1]),
    "W": A([-1, 0]),
    "U": A([0, -1]),
    "R": A([1, 0]),
    "D": A([0, 1]),
    "L": A([-1, 0])
}
O = A([0,0])
R_turn = A([[ 0,-1],
            [ 1, 0]])
L_turn = R_turn.T
U = directions["U"]
D = directions["D"]
L = directions["L"]
R = directions["R"]

abc = "abcdefghijklmnopqrstuvwxyz"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def inc(n):
    return n+1

def dec(n):
    return n-1

def manhattan_distance(a, b):
    return sum([abs(op.sub(*x)) for x in zip(a,b)])

def sgn(n):
    if n == 0:
        return 0
    return -1 if n < 0 else 1

def reconstruct_path(node, came_from):
    path = collections.deque([node])
    while node in came_from:
        node = came_from[node]
        path.appendleft(node)
    return path

def bfs(start, goal_fn, neighbor_fn):
    Q = collections.deque()
    seen = set()
    came_from = {}
    seen.add(start)
    Q.append(start)
    while Q:
        node = Q.popleft()
        if goal_fn(node):
            return reconstruct_path(node, came_from)
        for neighbor in neighbor_fn(node):
            if neighbor not in seen:
                came_from[neighbor] = node
                seen.add(neighbor)
                Q.append(neighbor)
    return seen

def dfs(start, goal_fn, neighbor_fn):
    Q = collections.deque()
    seen = set()
    came_from = {}
    seen.add(start)
    Q.append(start)
    while Q:
        node = Q.pop()
        if goal_fn(node):
            return reconstruct_path(node, came_from)
        for neighbor in neighbor_fn(node):
            if neighbor not in seen:
                came_from[neighbor] = node
                seen.add(neighbor)
                Q.append(neighbor)

def dijkstra(start, goal_fn, neighbor_fn, dist_fn):
    dist = collections.defaultdict(lambda: float("inf"))
    dist[start] = 0
    Q = heapdict()
    Q[start] = 0
    prev = {}

    while Q:
        u,_ = Q.popitem()
        if goal_fn(u):
            return reconstruct_path(u, prev)
        for v in neighbor_fn(u):
            alt = dist[u] + dist_fn(u,v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                Q[v] = alt
    return dist, prev

def a_star(start, goal_fn, neighbor_fn, dist_fn, heur_fn):
    open_set = queue.PriorityQueue()
    open_set.put((heur_fn(start), start))
    came_from = {}
    g_score = collections.defaultdict(lambda: float("inf"))
    g_score[start] = 0

    while not open_set.empty():
        current = open_set.get()[1] # Priority queues return (prio, elem) tuples
        if goal_fn(current):
            return reconstruct_path(current, came_from)

        for neighbor in neighbor_fn(current):
            tentative_gscore = g_score[current] + dist_fn(current, neighbor)
            if tentative_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score = tentative_gscore + heur_fn(neighbor)
                open_set.put((f_score, neighbor))

    raise Exception

def adjacent(p):
    return [p+d for d in [U,D,L,R]]

def adjacent_diag(p):
    return [p+d for d in [U,D,L,R,U+R,U+L,D+R,D+L]]

def eq(const):
    def is_equal(p):
        return p == const
    return is_equal

def toposort(edges):
    nodes = set()
    incoming_nodes = collections.defaultdict(list)
    outgoing_nodes = collections.defaultdict(list)
    for a,b in edges:
        nodes.add(a)
        nodes.add(b)
        incoming_nodes[b] += [a]
        outgoing_nodes[a] += [b]

    L = []
    S = set(n for n in nodes if not incoming_nodes[n])

    while S:
        n = S.pop()
        L.append(n)

        for m in outgoing_nodes[n]:
            outgoing_nodes[n].remove(m)
            incoming_nodes[m].remove(n)
            if not incoming_nodes[m]:
                S.add(m)
    return L

def extract_subtree(graph, subtree_root):
    result = set()
    Q = collections.deque()
    Q.append(subtree_root)
    while Q:
        n = Q.popleft()
        for (a,b) in graph:
            if b == n:
                result.add((a,b))
                Q.append(a)
    return result