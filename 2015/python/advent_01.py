from advent_lib import *

inpt = lines(1)[0]

print("Part 1:", inpt.count("(")-inpt.count(")"))

floor = 0
for i,c in enumerate(inpt):
    if c == '(':
        floor += 1
    elif c == ')':
        floor -= 1
    if floor == -1:
        part2 = i+1
        break

print("Part 2:", part2)