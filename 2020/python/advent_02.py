from common.advent_lib import *
import itertools as iter
import re

lines = lines(2)

def matches(s):
    min, max, char, pw = re.match(r"(\d+)-(\d+) (.): (.+)", s).groups()
    count = len(list(re.finditer(re.compile(char), pw)))
    return count >= int(min) and count <= int(max)


print("Part 1: ", len(list(filter(matches, lines))))

def matches2(s):
    min, max, char, pw = re.match(r"(\d+)-(\d+) (.): (.+)", s).groups()
    return (pw[int(min)-1] == char) ^ (pw[int(max)-1] == char)

print("Part 2: ", len(list(filter(matches2, lines))))
