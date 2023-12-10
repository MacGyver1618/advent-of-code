from common.advent_lib import *
import functools as func
import itertools as it
import operator as oper

lines = read_lines(9)

part1=0
part2=0
for line in lines:
    nums=[[*map(int,line.split())]]
    while not all(i==0 for i in nums[-1]):
        nums+=[[a-b for a,b in zip(nums[-1][1:], nums[-1][:-1])]]
    part1+=func.reduce(oper.add, [n[-1] for n in nums])
    part2+=func.reduce(flip(oper.sub), [n[0] for n in nums[::-1]])

print("Part 1:", part1)
print("Part 2:", part2)
