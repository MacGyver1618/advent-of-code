from common.advent_lib import *
import re

inpt = lines(14)

mem = {}

def applymask(mask, value):
    out = list("{:036b}".format(value))
    for i,c in enumerate(mask):
        if c == "X":
            continue
        elif c == "1":
            out[i] = "1"
        elif c == "0":
            out[i] = "0"
    return int("".join(out), base=2)

for line in inpt:
    instr, value = line.split(" = ")
    if instr == 'mask':
        mask = value
    else:
        addr = int(re.match(r"mem\[(\d+)\]", instr).groups()[0])
        mem[addr] = applymask(mask, int(value))

print("Part 1:", sum(mem.values()))

mem = {}

def getaddrs(mask, base):
    chars = list(mask)
    xs = int(chars.count("X"))
    for i in range(2**xs):
        addr = list("{:036b}".format(base))
        floatmask = list("{:0{:d}b}".format(i, xs))
        maskpos = 0
        for j, char in enumerate(chars):
            if char == "1":
                addr[j] = "1"
            elif char == "X":
                addr[j] = floatmask[maskpos]
                maskpos += 1
        yield int("".join(addr), base=2)

def applymask2(mask, baseaddr, value):
    for addr in getaddrs(mask, baseaddr):
        mem[addr] = value

for line in inpt:
    instr, value = line.split(" = ")
    if instr == 'mask':
        mask = value
    else:
        addr = int(re.match(r"mem\[(\d+)\]", instr).groups()[0])
        applymask2(mask, addr, int(value))

print("Part 2:", sum(mem.values()))