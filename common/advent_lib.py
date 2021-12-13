import collections
import functools as func
import itertools as it
import operator as op
import queue

from numpy import array as A

def full_input(day):
    return str(open("../input/%02d.txt" % day).read())

def lines(day):
    return [line.rstrip() for line in open("../input/%02d.txt" % day).readlines()]

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
    return iterable[0]

def second(iterable):
    return iterable[1]

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
R = A([[0, -1],
       [ 1, 0]])
L = R.T

abc = "abcdefghijklmnopqrstuvwxyz"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def inc(n):
    return n+1

def dec(n):
    return n-1

def manhattan_distance(a, b):
    return sum([abs(op.sub(*x)) for x in zip(a,b)])

def sgn(n):
    return -1 if n < 0 else 1

def bfs(current, goal, neighbor_fn):
    Q = collections.deque()
    seen = set()
    came_from = {}
    Q.append(current)
    while Q:
        node = Q.popleft()
        if node == goal:
            return reconstruct_path(node, came_from)
        for neighbor in neighbor_fn(node):
            if neighbor not in seen:
                seen.add(neighbor)
                Q.append(neighbor)


def reconstruct_path(node, came_from):
    path = collections.deque([node])
    while node in came_from:
        node = came_from[node]
        path.appendleft(node)
    return path

def a_star(start, goal_fn, neighbor_fn, dist_fn, heur_fn):
    open_set = queue.PriorityQueue()
    open_set.put((heur_fn(start), start))
    came_from = {}
    g_score = collections.defaultdict(lambda: float("inf"))
    g_score[start] = 0

    while not open_set.empty():
        current = open_set.get()[1] # Priority queues return (prio, elem) tuples
        if goal_fn(current):
            return reconstruct_path(came_from, current)

        for neighbor in neighbor_fn(current):
            tentative_gscore = g_score[current] + dist_fn(current, neighbor)
            if tentative_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score = tentative_gscore + heur_fn(neighbor)
                open_set.put((f_score, neighbor))

    raise Exception
