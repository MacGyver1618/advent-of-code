import collections
import functools as func
import os
import re
import subprocess
from datetime import datetime
import time

import itertools as it
import operator as op
import queue

import math
import sys
from heapdict import heapdict
from numpy import array as A

def get_day(day):
    file_path=f"../input/{day:02d}.txt"
    file_present=os.path.exists(file_path)
    year=os.getcwd().split("/")[-2]
    day_unlock_time=datetime.fromisoformat(f"{year}-12-{day:02d}T07:00:00")
    day_unlocked = datetime.now() > day_unlock_time
    if day_unlocked and not file_present:
        subprocess.run(["./fetch.sh", year, str(day)], shell=True, cwd="../..", capture_output=True)
    elif not file_present:
        raise ValueError(f"{year} day {day} not unlocked yet!")
    return open(file_path)

def full_input(day):
    return str(get_day(day).read())

def read_lines(day):
    return [line[:-1] for line in get_day(day).readlines()]

def to_nums(string_arr):
    return list(map(int, string_arr))

def read_grid(day):
    lines = read_lines(day)
    R = len(lines)
    C = len(lines[0])
    return R, C, [[c for c in line] for line in lines]

def parse_ints(line):
    return [int(d) for d in re.findall(r"\d+", line)]

def parse_floats(line):
    return [float(d) for d in re.findall(r"\d+(?:\.\d+)?", line)]

def intersection(iterable):
    return set(func.reduce(set.intersection, [set(i) for i in iterable]))

def union(iterable):
    return set(func.reduce(set.union, [set(i) for i in iterable], set()))

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
    return [*path]

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

def all_paths(start, goal_fn, neighbor_fn):
    Q = collections.deque([[start]])
    paths = []
    while Q:
        path = Q.popleft()
        pos = path[-1]

        if goal_fn(pos):
            paths+=[path]
        else:
            for n in neighbor_fn(pos):
                if n not in path:
                    Q.append(path+[n])
    return paths

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
    return seen

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

def true(*_):
    return True

def false(*_):
    return False

def flip(fn):
    def flipped(a,b):
       return fn(b,a)
    return flipped

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

def timed(fn):
    start = time.time()
    result = fn()
    end = time.time()
    return end-start, result

def pretty_time(seconds):
    if seconds > 60:
        return f"{int(seconds//60)} m {int(seconds%60)} s"
    if seconds > 1:
        return f"{round(seconds, 2)} s"
    nanos=int(seconds*1e9)
    if nanos > 1_000_000:
        return f"{nanos//1_000_000} ms"
    if nanos > 1_000:
        return f"{nanos//1_000} µs"
    return f"{nanos} ns"

def find_nth_in_cycle(latest,history,nth):
    offset=history.index(latest)
    cycle_length=len(history)-offset
    phase = (nth-offset)%cycle_length
    return history[phase+offset]

def cycle_until_nth(state, iterate, nth):
    history=[state]
    while (state:=iterate(state)) not in history:
        history+=[state]
    return find_nth_in_cycle(state,history,nth)

class Spinner:

    @staticmethod
    def _spinning_cursor():
        while True:
            for cursor in "-\\|/":
                yield cursor

    def __init__(self):
        self._generator=Spinner._spinning_cursor()
        self._started=False

    def spin(self):
        if not self._started:
            self._started=True
        else:
            sys.stdout.write("\r")
        sys.stdout.write(next(self._generator))
        sys.stdout.flush()

    def stop(self):
        self._started=False
        sys.stdout.write("\r")
        sys.stdout.flush()

class ProgressBar:

    def __init__(self, capacity):
        self._capacity=capacity
        self._progress=0
        self._tics=0
        self._started=False
        self._start_time=None
        self._elapsed=0

    def update(self):
        if not self._started:
            sys.stdout.write("\033[?25l")
            self._started=True
            self._start_time=time.time()
            sys.stdout.write(f"[{' '*50}]")
        self._progress+=1
        tics=(self._progress*50)//self._capacity
        sys.stdout.write(f"\r\033[53C {pretty_time(self.time_taken())}\033[K")
        if tics>self._tics:
            self._tics=tics
            sys.stdout.write("\r")
            if self._progress <= self._capacity:
                sys.stdout.write(f"[{'='*tics}{' '*(50-tics)}]")
            else:
                message=f"*** OVERFLOW {self._progress}/{self._capacity} ***"
                l=50-len(message)
                head=math.floor(l/2)
                tail=math.ceil(l/2)
                sys.stdout.write(f"[{head*' '}{message}{tail*' '}]")
        sys.stdout.flush()

    def clear(self):
        self._started=False
        sys.stdout.write("\r\033[K\033[?25h")
        sys.stdout.flush()

    def time_taken(self):
        return time.time()-self._start_time

    def reset(self):
        self._tics=0
        self._progress=0
        self._started=False

class Grid:
    def __init__(self, lines):
        self.R = len(lines)
        self.C = len(lines[0])
        self.raw_grid = [[c for c in line] for line in lines]

    def in_bounds(self, point):
        r,c=point
        return 0 <= r < self.R and 0 <= c < self.C

    def char_at(self, point):
        r,c=point
        return self.raw_grid[r][c]

    def int_at(self, point):
        return int(self.char_at(point))

    def points(self):
        for r in range(self.R):
            for c in range(self.C):
                yield r,c

    def items(self):
        for r in range(self.R):
            for c in range(self.C):
                yield (r,c),self.raw_grid[r][c]

    def neighbors(self, p):
        for n in adjacent(p):
            if self.in_bounds(n):
                yield n
