from advent_lib import *
from functools import reduce

input = lines(8)[0]
def chunk(arr, size):
    return [arr[x:x+size] for x in range(0, len(arr), size)]
layers = chunk(input, 150)

def count(layer, char):
    return len(list(filter(lambda x: x == char, layer)))

digits = [(count(l, '0'), count(l, '1'), count(l, '2')) for l in layers]

digits.sort()
print("Part 1:", digits[0][1]*digits[0][2])

def overlay(xs, ys):
    return "".join([y if x == '2' else x for x,y in zip(xs,ys)])

output = "".join(['*' if x == '1' else ' ' for x in reduce(overlay, layers)])

print("Part 2")
for line in chunk(output, 25):
    print(line)
