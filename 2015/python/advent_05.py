from advent_lib import *
import re

inpt = lines(5)

def is_nice(s):
    return len(re.findall(r"[aeiou]", s)) >= 3 and re.findall(r"(.)\1", s) and not re.findall(r"(ab|cd|pq|xy)", s)

print("Part 1:", len(list(filter(is_nice, inpt))))

def is_nice2(s):
    return re.findall(r"(..).*\1", s) and re.findall(r"(.).\1", s)

print("Part 2:", len(list(filter(is_nice2, inpt))))
