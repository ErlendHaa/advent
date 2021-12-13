from collections import defaultdict

def parse(inputfile):
    caves = defaultdict(list)
    for line in open(inputfile).readlines():
        x, y = line.strip('\n').split('-')

        caves[x].append(y)
        caves[y].append(x)

    return caves

def skipv1(cave, path):
    return cave.lower() == cave and cave in path

def skipv2(cave, path):
    if cave.upper() == cave: return False
    if cave not in path:     return False
    if cave == 'start':      return True
    if cave == 'end':        return True

    path = [x for x in path if x.lower() == x]

    return len(path) != len(set(path))

def findallpaths(caves, start, end, skip, path=[]):
    path.append(start)
    if start == end: return [path]

    paths = []
    for cave in caves[start]:
        if skip(cave, path): continue
        for subpath in findallpaths(caves, cave, end, skip, path.copy()):
            paths.append(subpath)
    return paths

def day12_part1(inputfile):
    caves = parse(inputfile)
    paths = findallpaths(caves, 'start', 'end', skipv1, path=[])
    return len(paths)

def day12_part2(inputfile):
    caves = parse(inputfile)
    paths = findallpaths(caves, 'start', 'end', skipv2, path=[])
    return len(paths)
