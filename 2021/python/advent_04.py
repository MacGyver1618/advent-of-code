from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(4)
nums = to_nums(inpt[0].split(","))

boards = []

board = []
for line in inpt[2:]:
    if line == "":
        boards.append(board)
        board = []
        continue
    board.append(list(map(int, re.split(r" +", line.strip()))))

hits = set()
col_hits = coll.defaultdict(lambda: 0)
row_hits = coll.defaultdict(lambda: 0)
bingo_scores = []

def has_bingo(board_num):
    col_bingo = max([col_hits[(board_num, x)] for x in range(5)]) == 5
    row_bingo = max([row_hits[(board_num, x)] for x in range(5)]) == 5
    return col_bingo or row_bingo

for num in nums:
    hits.add(num)
    for i, board in enumerate(boards):
        for x in range(5):
            for y in range(5):
                if board[x][y] == num:
                    row_hits[(i, y)] += 1
                    col_hits[(i, x)] += 1
        if i not in map(first, bingo_scores) and has_bingo(i):
            bingo_scores.append((i, num * sum([x for row in board for x in row if x not in hits])))

print("Part 1:", bingo_scores[0][1])
print("Part 2:", bingo_scores[-1][1])
