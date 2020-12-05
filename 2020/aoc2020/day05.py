import math

def parse(path):
    with open(path) as f:
        return f.readlines()

def seatnumber(boardingpass):
    low, high = 0, 127
    for x in boardingpass[:6]:
        if x == 'B': low  += math.ceil( (high - low) / 2 )
        if x == 'F': high -= math.ceil( (high - low) / 2 )

    row = low if boardingpass[6] == 'F' else high

    low, high = 0, 7
    for x in boardingpass[7:9]:
        if x == 'R': low  += math.ceil( (high - low) / 2 )
        if x == 'L': high -= math.ceil( (high - low) / 2 )

    column = low if boardingpass[9] == 'L' else high
    return row, column


def seatid(row, column):
    return row * 8 + column

def findseat(seatids):
    for x in range(min(seatids) + 1, max(seatids) - 1):
        if x not in seatids: return x

    return missing

def puzzle5(path='inputs/day05.txt'):
    passes  = parse(path)
    seatids = [seatid(*seatnumber(x)) for x in passes]

    part1 = max(seatids)
    part2 = findseat(seatids)

    return part1, part2
