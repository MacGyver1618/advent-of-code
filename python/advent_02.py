from advent_lib import *
import itertools as iter

input = to_nums(lines(2)[0].split(","))

def eval(a, b):
    nums = input.copy()
    nums[1:3] = (a, b)
    pos = 0
    (op, a, b, c) = nums[pos:pos+4]
    while op != 99:
        if   op == 1: nums[c] = nums[a] + nums[b]
        elif op == 2: nums[c] = nums[a] * nums[b]
        pos += 4
        (op, a, b, c) = nums[pos:pos+4]
    return nums[0]

print("Part 1: ", eval(12, 2))

for noun, verb in iter.product(range(100), range(100)):
    if eval(noun, verb) == 19690720:
        print("Part 2: ", noun*100 + verb)
        break
