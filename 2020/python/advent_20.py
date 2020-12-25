from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
from numpy import array as A, rot90, fliplr, flipud

inpt = full_input(20).rstrip().split("\n\n")

tiles = {}

for tilespec in inpt:
    n, spec = tilespec.split(":\n")
    tile = A(list(spec.replace("\n",""))).reshape(10,10)
    tiles[int(n.split(" ")[1])] = tile

edges = coll.defaultdict(list)

def transformations(a):
    a1 = rot90(a)
    a2 = rot90(a1)
    a3 = rot90(a2)
    a4 = fliplr(a)
    a5 = fliplr(a1)
    a6 = fliplr(a2)
    a7 = fliplr(a3)
    return a,a1,a2,a3,a4,a5,a6,a7

def edges_of(tile):
    return [
        tile[:,0],
        tile[:,9],
        tile[0,:],
        tile[9,:],
        tile[::-1,0],
        tile[::-1,9],
        tile[0,::-1],
        tile[9,::-1]
    ]

for name, tile in tiles.items():
    for edge in edges_of(tile):
        edges[str(edge)].append(name)

corners = []
for n,t in tiles.items():
    unique_edges = [e for e in edges_of(t) if len(edges[str(e)]) == 1]
    if len(unique_edges) == 4:
        corners.append(n)

def left_edge(tile):
    return tile[:,0]

def right_edge(tile):
    return tile[:,9]

def upper_edge(tile):
    return tile[0,:]

def lower_edge(tile):
    return tile[9,:]

def is_unique(edge):
    return len(edges[str(edge)]) == 1

print(corners)
print("Part 1:", product(corners))

def find_counterpart(tile_id, orientation_id, edge_extractor, join_extractor):
    tile = transformations(tiles[tile_id])[orientation_id]
    edge = edge_extractor(tile)
    other_id = [tid for tid in edges[str(edge)] if tid != tile_id][0]
    for other_orientation,other in enumerate(transformations(tiles[other_id])):
        other_edge = join_extractor(other)
        if str(edge) == str(other_edge):
            return other_id, other_orientation

# Assemble grid
assembled = []

# Find first corner and orient unique edges up and left
for i,a in enumerate(transformations(tiles[corners[0]])):
    if is_unique(upper_edge(a)) and is_unique(left_edge(a)):
        assembled.append((corners[0],i))
        break

# Assemble puzzle on a piece-by-piece basis

for i in range(1,144):
    if i % 12 == 0:
        assembled.append(find_counterpart(*assembled[i-12], lower_edge, upper_edge))
    else:
        assembled.append(find_counterpart(*assembled[i-1], right_edge, left_edge))

# Remove edges

def piece(tile_id, orientation_id):
    return transformations(tiles[tile_id])[orientation_id]

rows = []
for i in range(12):
    row = np.concatenate(list(map(lambda x: piece(*x)[1:-1,1:-1], assembled[i*12:i*12+12])), axis=1)
    rows.append(row)
grid = np.concatenate(rows, axis=0)

grid = (grid == '#')

sea_monster = (A(list("                  # #    ##    ##    ### #  #  #  #  #  #   ")).reshape(3,20) == '#')

# Find sea monsters

part2 = 0
for orientation, variant in enumerate(transformations(grid)):
    print()
    for i in range(0, 96-3):
        for j in range(0,96-20):
            section = variant[i:i + 3, j:j + 20]
            if ((section & sea_monster) == sea_monster).all():
                part2 += 1

grid_count = list(grid.flatten()).count(True)
monster_count = list(sea_monster.flatten()).count(True)

print("Part 2:", grid_count - part2*monster_count)