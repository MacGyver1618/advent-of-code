from collections import defaultdict, deque
from common.advent_lib import *

inpt = lines(21)

ingredients = set()
recipes = []

for line in inpt:
    r, a = line.split(" (contains ")
    a = set(a[:-1].split(", "))
    r = set(r.split(" "))
    recipes.append((r, a))
    ingredients.update(r)

allergen_translations = defaultdict(lambda: set(ingredients))

for r,a in recipes:
    for allergen in a:
        allergen_translations[allergen].intersection_update(r)

Q = deque()
for k,v in allergen_translations.items():
    if len(v) == 1:
        Q.append((k,v))

while Q:
    n,[t] = Q.popleft()
    for k,v in allergen_translations.items():
        if len(v) == 1:
            continue
        v.discard(t)
        if len(v) == 1:
            Q.append((k,v))

found_allergens = union(allergen_translations.values())

part1 = 0
for r,_ in recipes:
    part1 += len(set(r).difference(found_allergens))

print("Part 1:", part1)

part2 = []
for k,v in sorted(allergen_translations.items()):
    part2 += v

print("Part 2:", ",".join(part2))
