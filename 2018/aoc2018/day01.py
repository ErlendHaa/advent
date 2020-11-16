from collections import deque

def parse(fpath):
    with open(fpath) as f:
        return list(map(int, f.readlines()))

def cumulative(freqs):
    freqs = deque(freqs)
    seen = set()

    fr = freqs[0]
    while fr not in seen:
        seen.add(fr)
        freqs.rotate(-1)
        fr += freqs[0]

    return fr

def puzzle1(path='inputs/day01.txt'):
    freqs = parse(path)

    part1 = sum(freqs)
    part2 = cumulative(freqs)

    return part1, part2
