import math
from itertools   import tee
from collections import Counter
from collections import defaultdict


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def parse(inputfile):
    lines    = [x.strip('\n') for x in open(inputfile).readlines()]
    rules    = { tuple(line[0:2]) : line[6:7] for line in lines[2:] }
    sequence = defaultdict(lambda: 0)

    for pair in pairwise(lines[0]):
        sequence[pair] += 1

    return sequence, rules

def update(sequence, rules):
    updated = defaultdict(lambda: 0)

    for pair in sequence.keys():
        if pair not in rules:
            updated[pair] += 1
            continue

        char = rules[pair]
        count =  sequence[pair]

        updated[(pair[0], char)] += count
        updated[(char, pair[1])] += count

    return updated

def simulate(sequence, rules, days):
    for day in range(days):
        sequence = update(sequence, rules)

    return sequence

def score(sequence):
    expanded = defaultdict(lambda: 0)
    for (a, b), val in sequence.items():
        expanded[a] += val
        expanded[b] += val

    # I might be bit lucky that this works
    c = Counter(expanded)
    return math.ceil(max(c.values()) / 2 - min(c.values()) / 2)

def day14_part1(inputfile):
    sequence, rules = parse(inputfile)
    sequence = simulate(sequence, rules, days = 10)
    return score(sequence)

def day14_part2(inputfile):
    sequence, rules = parse(inputfile)
    sequence = simulate(sequence, rules, days = 40)
    return score(sequence)
