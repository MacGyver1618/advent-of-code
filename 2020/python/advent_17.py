from advent_lib import lines
import collections as coll

inpt = lines(17)

grid = []

for j,row in enumerate(inpt):
    for i,char in enumerate(row):
        if char == '#':
            grid.append((i,j,0))

for _ in range(6):
    ns = coll.defaultdict(lambda: 0)
    for p in grid:
        x,y,z = p
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                for k in range(z-1,z+2):
                    if not (i == x and j == y and k == z):
                        p2 = (i,j,k)
                        ns[p2] = ns[p2] + 1
    grid = [k for k,v in ns.items() if (k in grid and 2 <= v <= 3) or (k not in grid and v == 3)]

print("Part 1:", len(grid))


grid = []

for j,row in enumerate(inpt):
    for i,char in enumerate(row):
        if char == '#':
            grid.append((i,j,0,0))

for _ in range(6):
    ns = coll.defaultdict(lambda: 0)
    for p in grid:
        x,y,z,a = p
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                for k in range(z-1,z+2):
                    for l in range(a-1,a+2):
                        if not (i == x and j == y and k == z and l == a):
                            p2 = (i,j,k,l)
                            ns[p2] = ns[p2] + 1
    grid = [k for k,v in ns.items() if (k in grid and 2 <= v <= 3) or (k not in grid and v == 3)]

print("Part 2:", len(grid))
