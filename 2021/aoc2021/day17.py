import re

def parse(inputfile):
    line = open(inputfile).read().lstrip('target area: x=').strip('\n')
    limits = [ 'xmin', 'xmax', 'ymin', 'ymax']
    return { k : int(v) for  k, v in zip(limits, re.split('\.\.|, y=', line)) }

def xvelocity(xvel):
    if xvel >  0: return xvel - 1
    if xvel <  0: return xvel + 1
    if xvel == 0: return 0

def ingoal(xpos, ypos, goal):
    if xpos < goal['xmin']: return False
    if xpos > goal['xmax']: return False
    if ypos < goal['ymin']: return False
    if ypos > goal['ymax']: return False
    return True

def pastgoal(xpos, ypos, goal):
    if xpos > goal['xmax']: return True
    if ypos < goal['ymin']: return True
    return False

def simulatepath(xvel, yvel, goal):
    xpos, ypos = 0, 0
    path = [ (xpos, ypos) ]

    while True:
        if ingoal(xpos, ypos, goal):   return path
        if pastgoal(xpos, ypos, goal): return None

        xpos += xvel
        ypos += yvel
        xvel = xvelocity(xvel)
        yvel -= 1

        path.append((xpos, ypos))

def findpaths(goal):
    xvmin  = 0 # obviously invalid, but lets brute-force
    xvmax  = goal['xmax'] + 1
    yvmin  = goal['ymin'] - 1
    yv0max = xvmax

    candidates = {}
    for xvel0 in range(xvmin, xvmax):
        for yvel0 in range(goal['ymin'] - 1, xvmax):
            path = simulatepath(xvel0, yvel0, goal)
            if path: candidates[(xvel0, yvel0)] = path

    return candidates

def findhighest(candidates):
    highest = 0
    for init, path in candidates.items():
        maxy = max(path, key = lambda x: x[1])[1]
        if maxy <= highest: continue

        highest = maxy

    return highest

def day17_part1(inputfile):
    goal = parse(inputfile)
    candidates = findpaths(goal)
    return findhighest(candidates)

def day17_part2(inputfile):
    goal = parse(inputfile)
    candidates = findpaths(goal)
    return len(candidates)
