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

steps = 0
atoms = atoms_of(mol)
# No replacement starts with a terminal other than C, which isn't in the output
# Therefore, we can assume the start with a intermediate
s = mol
while len(s) > 2:
    s2 = ""
    # Reduce strings of intermediates to single intermediate, counting iterations
    for atom in atoms_of(s):
        if atom in terminals:
            s2 += "S"
            s2 += atom
            steps -= 1
        else:
            steps += 1
    # Replace occurrences of SRnSAr and SRnSYSAr with S
    steps += s2.count("SRnSAr")
    s2 = s2.replace("SRnSAr", "S")
    steps += s2.count("SRnSYSAr")
    s2 = s2.replace("SRnSYSAr", "S")
    s = s2

# The final (first) step taken was e => SS
steps += 1

print("Part 2:", steps)
