
def readcmds(inputfile):
    with open(inputfile) as f:
        return [x.strip('\n').split(' ') for x in f.readlines()]

def day2_part1(inputfile):
    depth, hpos = 0, 0
    for direction, distance in readcmds(inputfile):
        distance = int(distance)
        if direction == 'up':      depth -= distance
        if direction == 'down':    depth += distance
        if direction == 'forward': hpos  += distance

    return depth * hpos

def day2_part2(inputfile):
    depth, hpos, aim = 0, 0, 0
    for direction, distance in readcmds(inputfile):
        distance = int(distance)
        if direction == 'up':   aim -= distance
        if direction == 'down': aim += distance
        if direction == 'forward':
            hpos  += distance
            depth += (distance * aim)

    return depth * hpos
