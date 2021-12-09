import sys
import numpy as np

def parse(inputfile):
    data = [
        list(map(int, list(line.strip('\n'))))
        for line
        in open(inputfile).readlines()
    ]

    # Padd the hmap to avoid special casing for boundaries
    xdim, ydim = len(data[0]), len(data)
    arr = np.full((xdim + 2, ydim + 2), 10, dtype = np.int32)
    for x in range(xdim):
        for y in range(ydim):
            arr[x + 1][y + 1] = data[x][y]
    return arr

def adjacent(point):
    x, y = point
    ns = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for n in ns:
        yield n

def lowpoints(hmap):
    points = []
    xs, ys = hmap.shape

    for x in range(1, xs - 1):
        for y in range(1, ys - 1):
            point = hmap[x, y]
            if any(x for x in adjacent((x, y)) if point >= hmap[x]): continue
            points.append((x, y))

    return points

def basinsize(point, hmap, visited = []):
    size = 0
    if point not in visited:
        visited.append(point)
        size = 1 + sum([
            basinsize(n, hmap, visited)
            if 9 > hmap[n] > hmap[point]
            else 0
            for n
            in adjacent(point)
        ])

    return size

def day9_part1(inputfile):
    hmap = parse(inputfile)
    points = lowpoints(hmap)
    return sum([hmap[point] + 1 for point in points])

def day9_part2(inputfile):
    hmap = parse(inputfile)
    points = lowpoints(hmap)
    basins = [basinsize(p, hmap) for p in points]
    return np.prod(sorted(basins)[-3:])
