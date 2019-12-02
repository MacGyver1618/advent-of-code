from advent_lib import *

masses = to_nums(lines(1))

def fuel_for(mass):
    return max(0, mass // 3 - 2)

part1 = sum(list(map(fuel_for, masses)))
print("Part 1: ", part1)

def total_fuel_for(mass):
    total_fuel = 0
    additional_fuel = fuel_for(mass)
    while additional_fuel > 0:
        total_fuel += additional_fuel
        additional_fuel = fuel_for(additional_fuel)
    return total_fuel

part2 = sum(list(map(total_fuel_for, masses)))
print("Part 2: ", part2)
