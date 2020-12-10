from advent_lib import *
import itertools as it

nums = to_nums(lines(10))
nums.append(0)
nums.append(max(nums)+3)

nums = sorted(nums)
diffs = [x-y for x,y in zip(nums[1:], nums[0:-1])]

part1 = diffs.count(1) * diffs.count(3)
print("Part 1", part1)

edges = []
for start in nums:
    for end in [x for x in nums if 1 <= x - start <= 3]:
        edges.append((start, end))

q = sorted(nums, reverse=True)
paths = {154: 1}
for end in q:
    for start in [a for a, b in edges if b == end]:
        paths[start] = paths.get(start, 0) + paths[end]

print("Part 2", paths[0])
