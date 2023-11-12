import time

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

lines = read_lines(15)
R=len(lines)
C=len(lines[0])
ROW,COLUMN,ID,FACTION,ATTACK,HP,TURNS=0,1,2,3,4,5,6

original_units=[]
grid=[]
i=0
for r,line in enumerate(lines):
    row=[]
    for c,char in enumerate(line):
        if char in ["E","G"]:
            original_units+=[(r,c,i,char,3,200,0)]
            i+=1
            row+=["."]
        else:
            row+=[char]
    grid+=[row]


def print_grid(units, special_groups=[]):
    ss=[]
    for r in range(R):
        s=""
        for c in range(C):
            if special_groups and (r,c) in special_groups[0]:
                s+=special_groups[1]
            elif (r,c) in [unit[:2] for unit in units]:
                s+=[unit[FACTION] for unit in units if unit[ROW]==r and unit[COLUMN]==c][0]
            else:
                s+=grid[r][c] if grid[r][c]=="#" else " "
        units_on_row=[f"{u[FACTION]}({u[HP]})" for u in sorted(units,key=second) if u[ROW]==r]
        if units_on_row:
            s+=f"   {', '.join(units_on_row)}"
        ss+=[s]
    print("\n".join(ss))

def adjacent_ro(r,c):
    yield r-1,c
    yield r,c-1
    yield r,c+1
    yield r+1,c

def in_range(r,c):
    for nr,nc in adjacent_ro(r,c):
        if grid[nr][nc] not in ["#"]:
            yield nr,nc

def reachable_neighborhood(p,unit_positions):
    return [(nr,nc) for (nr,nc) in in_range(*p) if (nr,nc) not in unit_positions]

def distance_to(start, target, unit_positions):
    bfs_result = bfs(start,eq(target),lambda p: reachable_neighborhood(p, unit_positions))
    return -1 if isinstance(bfs_result, set) else len(bfs_result)-1

def can_attack(unit, units):
    r,c,_,faction,*_=unit
    enemy_positions=[unit[:2] for unit in units if unit[FACTION]!=faction]
    return [enemy for enemy in enemy_positions if enemy in adjacent_ro(r,c)]

def play_game(attack_power=3,part2=False):
    units=original_units.copy()
    rounds=0
    while sorted(set([unit[FACTION] for unit in units]))==["E","G"]:
        unit=[unit for unit in sorted(units) if unit[TURNS] == rounds][0]
        r,c,uid,faction,attack,hp,turns=unit
        if faction=="E":
            attack=attack_power
        unit_positions=[unit[:2] for unit in units]
        enemies=[unit for unit in units if unit[FACTION]!=faction]
        if can_attack(unit, units):
            attackable_enemies=[enemy for enemy in enemies if enemy[:2] in adjacent_ro(r,c)]
            closest_enemy=sorted(attackable_enemies,key=lambda e:(e[HP],e[ROW],e[COLUMN]))[0]
            er,ec,eid,ef,ea,ehp,et=closest_enemy
            units.remove(unit)
            units.append((r,c,uid,faction,attack,hp,turns+1))
            units.remove(closest_enemy)
            if ehp-attack>0:
                units.append((er,ec,eid,ef,ea,ehp-attack,et))
            else:
                if part2 and ef=="E":
                    raise Exception("Elves lost")
                if sorted(set([unit[FACTION] for unit in units]))!=["E","G"]:
                    break
        else:
            in_ranges=[square for er,ec,*_ in enemies for square in in_range(er, ec) if square not in unit_positions]
            distances=[(square, distance_to((r, c), square, unit_positions)) for square in in_ranges]
            distances=[(s,d) for s,d in distances if d>=0]
            nearest=[s for s,d in distances if d==min(d for _,d in distances)]
            if nearest:
                chosen=sorted(nearest)[0]
                path_to_chosen=bfs((r,c),eq(chosen),lambda p: reachable_neighborhood(p, unit_positions))
                next_move=path_to_chosen[1]
                units.remove(unit)
                unit_after_move = (*next_move, uid, faction, attack, hp, turns + 1)
                units.append(unit_after_move)
                if can_attack(unit_after_move, units):
                    r,c=next_move
                    attackable_enemies=[enemy for enemy in enemies if enemy[:2] in adjacent_ro(r,c)]
                    closest_enemy=sorted(attackable_enemies,key=lambda e:(e[HP],e[ROW],e[COLUMN]))[0]
                    er,ec,eid,ef,ea,ehp,et=closest_enemy
                    units.remove(closest_enemy)
                    if ehp-attack>0:
                        units.append((er,ec,eid,ef,ea,ehp-attack,et))
                    else:
                        if part2 and ef=="E":
                            raise Exception("Elves lost")
                        if sorted(set([unit[FACTION] for unit in units]))!=["E","G"]:
                            break
            else:
                units.remove(unit)
                units.append((r,c,uid,faction,attack,hp,turns+1))
        if (min(r for *_,r in units)) > rounds:
            rounds += 1
    return rounds*sum(unit[HP] for unit in units)

part1 = play_game()
print("Part 1:", part1)

score=-1
attack_power=17
while score==-1:
    try:
        print(f"Trying attack power {attack_power}")
        score=play_game(attack_power=attack_power,part2=True)
        part2=score
    except Exception:
        attack_power+=1
print("Part 2:", part2)
