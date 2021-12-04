from common.advent_lib import *

inpt = lines(2)

area = 0
ribbon = 0
for line in inpt:
    l,h,w = map(int, line.split("x"))
    sides = [2*l*h, 2*l*w, 2*w*h]
    area += sum(sides) + min(sides) // 2
    ribbon += min([2*(l+h),2*(l+w),2*(w+h)]) + l*h*w

print("Part 1:", area)
print("Part 2:", ribbon)