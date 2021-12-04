from common.advent_lib import *
import itertools as it

nums = to_nums(lines(10))
nums.append(0)
nums.append(max(nums)+3)
nums = sorted(nums)

diffs = [x-y for x,y in zip(nums[1:], nums)]

part1 = diffs.count(1) * diffs.count(3)
print("Part 1", part1)

edges = []
for start in nums:
    for end in [x for x in nums if 1 <= x - start <= 3]:
        edges.append((start, end))

paths = {0: 1}
for start in nums:
    for end in [b for a, b in edges if a == start]:
        paths[end] = paths.get(end, 0) + paths[start]

print("Part 2", paths[max(nums)])
