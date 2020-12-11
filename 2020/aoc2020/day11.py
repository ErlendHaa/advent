import collections

import numpy as np

free  = 'L'
taken = '#'
floor = '.'

def parse(path):
    with open(path) as f:
        grid = np.array([[c for c in line.strip('\n')] for line in f.readlines()])
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if grid[x, y] == 'L': grid[x,y] = free
                if grid[x, y] == '#': grid[x,y] = taken
                if grid[x, y] == '.': grid[x,y] = floor

        return grid

def nadjacent_v1(grid, xinit, yinit):
    occupied = 0

    for x in [xinit - 1 , xinit, xinit + 1]:
        for y in [yinit - 1 , yinit, yinit + 1]:
            if x == xinit and y == yinit: continue
            if x < 0 or y < 0: continue

            try:
                if grid[x, y] == taken: occupied += 1
            except IndexError:
                continue

    return occupied


def nadjacent_v2(grid, xinit, yinit):
    occupied = 0
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]

    for d in dirs:
        n = 1
        while True:
            x = xinit + (d[0] * n)
            y = yinit + (d[1] * n)
            n += 1

            if x < 0 or y < 0: break

            try: state = grid[x, y]
            except IndexError: break

            if state == floor: continue
            if state == taken: occupied += 1
            break

    return occupied

def update(grid, maxocc, occurance):
    updates = {}
    for ix,iy in np.ndindex(grid.shape):
        state = grid[ix, iy]
        if state == floor: continue

        occ = occurance(grid, ix, iy)
        if state == taken and occ >= maxocc:
            updates[(ix, iy)] = free

        if state == free and occ == 0:
            updates[(ix, iy)] = taken

    return updates

def solve(grid, maxocc, occ):
    while True:
        updates = update(grid, maxocc, occ)
        if len(updates) == 0:
            return dict(zip(*np.unique(grid, return_counts=True)))[taken]
        for pos, state in updates.items():
            grid[pos] = state

def puzzle11(path='inputs/day11.txt'):
    grid = parse(path)

    part1 = solve(parse(path), 4, nadjacent_v1)
    part2 = solve(parse(path), 5, nadjacent_v2)

    return part1, part2
