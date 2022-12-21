from common.advent_lib import *

inpt = read_lines(8)

print(inpt)
tot = 0
for line in inpt:
    decoded = bytes(line, "utf-8").decode("unicode_escape")
    tot += len(line)-len(decoded)+2

print("Part 1:", tot)

tot = 0
for line in inpt:
    encoded = "\"" + line.replace("\\", "\\\\").replace("\"","\\\"") + "\""
    print(line)
    print(encoded)
    input()
    tot += len(encoded) - len(line)
print("Part 2:", tot)
