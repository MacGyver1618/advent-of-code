from common.advent_lib import *

input = read_lines(8)

def loop():
    pc = 0
    acc = 0
    history = []
    while True:
        if pc == len(input):
            return True, acc
        if pc in history:
            return False, acc
        history.append(pc)
        op, amt = input[pc].split(" ")
        if op == "nop":
            pc += 1
        elif op == "acc":
            pc += 1
            acc += int(amt)
        elif op == "jmp":
            pc += int(amt)

_, part1 = loop()
print("Part 1:", part1)

for pos, instr in [(i, input[i]) for i in range(0, len(input))]:
    op, amt = instr.split(" ")
    if op == "nop":
        input[pos] = " ".join(["jmp", amt])
    elif op == "jmp":
        input[pos] = " ".join(["nop", amt])
    halted, result = loop()
    if halted:
        part2 = result
        break
    if op == "nop":
        input[pos] = " ".join(["nop", amt])
    elif op == "jmp":
        input[pos] = " ".join(["jmp", amt])
print("Part 2:", part2)
