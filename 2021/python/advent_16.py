from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(16)

stream = "".join(["{:04b}".format(int(x, 16)) for x in inpt[0]])
versions = 0

def parse_literal(pos):
    parsed = ""
    found_last = False
    while not found_last:
        parsed += stream[pos+1:pos+5]
        if stream[pos] == "0":
            found_last = True
        pos += 5
    return pos, int(parsed, 2)

def parse_operator(pos, operator):
    orig = pos
    length_id = stream[pos]
    operands = []
    if length_id == "0": # read length
        total_bits = int(stream[pos+1:pos+16], 2)
        pos += 16
        while pos < orig + 16 + total_bits:
            pos, value = parse_pkt(pos)
            operands.append(value)
    else: # read pkg count
        num_pkgs = int(stream[pos+1:pos+12], 2)
        parsed = 0
        pos += 12
        while parsed < num_pkgs:
            pos, value = parse_pkt(pos)
            operands.append(value)
            parsed += 1
    return pos, operator(operands)

def parse_pkt(pos):
    global versions
    version = int(stream[pos:pos+3], 2)
    versions += version
    type_id = int(stream[pos+3:pos+6],2)
    if type_id == 4: # literal
        return parse_literal(pos+6)
    elif type_id == 0:
        return parse_operator(pos+6, sum)
    elif type_id == 1:
        return parse_operator(pos+6, product)
    elif type_id == 2:
        return parse_operator(pos+6, min)
    elif type_id == 3:
        return parse_operator(pos+6, max)
    elif type_id == 5:
        return parse_operator(pos+6, lambda o: 1 if o[0] > o[1] else 0)
    elif type_id == 6:
        return parse_operator(pos+6, lambda o: 1 if o[0] < o[1] else 0)
    elif type_id == 7:
        return parse_operator(pos+6, lambda o: 1 if o[0] == o[1] else 0)

_, val = parse_pkt(0)

print("Part 1:", versions)
print("Part 2:", val)
