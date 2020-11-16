import re
import datetime

from collections import defaultdict

def parse(fpath):
    with open(fpath) as f:
        lines = [x.strip('[').strip('\n').split('] ') for x in f.readlines()]

    entries = []
    for stamp, entry in lines:
        stamp = list(map(int, re.split('-| |:', stamp)))

        dt = datetime.datetime(
            year   = stamp[0],
            month  = stamp[1],
            day    = stamp[2],
            hour   = stamp[3],
            minute = stamp[4]
        )
        entries.append([dt, entry])

    return sorted(entries)

def inspect(shifts):
    guard   = None
    curtime = 0

    guards = defaultdict(lambda: [0] * 60)
    for time, entry in shifts:
        if   'Guard' in entry:
            guard   = int(entry.split(' ')[1].strip('#'))
            curtime = 0

        elif 'wakes' in entry:
            for time in range(curtime,int(time.minute)):
                guards[guard][time] += 1

        elif 'falls' in entry:
            curtime = int(time.minute)

    return guards

def part1(guards):
    guard   = None
    longest = float('-inf')

    for g, times in guards.items():
        if sum(times) < longest: continue
        guard   = g
        longest = sum(times)

    return guards[guard].index(max(guards[guard])) * guard

def part2(guards):
    guard   = None
    longest = float('-inf')

    for g, times in guards.items():
        if max(times) < longest: continue
        longest = max(times)
        guard   = g

    return guard * guards[guard].index(longest)

def puzzle4(path='inputs/day04.txt'):
    shifts = parse(path)

    guards = inspect(shifts)
    return part1(guards), part2(guards)
