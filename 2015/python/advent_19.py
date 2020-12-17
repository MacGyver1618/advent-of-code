from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
import heapq

inpt = full_input(19)
ts, mol = inpt.split("\n\n")
mol = mol.rstrip()
rules = []
for line in ts.splitlines():
    a,b = line.split(" => ")
    rules.append((a,b))

def rules_for(atom):
    return [(a,b) for a,b in rules if a == atom]

def children(molecule):
    atoms = atoms_of(molecule)
    for i, atom in enumerate(atoms):
        for _,b in rules_for(atom):
            new_molecule = atoms.copy()
            new_molecule[i] = b
            yield "".join(new_molecule)


def atoms_of(molecule):
    return re.split(r"(?=[A-Z])(?<!^)", molecule)


part1=0
print("Part 1:", len(set(children(mol))))

def parents(M):
    for a,m in sorted(rules, key=lambda r: len(r[1]), reverse=True):
        for i in range(len(M)-len(m)):
            ss = M[i:i+len(m)]
            if ss == m:
                yield M[:i] + a + M[i+len(m):]

lefts = set([a for a,_ in rules])
rights = union([set(re.split(r"(?=[A-Z])(?<!^)", m)) for _,m in rules])
initials = [i for i in lefts if i not in rights]
terminals = [i for i in rights if i not in lefts]
intermediates = lefts.union(rights)
#rules = [(a,m) for a,m in rules if not m.startswith("CRn")]
o = []
for _,m in rules:
    s = ""
    for atom in re.split(r"(?=[A-Z])(?<!^)", m):
        if atom in terminals:
            s += "T"
        else:
            s += "s"
    o.append(s)
dist = {mol: 0}
Q = []
seen = set()

Q.append((len(mol), mol))
seen.add(mol)

min = 506
while Q:
    _,v = heapq.heappop(Q)
    if len(v) < min:
        min = len(v)
        print(len(v))
    if v == "e":
        break
    for w in parents(v):
        if w not in seen:
            dist[w] = dist[v] + 1
            seen.add(w)
            Q.append((len(w),w))

print("Part 2:", dist["e"])
