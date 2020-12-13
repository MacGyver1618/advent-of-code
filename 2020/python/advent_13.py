from advent_lib import *
from sympy.ntheory.modular import crt

inpt = lines(13)
min_time = int(inpt[0])
timestamps = inpt[1].split(",")
nums = [int(t) for t in timestamps if t != 'x']

for time in it.count(min_time):
    divisors = [x for x in nums if time % x == 0]
    if divisors:
        part1 = divisors[0]*(time-min_time)
        break

print("Part 1:", part1)

nums, mods = zip(*[(int(x), int(x) - i) for i, x in enumerate(timestamps) if x != 'x'])
print("Part 2:", crt(nums, mods)[0])
