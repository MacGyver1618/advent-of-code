from common.advent_lib import *

inpt = to_nums(read_lines(24))

part1 = min([product(ss) for ss in it.combinations(inpt, 6) if sum(ss) == sum(inpt) // 3])
print("Part 1:", part1)

part2 = min([product(ss) for ss in it.combinations(inpt, 4) if sum(ss) == sum(inpt) // 4])
print("Part 2:", part2)
