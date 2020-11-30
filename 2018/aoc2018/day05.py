from collections import deque

def parse(fpath):
    with open(fpath) as f:
        return ''.join(f.readlines()).strip('\n')

def remove_all_units(polymers):
    res = deque([polymers[0]])

    for x in polymers[1:]:
        if len(res) and x.swapcase() == res[-1]:
            res.pop()
        else:
            res.append(x)

    return len(res)

def puzzle5(path='inputs/day05.txt'):
    polymers = parse(path)

    remaining = remove_all_units(polymers)

    return remaining, 'Not implemented'
