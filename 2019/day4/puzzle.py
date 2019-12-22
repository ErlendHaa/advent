from itertools import groupby

def validate(rmin, rmax):
    part1, part2 = 0, 0
    current = rmin
    while current <= rmax:
        password = list(map(int, str(current)))
        if criteria1(password): part1 += 1
        if criteria2(password): part2 += 1
        current += 1
    return part1, part2

def criteria1(password):
    if len(set(password)) == len(password): return False
    if sorted(password)   != password:      return False
    return True

def criteria2(password):
    if sorted(password) != password:      return False
    if 2 not in [len(list(group)) for _, group in groupby(password)]: return False
    return True

if __name__ == '__main__':
    part1, part2 = validate(128392, 643281)
    print('Part 1: {}'.format(part1))
    print('Part 2: {}'.format(part2))
