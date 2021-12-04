from common.advent_lib import *
import re

inpt = lines(7)

def eval():
    L = []
    S = set()
    edges = []
    rules = {}
    values = {}
    for line in inpt:
        expr, out = line.split(" -> ")
        ins = re.findall(r"[a-z]+", expr)
        rules[out] = expr.split(" ")
        if not ins:
            S.add(out)
        for i in ins:
            edges.append((i, out))

    while S:
        n = S.pop()
        L.append(n)
        for edge in [(a,b) for a,b in edges if a == n]:
            _, child = edge
            edges.remove(edge)
            if not [_ for a,b in edges if b == child]:
                S.add(child)

    def value_of(node):
        return values[node] if node in values else int(node)

    for node in L:
        rule = rules.get(node)
        if len(rule) == 1:
            values[node] = value_of(rule[0])
        elif len(rule) == 2:
            values[node] = ~value_of(rule[1])
        else:
            a = value_of(rule[0])
            op = rule[1]
            b = value_of(rule[2])
            if op == 'RSHIFT':
                values[node] = a >> b
            if op == 'LSHIFT':
                values[node] = a << b
            if op == 'AND':
                values[node] = a & b
            if op == 'OR':
                values[node] = a | b
    return values["a"]

part1 = eval()
print("Part 1:", part1)

for i,line in enumerate(inpt):
    if line.endswith("-> b"):
        inpt[i] = "{:d} -> b".format(part1)
print("Part 2:", eval())
