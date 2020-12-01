import itertools
import functools

def parse(path):
    with open(path) as f:
        return list( map( int, f.readlines() ) )

def solve(report, n):
    for com in itertools.combinations(report, n):
        if sum(com) != 2020: continue
        return functools.reduce( lambda x, y: x * y, com)

def puzzle1(path='inputs/day01.txt'):
    exp_report = parse(path)

    return solve(exp_report, 2), solve(exp_report, 3)
