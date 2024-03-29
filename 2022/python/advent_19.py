import math

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

lines = read_lines(19)

blueprints = [tuple(to_nums(re.findall(r"(\d+)", line))) for line in lines]

max_geodes = defaultdict(int)
def neighbors(blueprint):
    no,ore_ore,clay_ore,obs_ore,obs_clay,geo_ore,geo_obs = blueprint
    def neighbor_fn(state):
        time_left,ore,clay,obsidian,geodes,ore_robots,clay_robots,obsidian_robots,geode_robots = state
        max_geodes[no] = max(max_geodes[no], geodes)
        if time_left == 0:
            return
        upper_bound = time_left * (time_left + 1) // 2 + geodes
        #if upper_bound < max_geodes[no]:
        #    return
        if obsidian_robots >= geo_obs and ore_robots >= geo_ore:
            return 0,0,0,0,upper_bound,0,0,0,0
        next_time = time_left-1
        most_ore = max(geo_ore, obs_ore, clay_ore, ore_ore)
        next_ore = min(most_ore, ore+ore_robots)
        next_clay = min(obs_clay, clay+clay_robots)
        next_obsidian = min(geo_obs, obsidian+obsidian_robots)
        next_geodes = geodes+geode_robots
        # to next geode robot
        if ore >= geo_ore and obsidian >= geo_obs:
            yield next_time,next_ore-geo_ore,next_clay,next_obsidian-geo_obs,next_geodes,ore_robots,clay_robots,obsidian_robots,geode_robots+1
        # to next obsidian robot
        if ore >= obs_ore and clay >= obs_clay and obsidian_robots < geo_obs:
            yield next_time,next_ore-obs_ore,next_clay-obs_clay,next_obsidian,next_geodes,ore_robots,clay_robots,obsidian_robots+1,geode_robots
        # to next clay robot
        if ore >= clay_ore and clay_robots < obs_clay:
            yield next_time,next_ore-clay_ore,next_clay,next_obsidian,next_geodes,ore_robots,clay_robots+1,obsidian_robots,geode_robots
        # to next ore robot
        if ore >= ore_ore and ore_robots < most_ore:
            yield next_time,next_ore-ore_ore,next_clay,next_obsidian,next_geodes,ore_robots+1,clay_robots,obsidian_robots,geode_robots
        # to end of time
        yield next_time,next_ore,next_clay,next_obsidian,next_geodes,ore_robots,clay_robots,obsidian_robots, geode_robots
    return neighbor_fn

start = 24,0,0,0,0,1,0,0,0

for blueprint in blueprints:
   bfs(start,lambda _:False, neighbors(blueprint))
   print(f"blueprint {blueprint[0]} cracks at most {max_geodes[blueprint[0]]} geodes")

part1 = sum(n*g for n,g in max_geodes.items())
print("Part 1:", part1)

start = 32,0,0,0,0,1,0,0,0
max_geodes.clear()

for blueprint in blueprints[:3]:
    dfs(start,lambda _:False, neighbors(blueprint))
    print(f"blueprint {blueprint[0]} cracks at most {max_geodes[blueprint[0]]} geodes")

part2 = product(max_geodes.values())
print("Part 2:", part2)
