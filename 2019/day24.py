import numpy as np

def parse(fpath):
    with open(fpath, 'r') as f:
        area = [list(line.strip('\n')) for line in f.readlines()]
        area = [x for line in area for x in line]
        return list(map(lambda x: 0 if x == '.' else 1, area))

def checksum(area):
    return sum([pow(2, i) for i, point in enumerate(area) if point])

def adjacent(area, i):
    up    = area[i-5] if i > 4         else 0
    down  = area[i+5] if i < 20        else 0
    left  = area[i-1] if i % 5     else 0
    right = area[i+1] if (i-4) % 5 else 0
    return up + down + left + right

def update(area):
    tmp = []

    for i, point in enumerate(area):
        bugs = adjacent(area, i)
        if point == 0 and (bugs == 1 or bugs == 2):
            tmp.append(1)
        elif point == 1 and bugs != 1:
            tmp.append(0)
        else:
            tmp.append(area[i])
    return tmp

if __name__ == '__main__':
    area = parse('inputs/day24.txt')

    layouts = set()
    cs = checksum(area)

    while cs not in layouts:
        layouts.add(cs)
        area = update(area)
        cs = checksum(area)

    print('Part 1: {}'.format(cs))
