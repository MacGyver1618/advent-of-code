from advent_lib import *
import itertools as iter
import functools as func
import math

groups = [group.splitlines() for group in full_input(6).split("\n\n")]

part1 = sum([len(union(group)) for group in groups])
print("Part 1:", part1)

part2 = sum([len(intersection(group)) for group in groups])
print("Part 2:", part2)
