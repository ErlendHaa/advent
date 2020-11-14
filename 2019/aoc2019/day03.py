from itertools import product

def parse(data):
    with open(data) as f:
        wire1 = f.readline().strip('\n').split(',')
        wire2 = f.readline().strip('\n').split(',')
    return wire1, wire2

def findpath(wire, x=0, y=0):
    points = []
    for turn in wire:
        direction = turn[0]
        lenght    = int(turn[1:])

        if direction == 'R':
            for _ in range(lenght):
                x += 1
                points.append((x, y))

        if direction == 'L':
            for _ in range(lenght):
                x -= 1
                points.append((x, y))

        if direction == 'U':
            for _ in range(lenght):
                y +=1
                points.append((x, y))

        if direction == 'D':
            for _ in range(lenght):
                y -= 1
                points.append((x, y))

    return {point : steps for steps, point in enumerate(points)}

def manhatten(point, x0=0, y0=0):
    return abs(point[0] - x0) + abs(point[1] - y0)

def puzzle3(path='inputs/day03.txt'):
    w1, w2 = parse(path)

    path1, path2 = findpath(w1), findpath(w2)

    intersections = set(path1.keys()).intersection(set(path2.keys()))

    shortest = min([manhatten(p) for p in intersections])
    fastest  = min([path1[x] + path2[x] + 2 for x in intersections])

    return shortest, fastest
