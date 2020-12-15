from collections import defaultdict

def parse(path):
    with open(path) as f:
        return list(map(int, f.readline().strip().split(',')))

def game(starting, nth):
    spoken = defaultdict(list)
    for i, number in enumerate(starting, start=1):
        spoken[number].append(i)

    last = starting[-1]
    i = len(starting) +  1

    while i <= nth:
        prev = spoken[last]
        if   len(prev) == 1: last = 0
        elif len(prev)  > 1: last = prev[-1] - prev[-2]

        spoken[last].append(i)
        i += 1

    return last


def puzzle15(path='inputs/day15.txt'):
    starting = parse(path)

    return game(starting, 2020), game(starting, 30000000)
