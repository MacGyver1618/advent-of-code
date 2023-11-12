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

lines = read_lines(14)
target=int(lines[0])

recipes=[3,7]
elf1=0
elf2=1

while len(recipes)<target+10:
    current_recipe=recipes[elf1]+recipes[elf2]
    if current_recipe>9:
        recipes+=[current_recipe//10,current_recipe%10]
    else:
        recipes+=[current_recipe]
    elf1+=recipes[elf1]+1
    elf1%=len(recipes)
    elf2+=recipes[elf2]+1
    elf2%=len(recipes)

part1 = "".join(str(i) for i in recipes[target:target+10])
print("Part 1:", part1)


recipes=[3,7]
elf1=0
elf2=1

target=[int(c) for c in str(target)]
while recipes[-len(target):] != target and recipes[-len(target)-1:-1] != target:
    current_recipe=recipes[elf1]+recipes[elf2]
    if current_recipe>9:
        recipes+=[current_recipe//10,current_recipe%10]
    else:
        recipes+=[current_recipe]
    elf1+=recipes[elf1]+1
    elf1%=len(recipes)
    elf2+=recipes[elf2]+1
    elf2%=len(recipes)

part2 = len(recipes)-len(target) - (0 if recipes[-len(target):]==target else 1)
print("Part 2:", part2)
