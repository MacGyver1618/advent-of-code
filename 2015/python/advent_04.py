from common.advent_lib import *
import itertools as it
import hashlib

inpt = read_lines(4)[0]

def md5(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()

for i in it.count(0):
    if md5("".join([inpt, str(i)])).startswith("00000"):
        part1 = i
        break


print("Part 1:", part1)

for i in it.count(0):
    if md5("".join([inpt, str(i)])).startswith("000000"):
        part2 = i
        break

print("Part 2:", part2)
