from advent_lib import *
import itertools as it

input = to_nums(lines(9))

def valid(n):
    prev = input[n-25:n]
    return input[n] not in [x+y for x in prev for y in prev]

part1 = [input[n] for n in range(25,len(input)) if valid(n)][0]
print("Part 1:", part1)

def part2():
    for l in range(2, len(input)):
        sublists = [input[i:i+l] for i in range(0,len(input)-l)]
        for sublist in sublists:
            if sum(sublist) == part1:
                return min(sublist)+max(sublist)


print("Part 2:", part2())
