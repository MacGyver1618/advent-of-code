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

lines = read_lines(21)

edges = set()
vals = dict()
exprs = dict()

for line in lines:
    monkey, rest = line.split(": ")
    val = re.findall("\d+", rest)
    if val:
        exprs[monkey] = val[0]
        vals[monkey] = int(val[0])
    else:
        exprs[monkey] = rest
        a, _, b = rest.split()
        edges.add((a,monkey))
        edges.add((b,monkey))

for n in toposort(edges):
    if n in vals:
        continue
    expr = exprs[n]
    a,op,b = expr.split()
    if op == "*":
        vals[n] = vals[a]*vals[b]
    if op == "/":
        vals[n] = vals[a]//vals[b]
    if op == "-":
        vals[n] = vals[a]-vals[b]
    if op == "+":
        vals[n] = vals[a]+vals[b]

s = exprs["root"]
toks = re.findall(r"[a-z]{4}", s)
while toks:
    for tok in toks:
        s = s.replace(tok, f"({exprs[tok]})")
    toks = re.findall(r"[a-z]{4}", s)
print(int(eval(s)))
print("Part 1:", vals["root"])

inverted_vals = dict()
path = list(reversed(dfs("humn", eq("root"), lambda n: [b for a,b in edges if a == n])))
cur = "root"

for n in path:
    if n == "humn":
        break
    if n == "root":
        a,b = [a for a,b in edges if b == "root"]
        inverted_vals[a] = vals[b]
        inverted_vals[b] = vals[a]
        continue
    expr = exprs[n]
    a,op,b = expr.split()
    human_first = a in path
    if op == "*":
        if human_first:
            inverted_vals[a] = inverted_vals[n] // vals[b]
        else:
            inverted_vals[b] = inverted_vals[n] // vals[a]
    if op == "/":
        if human_first:
            inverted_vals[a] = inverted_vals[n] * vals[b]
        else:
            inverted_vals[b] = vals[a] // inverted_vals[n]
    if op == "-":
        if human_first:
            inverted_vals[a] = inverted_vals[n] + vals[b]
        else:
            inverted_vals[b] = vals[a] - inverted_vals[n]
    if op == "+":
        if human_first:
            inverted_vals[a] = inverted_vals[n] - vals[b]
        else:
            inverted_vals[b] = inverted_vals[n] - vals[a]

curtree = edges
while False:
    if cur == "humn":
        break
    left, right = [a for a,b in curtree if b == cur]
    ltree = extract_subtree(curtree, left)
    rtree = extract_subtree(curtree, right)
    human_on_left = "humn" in [a for a,b in ltree] or left == "humn"
    if cur == "root":
        if human_on_left:
            inverted_vals[left] = vals[right]
        else:
            inverted_vals[right] = vals[left]
    else:
        expr = exprs[cur]
        a,op,b = expr.split()
        human_first = human_on_left and left == a or not human_on_left and left == b or a == "humn"
        if op == "*":
            if human_first:
                inverted_vals[a] = inverted_vals[cur] // vals[b]
            else:
                inverted_vals[b] = inverted_vals[cur] // vals[a]
        if op == "/":
            if human_first:
                inverted_vals[a] = inverted_vals[cur] * vals[b]
            else:
                inverted_vals[b] = vals[a] // inverted_vals[cur]
        if op == "-":
            if human_first:
                inverted_vals[a] = inverted_vals[cur] + vals[b]
            else:
                inverted_vals[b] = vals[a] - inverted_vals[cur]
        if op == "+":
            if human_first:
                inverted_vals[a] = inverted_vals[cur] - vals[b]
            else:
                inverted_vals[b] = inverted_vals[cur] - vals[a]

    cur = left if human_on_left else right
    curtree = ltree if human_on_left else rtree

print("Part 2:", inverted_vals["humn"])
