from advent_lib import *

nums = to_nums(lines(1))

part1 = [ x*y for x in nums for y in nums if x + y == 2020 ][0]
print("Part 1: ", part1)

part2 = [x*y*z for x in nums for y in nums for z in nums if x + y + z == 2020][0]
print("Part 2: ", part2)
