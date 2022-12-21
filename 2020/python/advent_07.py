import re
from common.advent_lib import *
from collections import deque

input = read_lines(7)

edges = set()

for line in input:
    start, rest = line.split(" bags contain ")
    if not rest.startswith("no"):
        for bag in rest.split(", "):
            weight, end = re.match(r"(\d+) ([a-z]+ [a-z]+) bag", bag).groups()
            edges.add((start, end, int(weight)))

q = deque()
found = set()
q.append("shiny gold")
while len(q) > 0:
    node = q.pop()
    for (start, end, weight) in edges:
        if node == end and start not in found:
            found.add(start)
            q.append(start)

print("Part 1:", len(found))

def weight(node):
    return 1 + sum([count * weight(end) for start, end, count in edges if start == node])

print("Part 2:", weight("shiny gold")-1)
