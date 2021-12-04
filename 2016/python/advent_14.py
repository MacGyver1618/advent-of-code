import hashlib

from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(14)[0]
salt = inpt
# salt = "abc"
keys = []

@func.cache
def gen_hash(i):
    return hashlib.md5((salt+str(i)).encode("utf-8")).hexdigest()

def is_key(i):
    h = gen_hash(i)
    triples = re.findall(r"(.)\1\1", h)
    if not triples:
        return False
    following = [gen_hash(n) for n in range(i+1, i+1001)]
    quint = "".join(it.repeat(triples[0], 5))
    if [n for n in following if quint in n]:
        return True
    return False

x = 0
while len(keys) < 64:
    if is_key(x):
        keys.append(x)
    x += 1

print("Part 1:", keys[63])

megakeys = []

@func.cache
def megahash(i):
    h = hashlib.md5((salt+str(i)).encode("utf-8")).hexdigest()
    for _ in range(2016):
        h = hashlib.md5(h.encode("utf-8")).hexdigest()
    return h

def is_megakey(i):
    h = megahash(i)
    triples = re.findall(r"(.)\1\1", h)
    if not triples:
        return False
    following = [megahash(n) for n in range(i+1, i+1001)]
    quint = "".join(it.repeat(triples[0], 5))
    if [n for n in following if quint in n]:
        return True
    return False

x = 0
while len(megakeys) < 64:
    if is_megakey(x):
        megakeys.append(x)
    x += 1


print("Part 2:", megakeys[63])
