from common.advent_lib import *
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

from intcode import IntCodeMachine

machines=[IntCodeMachine.from_day_input(23) for _ in range(50)]
for i,machine in enumerate(machines):
    machine.input(i)

nat=[]
sent=set()
part1=None
try:
    while True:
        if all(not machine.inputs_queued() for machine in machines) and nat:
            x,y = nat[-1]
            if y in sent:
                part2=y
                break
            machines[0].input(x,y)
            sent.add(y)
        for machine in machines:
            machine.run()
            if not machine.inputs_queued():
                machine.input(-1)
            machine.run()
            while machine.outputs_queued():
                addr,x,y=machine.read_n(3)
                if addr==255:
                    if not part1:
                        part1=y
                    nat+=[(x,y)]
                else:
                    machines[addr].input(x,y)
except Exception as e:
    print(e)


print("Part 1:", part1)


print("Part 2:", part2)
