from functools import cache

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

lines = read_lines(21)

numpad=Grid(["789","456","123","#0A"])
dirpad=Grid(["#^A","<v>"])
dirs={(0,-1):"<",(-1,0):"^",(1,0):"v",(0,1):">",}
seqs={}

def genseq(path):
    return ''.join(dirs[tuple(A(b)-A(a))] for a,b in zip(path[:-1],path[1:]))+"A"

def neighbors(pad):
    def _neighbors(p):
        r,c=p
        for dr,dc in dirs:
            n = r+dr, c+dc
            if pad.in_bounds(n) and pad.char_at(n)!= "#":
                yield n
    return _neighbors

def num_turns(path):
    s = genseq(path)
    return sum(a!=b for a,b in zip(s[1:],s))

def key_index(path):
    return tuple("<^v>A".index(dirs[tuple(A(b)-A(a))]) for a,b in zip(path[1:],path))

def path_sort_key(path):
    return num_turns(path), *key_index(path)

for s,c1 in dirpad.items():
    for e,c2 in dirpad.items():
        if "#" in [c1,c2]:
            continue
        seqs[f"{c1}{c2}"]=genseq(min(all_paths(s,eq(e),neighbors(dirpad)),key=path_sort_key))

#only case where BFS creates an extra turn
# seqs["A<"]="v<<A"
# seqs["<A"]=">>^A"
# seqs["<^"]=">^A"
# seqs["^<"]="v<A"

def keypad_length(path):
    seq="A"+genseq(path)
    out=""
    for i in range(len(seq)-1):
        sub = seq[i:i+2]
        out+=seqs[sub]
    return len(out)


for start,char1 in numpad.items():
    for end,char2 in numpad.items():
        if "#" in [char1,char2]:
            continue
        paths=all_paths(start, eq(end),neighbors(numpad))
        equiv_length=[path for path in paths if len(path)==len(paths[0])]
        #shortest=min([path for path in paths if len(path)==len(paths[0])], key=key_index)
        seqs[f"{char1}{char2}"]=genseq(min(equiv_length,key=num_turns))

# only cases where the shortest path contains an extra turn
# seqs["A1"]="^<<A"
# seqs["A4"]="^^<<A"
# seqs["A7"]="^^^<<A"
# seqs["1A"]=">>vA"
# seqs["4A"]=">>vvA"
# seqs["7A"]=">>vvvA"
# seqs["01"]="^<A"
# seqs["04"]="^^<A"
# seqs["07"]="^^^<A"
# seqs["10"]=">vA"
# seqs["40"]=">vvA"
# seqs["70"]=">vvvA"

@cache
def seqlength(start, end, depth):
    key=f"{start}{end}"
    if depth==0:
        return len(seqs[key])
    seq=seqs[key]
    return sum(seqlength(a,b,depth-1) for a,b in zip("A"+seq,seq))

part1=sum(sum(seqlength(a,b,2) for a,b in zip("A"+line,line))*int(line[:-1]) for line in lines)
part2=sum(sum(seqlength(a,b,25) for a,b in zip("A"+line,line))*int(line[:-1]) for line in lines)
print("Part 1:", part1)
print("Part 2:", part2)

n = [ "789", "456", "123", " 0A" ]
d = [ " ^A", "<v>" ]

# path between to adjacent nodes
def path( p, f, t ):
    fx, fy = next( ( x, y ) for y, r in enumerate( p ) for x, c in enumerate( r ) if c == f )
    tx, ty = next( ( x, y ) for y, r in enumerate( p ) for x, c in enumerate( r ) if c == t )
    def g( x, y, s ):
        if ( x, y ) == ( tx, ty ):            yield s + 'A'
        if tx < x and p[ y ][ x - 1 ] != ' ': yield from g( x - 1, y, s + '<' )
        if ty < y and p[ y - 1 ][ x ] != ' ': yield from g( x, y - 1, s + '^' )
        if ty > y and p[ y + 1 ][ x ] != ' ': yield from g( x, y + 1, s + 'v' )
        if tx > x and p[ y ][ x + 1 ] != ' ': yield from g( x + 1, y, s + '>' )
    return min( g( fx, fy, "" ), key = lambda p: sum( a != b for a, b in zip( p, p[ 1 : ] ) ) )

@cache
def solve( s, l ):
    if l > 25: return len( s )
    return sum( solve( path( d if l else n, f, t ), l + 1 ) for f, t in zip( 'A' + s, s ) )

print( sum( solve( s.strip(), 0 ) * int( s[ : 3 ] )
            for s in lines ) )

for a in "0123456789A":
    for b in "0123456789A":
        mine=seqs[f"{a}{b}"]
        theirs=path(n if a in "0123456789" or b in "0123456789" else d,a,b)
        if mine != theirs:
            print(f"{a}{b}: {mine}")
            print(f"    {theirs}")
for a in "<^v>A":
    for b in "<^v>A":
        mine=seqs[f"{a}{b}"]
        theirs=path(d,a,b)
        if mine != theirs:
            print(f"{a}{b}: {mine}")
            print(f"    {theirs}")

